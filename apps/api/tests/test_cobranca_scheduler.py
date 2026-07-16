"""Testes do scheduler de cobrança (TDD)."""

from unittest.mock import MagicMock, patch

import pytest

from app.modules.shipments import scheduler as scheduler_module
from app.modules.shipments.scheduler import (
    _parse_cron,
    shutdown_cobranca_scheduler,
    start_cobranca_scheduler,
)


def test_parse_cron_valido():
    result = _parse_cron("0 9 * * *")
    assert result == {
        "minute": "0",
        "hour": "9",
        "day": "*",
        "month": "*",
        "day_of_week": "*",
    }


def test_parse_cron_invalido_levanta():
    with pytest.raises(ValueError):
        _parse_cron("0 9 *")


def test_start_scheduler_chama_run_cobranca_quando_habilitado():
    fake_result = {
        "enviadas": 1,
        "puladas_sem_whatsapp": 0,
        "falhas": 0,
        "critico_escalonado": 0,
    }
    with patch.object(scheduler_module.settings, "cobranca_scheduler_enabled", True), patch.object(
        scheduler_module.settings, "cobranca_cron", "0 9 * * *"
    ), patch.object(
        scheduler_module.settings, "cobranca_dias_min", 1
    ), patch.object(
        scheduler_module.settings, "cobranca_dias_max", 999
    ), patch(
        "app.modules.shipments.scheduler.run_cobranca", return_value=fake_result
    ) as mock_run, patch(
        "app.modules.shipments.scheduler.SessionLocal"
    ) as mock_session_factory:
        mock_session = MagicMock()
        mock_session_factory.return_value.__enter__.return_value = mock_session
        mock_session_factory.return_value.__exit__.return_value = False

        sched = start_cobranca_scheduler()
        try:
            assert sched is not None
            # Dispara o job manualmente para validar a chamada
            scheduler_module._job()
            mock_run.assert_called_once()
            kwargs = mock_run.call_args.kwargs
            assert kwargs["dias_min"] == 1
            assert kwargs["dias_max"] == 999
        finally:
            shutdown_cobranca_scheduler()


def test_start_scheduler_retorna_none_quando_desabilitado():
    with patch.object(scheduler_module.settings, "cobranca_scheduler_enabled", False):
        sched = start_cobranca_scheduler()
        assert sched is None
