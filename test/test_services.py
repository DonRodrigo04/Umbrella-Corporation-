import pytest
from unittest.mock import patch
from src.services.genetico_service import GeneticoService
from src.services.bioquimico_service import BioquimicoService
from src.services.fisico_service import FisicoService

# -------------------------
# GENETICO SERVICE TESTS
# -------------------------
@pytest.mark.asyncio
async def test_genetico_service_normal_result():
    service = GeneticoService("dummy_source")
    data = {"sample_id": "G001", "sequence": "ATCG", "quality": 0.85}
    result = service.analyze(data)

    assert result["mutation_detected"] == "TP53"
    assert result["confidence"] == 0.95

@pytest.mark.asyncio
async def test_genetico_service_alert_triggered():
    service = GeneticoService("dummy_source")
    data = {"sample_id": "G002", "sequence": "ATCG", "quality": 0.99}
    result = service.analyze(data)

    with patch("src.alerts.notifier.send_alert") as mock_alert:
        service.handle_result(result)
        mock_alert.assert_called_once()
        args = mock_alert.call_args[0][0]
        assert args["sample_id"] == "G002"
        assert "Mutación crítica detectada" in args["message"]

# -------------------------
# BIOQUIMICO SERVICE TESTS
# -------------------------
@pytest.mark.asyncio
async def test_bioquimico_service_normal_result():
    service = BioquimicoService("dummy_source")
    data = {"sample_id": "B001", "ph": 7.4, "enzyme_activity": 120.0}
    result = service.analyze(data)

    assert result["anomaly_detected"] is False
    assert result["enzyme_activity"] == 120.0

@pytest.mark.asyncio
async def test_bioquimico_service_alert_triggered():
    service = BioquimicoService("dummy_source")
    data = {"sample_id": "B002", "ph": 6.0, "enzyme_activity": 100.0}
    result = service.analyze(data)

    with patch("src.alerts.notifier.send_alert") as mock_alert:
        service.handle_result(result)
        mock_alert.assert_called_once()
        args = mock_alert.call_args[0][0]
        assert args["sample_id"] == "B002"
        assert "Anomalía bioquímica detectada" in args["message"]

# -------------------------
# FISICO SERVICE TESTS
# -------------------------
@pytest.mark.asyncio
async def test_fisico_service_normal_result():
    service = FisicoService("dummy_source")
    data = {"sample_id": "F001", "temperature": 36.5, "pressure": 101.0}
    result = service.analyze(data)

    assert result["temperature_alert"] is False
    assert result["pressure_alert"] is False

@pytest.mark.asyncio
async def test_fisico_service_alert_triggered():
    service = FisicoService("dummy_source")
    data = {"sample_id": "F002", "temperature": 39.0, "pressure": 101.0}
    result = service.analyze(data)

    with patch("src.alerts.notifier.send_alert") as mock_alert:
        service.handle_result(result)
        mock_alert.assert_called_once()
        args = mock_alert.call_args[0][0]
        assert args["sample_id"] == "F002"
        assert "Parámetros físicos fuera de rango" in args["message"]