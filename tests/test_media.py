from __future__ import annotations

import base64
import hashlib
from unittest.mock import AsyncMock

import httpx
import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac as crypto_hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from wazzapi.errors import WazzapiMediaError
from wazzapi.media import _decrypt_wa_media, _media_info_bytes, download_media

PLAINTEXT = b"hello world this is a test file"
MIMETYPE = "application/pdf"
_MEDIA_KEY_BYTES = b"\x00" * 32
MEDIA_KEY = base64.b64encode(_MEDIA_KEY_BYTES).decode()


def _encrypt_wa_media(plaintext: bytes, media_key: bytes, mimetype: str) -> bytes:
    info = _media_info_bytes(mimetype)
    hkdf = HKDF(algorithm=hashes.SHA256(), length=112, salt=None, info=info)
    expanded = hkdf.derive(media_key)
    iv = expanded[:16]
    aes_key = expanded[16:48]
    mac_key = expanded[48:80]

    pad_len = 16 - (len(plaintext) % 16)
    padded = plaintext + bytes([pad_len] * pad_len)

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    h = crypto_hmac.HMAC(mac_key, hashes.SHA256())
    h.update(iv + ciphertext)
    mac = h.finalize()[:10]

    return ciphertext + mac


ENC_BLOB = _encrypt_wa_media(PLAINTEXT, _MEDIA_KEY_BYTES, MIMETYPE)
FILE_SHA256 = base64.b64encode(hashlib.sha256(PLAINTEXT).digest()).decode()
ENC_SHA256 = base64.b64encode(hashlib.sha256(ENC_BLOB).digest()).decode()


def _mock_client(enc_data: bytes, status_code: int = 200) -> AsyncMock:
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    request = httpx.Request("GET", "https://cdn.example.com/file")
    mock_client.get.return_value = httpx.Response(status_code, content=enc_data, request=request)
    mock_client.aclose = AsyncMock()
    return mock_client


def test_decrypt_wa_media_success() -> None:
    result = _decrypt_wa_media(MEDIA_KEY, ENC_BLOB, MIMETYPE)
    assert result == PLAINTEXT


def test_decrypt_wa_media_mac_failure() -> None:
    bad_blob = ENC_BLOB[:-10] + b"\x00" * 10
    with pytest.raises(WazzapiMediaError, match="MAC verification failed"):
        _decrypt_wa_media(MEDIA_KEY, bad_blob, MIMETYPE)


def test_decrypt_wa_media_short_data() -> None:
    with pytest.raises(WazzapiMediaError, match="Encrypted data too short"):
        _decrypt_wa_media(MEDIA_KEY, b"123", MIMETYPE)


def test_decrypt_wa_media_bad_base64_key() -> None:
    with pytest.raises(WazzapiMediaError, match="Invalid media_key base64"):
        _decrypt_wa_media("not-valid-b64!!!", ENC_BLOB, MIMETYPE)


def test_media_info_bytes_mapping() -> None:
    assert _media_info_bytes("image/jpeg") == b"WhatsApp Image Keys"
    assert _media_info_bytes("video/mp4") == b"WhatsApp Video Keys"
    assert _media_info_bytes("audio/ogg") == b"WhatsApp Audio Keys"
    assert _media_info_bytes("application/pdf") == b"WhatsApp Document Keys"


@pytest.mark.asyncio
async def test_download_media_success() -> None:
    mock_client = _mock_client(ENC_BLOB)
    result = await download_media(
        url="https://cdn.example.com/file",
        media_key=MEDIA_KEY,
        mimetype=MIMETYPE,
        file_sha256=FILE_SHA256,
        file_enc_sha256=ENC_SHA256,
        file_name="test.pdf",
        http_client=mock_client,
    )
    assert result.content == PLAINTEXT
    assert result.mimetype == MIMETYPE
    assert result.file_name == "test.pdf"
    assert result.file_size == len(PLAINTEXT)
    mock_client.get.assert_awaited_once_with("https://cdn.example.com/file")
    mock_client.aclose.assert_not_awaited()


@pytest.mark.asyncio
async def test_download_media_http_error() -> None:
    mock_client = _mock_client(b"not found", status_code=404)
    with pytest.raises(WazzapiMediaError, match="CDN fetch failed: 404"):
        await download_media(
            url="https://cdn.example.com/file",
            media_key=MEDIA_KEY,
            mimetype=MIMETYPE,
            http_client=mock_client,
        )


@pytest.mark.asyncio
async def test_download_media_network_error() -> None:
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.get.side_effect = httpx.RequestError(
        "connection refused", request=httpx.Request("GET", "https://cdn.example.com/file")
    )
    mock_client.aclose = AsyncMock()
    with pytest.raises(WazzapiMediaError, match="CDN fetch error:"):
        await download_media(
            url="https://cdn.example.com/file",
            media_key=MEDIA_KEY,
            mimetype=MIMETYPE,
            http_client=mock_client,
        )


@pytest.mark.asyncio
async def test_download_media_enc_sha_mismatch() -> None:
    mock_client = _mock_client(ENC_BLOB)
    with pytest.raises(WazzapiMediaError, match="file_enc_sha256 mismatch"):
        await download_media(
            url="https://cdn.example.com/file",
            media_key=MEDIA_KEY,
            mimetype=MIMETYPE,
            file_enc_sha256=base64.b64encode(hashlib.sha256(b"wrong").digest()).decode(),
            http_client=mock_client,
        )


@pytest.mark.asyncio
async def test_download_media_plain_sha_mismatch() -> None:
    mock_client = _mock_client(ENC_BLOB)
    with pytest.raises(WazzapiMediaError, match="file_sha256 mismatch after decryption"):
        await download_media(
            url="https://cdn.example.com/file",
            media_key=MEDIA_KEY,
            mimetype=MIMETYPE,
            file_sha256=base64.b64encode(hashlib.sha256(b"wrong").digest()).decode(),
            http_client=mock_client,
        )


@pytest.mark.asyncio
async def test_download_media_no_checksums() -> None:
    mock_client = _mock_client(ENC_BLOB)
    result = await download_media(
        url="https://cdn.example.com/file",
        media_key=MEDIA_KEY,
        mimetype=MIMETYPE,
        http_client=mock_client,
    )
    assert result.content == PLAINTEXT
    assert result.file_name == "media"
