"""Testes do cliente MCP WhatsApp (TDD RED)."""

from unittest.mock import MagicMock, patch

import pytest

from app.integrations.mcp_whatsapp import (
    McpWhatsAppClient,
    McpWhatsAppError,
    normalize_e164,
)


def test_normalize_e164_br_with_plus() -> None:
    assert normalize_e164("+55 11 91234-5678") == "+5511912345678"


def test_normalize_e164_br_without_country() -> None:
    assert normalize_e164("(11) 91234-5678") == "+5511912345678"


def test_normalize_e164_empty() -> None:
    assert normalize_e164("") is None
    assert normalize_e164(None) is None


def test_send_message_success() -> None:
    client = McpWhatsAppClient(base_url="http://mcp.local", token="tok")
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"status": "sent"}
    fake_response.text = "ok"
    with patch("httpx.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.post.return_value = fake_response
        mock_client_cls.return_value.__enter__.return_value = mock_client
        result = client.send_message("+5511912345678", "cobranca", {"x": 1})
    assert result == {"status": "sent"}


def test_send_message_disabled_returns_none() -> None:
    client = McpWhatsAppClient(base_url=None, token=None)
    assert client.enabled is False
    assert client.send_message("+5511912345678", "cobranca", {}) is None


def test_send_message_invalid_number_raises() -> None:
    client = McpWhatsAppClient(base_url="http://mcp.local")
    with pytest.raises(McpWhatsAppError):
        client.send_message("", "cobranca", {})


def test_send_message_retries_then_raises() -> None:
    client = McpWhatsAppClient(base_url="http://mcp.local", timeout=0.1)
    fake_response = MagicMock()
    fake_response.status_code = 500
    fake_response.text = "boom"
    with patch("httpx.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.post.return_value = fake_response
        mock_client_cls.return_value.__enter__.return_value = mock_client
        with pytest.raises(McpWhatsAppError):
            client.send_message("+5511912345678", "cobranca", {})
    assert mock_client.post.call_count == 3
