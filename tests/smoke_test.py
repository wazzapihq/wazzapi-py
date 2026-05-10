from __future__ import annotations

from wazzapi import (
    SendMessageRequest,
    WazzapiClient,
    WebhookHandler,
    __version__,
    generate_webhook_signature,
)


def main() -> None:
    assert __version__ == "0.3.0"

    client = WazzapiClient(api_key="smoke-test-token")
    try:
        assert str(client.http.base_url) == "https://api.wazzapi.com"
        assert client.http.headers["Authorization"] == "Bearer smoke-test-token"
    finally:
        client.close()

    request = SendMessageRequest(
        phone_number="+6281234567890",
        whatsapp_account_id="wa_123",
        content="smoke test",
    )
    assert request.phone_number == "+6281234567890"
    assert request.content == "smoke test"

    handler = WebhookHandler("secret")
    signature = generate_webhook_signature(b"{}", "secret")
    assert handler.verify_signature(b"{}", signature)

    print("smoke-ok")


if __name__ == "__main__":
    main()
