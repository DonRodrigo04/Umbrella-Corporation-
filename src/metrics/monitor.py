import asyncio
import logging
import time
from typing import Dict, Any
from src.utils.normalizer import normalize_data
from src.metrics.monitor import MetricsMonitor
from src.alerts.notifier import send_alert

# Configuración del logger
logger = logging.getLogger("GeneticoService")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class GeneticoService:
    def __init__(self, source: str):
        self.source = source
        self.queue = asyncio.Queue()
        self.monitor = MetricsMonitor()
        logger.info(f"GeneticoService inicializado con fuente: {self.source}")

    async def ingest_data(self):
        while True:
            raw_data = await self.fetch_from_source()
            normalized = normalize_data(raw_data, data_type="genetico")
            await self.queue.put(normalized)
            logger.info(f"Datos normalizados en cola: {normalized['sample_id']}")
            await asyncio.sleep(0.1)

    async def fetch_from_source(self) -> Dict[str, Any]:
        return {"sample_id": "G123", "sequence": "ATCGTTAG", "quality": 0.98}

    async def process_data(self):
        while True:
            data = await self.queue.get()
            start_time = time.perf_counter()
            result = self.analyze(data)
            self.handle_result(result)
            latency_ms = (time.perf_counter() - start_time) * 1000
            self.monitor.record_event("GeneticoService", latency_ms, "OK" if result["confidence"] > 0.9 else "NORMAL")
            self.queue.task_done()

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"sample_id": data["sample_id"], "mutation_detected": "TP53", "confidence": 0.95}

    def handle_result(self, result: Dict[str, Any]):
        if result["confidence"] > 0.9:
            send_alert({
                "sample_id": result["sample_id"],
                "mutation": result["mutation_detected"],
                "confidence": result["confidence"],
                "message": "Mutación crítica detectada"
            })
        else:
            logger.info(f"Resultado no crítico: {result}")
    class MetricsMonitor:
    def __init__(self):
        self.records = []

    def log_event(self, service_name: str, latency: float, status: str):
        self.records.append({"service": service_name, "latency": latency, "status": status})

    def to_dataframe(self):
        import pandas as pd
        return pd.DataFrame(self.records)
    