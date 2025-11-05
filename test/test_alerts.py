import pytest
from src.alerts.notifier import send_alert
from src.config import settings

def test_send_alert_log(monkeypatch, caplog):
    # Forzar canal de alerta a "log"
    monkeypatch.setattr(settings, "ALERT_CHANNEL", "log")

    event = {"sample_id": "G123", "message": "Mutación crítica detectada"}
    with caplog.at_level("WARNING"):
        send_alert(event)
    assert "[ALERTA]" in caplog.text
    assert "Mutación crítica detectada" in caplog.text

def test_send_alert_invalid_channel(monkeypatch, caplog):
    # Canal inválido
    monkeypatch.setattr(settings, "ALERT_CHANNEL", "sms")

    event = {"sample_id": "G123", "message": "Evento crítico"}
    with caplog.at_level("ERROR"):
        send_alert(event)
    assert "Canal de alerta no soportado" in caplog.text