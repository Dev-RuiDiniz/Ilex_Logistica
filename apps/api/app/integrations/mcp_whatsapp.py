"""Cliente MCP para envio de mensagens WhatsApp.

Conector externo desacoplado (AGENTS.md 7.2): timeout, retry controlado,
idempotência e observabilidade. Se a URL do MCP não estiver configurada,
opera em modo de degradação (retorna None) para que a rotina de cobrança
registre apenas o log interno sem quebrar o batch.
"""

from __future__ import annotations

import logging
import time

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 3
BACKOFF_SECONDS = 1.0


class McpWhatsAppError(Exception):
    """Erro ao enviar mensagem via MCP WhatsApp."""


def normalize_e164(number: str | None) -> str | None:
    """Normaliza um número de telefone para o formato E.164 (+55...)."""
    if not number:
        return None
    digits = "".join(ch for ch in number if ch.isdigit())
    if not digits:
        return None
    if digits.startswith("55") and len(digits) >= 12:
        return f"+{digits}"
    if len(digits) == 11 or len(digits) == 10:
        return f"+55{digits}"
    if digits.startswith("+"):
        return digits
    return f"+{digits}"


class McpWhatsAppClient:
    """Cliente do servidor MCP que expõe a ferramenta send_whatsapp_message."""

    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.base_url = base_url or settings.mcp_whatsapp_url
        self.token = token or settings.mcp_whatsapp_token
        self.timeout = timeout if timeout is not None else settings.mcp_whatsapp_timeout

    @property
    def enabled(self) -> bool:
        return bool(self.base_url)

    def send_message(self, to: str, template: str, variables: dict) -> dict | None:
        """Envia mensagem via MCP.

        Retorna o payload de resposta em caso de sucesso, ou None quando o
        MCP não está configurado (modo de degradação). Levanta McpWhatsAppError
        após esgotar as tentativas em caso de falha persistente.
        """
        normalized = normalize_e164(to)
        if not normalized:
            raise McpWhatsAppError("numero de destinatario invalido ou ausente")
        if not self.enabled:
            logger.warning("MCP WhatsApp nao configurado; enviando em modo de degradacao")
            return None

        payload = {
            "tool": "send_whatsapp_message",
            "arguments": {
                "to": normalized,
                "template": template,
                "variables": variables,
            },
        }
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        last_error: Exception | None = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(f"{self.base_url.rstrip('/')}/invoke", json=payload, headers=headers)
                if response.status_code >= 200 and response.status_code < 300:
                    try:
                        return response.json()
                    except ValueError:
                        return {"status": "ok"}
                last_error = McpWhatsAppError(
                    f"MCP retornou status {response.status_code}: {response.text[:200]}"
                )
            except httpx.HTTPError as exc:
                last_error = McpWhatsAppError(f"erro de transporte MCP: {exc}")
            if attempt < MAX_ATTEMPTS:
                time.sleep(BACKOFF_SECONDS * attempt)
        raise McpWhatsAppError(f"falha apos {MAX_ATTEMPTS} tentativas: {last_error}")


def get_mcp_whatsapp_client() -> McpWhatsAppClient:
    return McpWhatsAppClient()
