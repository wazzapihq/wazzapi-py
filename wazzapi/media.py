from __future__ import annotations

import base64
import hashlib
import logging

import httpx
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac as crypto_hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from .errors import WazzapiMediaError
from .models.media import MediaDownloadResult

logger = logging.getLogger("wazzapi.media")

# https://github.com/tgalal/python-axolotl/wiki/WhatsApp-media-encryption
_WA_MEDIA_INFO: dict[str, bytes] = {
    "image": b"WhatsApp Image Keys",
    "video": b"WhatsApp Video Keys",
    "audio": b"WhatsApp Audio Keys",
    "ptt": b"WhatsApp Audio Keys",
    "document": b"WhatsApp Document Keys",
    "sticker": b"WhatsApp Image Keys",
    "history": b"WhatsApp History Keys",
}


def _media_info_bytes(mimetype: str) -> bytes:
    mt = mimetype.lower()
    if mt.startswith("image/"):
        return _WA_MEDIA_INFO["image"]
    if mt.startswith("video/"):
        return _WA_MEDIA_INFO["video"]
    if mt.startswith("audio/"):
        return _WA_MEDIA_INFO["audio"]
    return _WA_MEDIA_INFO["document"]


def _decrypt_wa_media(media_key_b64: str, enc_data: bytes, mimetype: str) -> bytes:
    if len(enc_data) < 10:
        raise WazzapiMediaError("Encrypted data too short")

    try:
        media_key = base64.b64decode(media_key_b64)
    except Exception as exc:
        raise WazzapiMediaError("Invalid media_key base64") from exc

    info = _media_info_bytes(mimetype)

    hkdf = HKDF(algorithm=hashes.SHA256(), length=112, salt=None, info=info)
    expanded = hkdf.derive(media_key)

    iv = expanded[:16]
    aes_key = expanded[16:48]
    mac_key = expanded[48:80]

    ciphertext = enc_data[:-10]
    mac = enc_data[-10:]

    h = crypto_hmac.HMAC(mac_key, hashes.SHA256())
    h.update(iv + ciphertext)
    computed_mac = h.finalize()[:10]
    if computed_mac != mac:
        raise WazzapiMediaError(
            "MAC verification failed — media may be corrupted or mediaKey is wrong"
        )

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()

    if not plaintext_padded:
        raise WazzapiMediaError("Decrypted plaintext is empty")

    pad_len = plaintext_padded[-1]
    if pad_len > 16 or pad_len == 0 or pad_len > len(plaintext_padded):
        raise WazzapiMediaError("Invalid PKCS7 padding")
    if any(b != pad_len for b in plaintext_padded[-pad_len:]):
        raise WazzapiMediaError("Invalid PKCS7 padding")

    return plaintext_padded[:-pad_len]


async def download_media(
    url: str,
    media_key: str,
    mimetype: str,
    *,
    file_sha256: str | None = None,
    file_enc_sha256: str | None = None,
    file_name: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> MediaDownloadResult:
    logger.info("Downloading media url=%s mimetype=%s", url, mimetype)

    client = http_client or httpx.AsyncClient(follow_redirects=True, timeout=30)
    owns_client = http_client is None

    try:
        resp = await client.get(url)
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error("CDN fetch failed: %s", exc)
        raise WazzapiMediaError(f"CDN fetch failed: {exc.response.status_code}") from exc
    except httpx.RequestError as exc:
        logger.error("CDN network error: %s", exc)
        raise WazzapiMediaError(f"CDN fetch error: {exc}") from exc
    finally:
        if owns_client:
            await client.aclose()

    enc_data = resp.content

    if file_enc_sha256:
        expected_enc = base64.b64decode(file_enc_sha256)
        actual_enc = hashlib.sha256(enc_data).digest()
        if actual_enc != expected_enc:
            raise WazzapiMediaError(
                f"file_enc_sha256 mismatch: CDN returned wrong data (got {len(enc_data)} bytes)"
            )

    plaintext = _decrypt_wa_media(media_key, enc_data, mimetype)

    if file_sha256:
        expected = base64.b64decode(file_sha256)
        actual = hashlib.sha256(plaintext).digest()
        if actual != expected:
            raise WazzapiMediaError("file_sha256 mismatch after decryption")

    result = MediaDownloadResult(
        content=plaintext,
        mimetype=mimetype,
        file_name=file_name or "media",
        file_size=len(plaintext),
    )
    logger.info("Media download success url=%s size=%d", url, result.file_size)
    return result


__all__ = [
    "MediaDownloadResult",
    "_decrypt_wa_media",
    "_media_info_bytes",
    "download_media",
]
