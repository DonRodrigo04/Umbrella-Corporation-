# src/services/bioquimico_service.py

import asyncio
import logging
from typing import Dict, Any
from src.utils.normalizer import normalize_data

# Configurar logger
logger = logging.getLogger("BioquimicoService")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class BioquimicoService:
    def __init__(self, source: str):
        self.source = source
        self.queue = asyncio.Queue()
        logger.info(f"BioquimicoService inicializado con fuente: {self.source}")

    async def ingest_data(self):
        """
        Simula la ingesta de datos bioquímicos desde una fuente asíncrona.
        """
        while True:
            raw_data = await self.fetch_from_source()
            logger.debug(f"Datos crudos recibidos: {raw_data}")
            normalized = normalize_data(raw_data, data_type="bioquimico")
            await self.queue.put(normalized)
            logger.info(f"Datos normalizados en cola: {normalized['sample_id']}")
            await asyncio.sleep(0.2)  # Simula latencia

    async def fetch_from_source(self) -> Dict[str, Any]:
        """
        Simula la obtención de datos bioquímicos.
        """
        return {
            "sample_id": "B456",
            "ph": 7.4,
            "enzyme_activity": 120.5
        }

    async def process_data(self):
        """
        Procesa datos normalizados desde la cola.
        """
        while True:
            data = await self.queue.get()
            logger.info(f"Procesando muestra: {data['sample_id']}")
            result = self.analyze(data)
            self.handle_result(result)
            self.queue.task_done()

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza parámetros bioquímicos.
        """
        result = {
            "sample_id": data["sample_id"],
            "anomaly_detected": data["ph"] < 7.0 or data["ph"] > 7.8,
            "enzyme_activity": data["enzyme_activity"]
        }
        logger.debug(f"Resultado del análisis: {result}")
        return result

    def handle_result(self, result: Dict[str, Any]):
        """
        Maneja el resultado del análisis.
        """
        if result["anomaly_detected"]:
            logger.warning(f"[ALERTA] Anomalía bioquímica detectada: {result}")
        else:
            logger.info(f"Resultado normal: {result}")
