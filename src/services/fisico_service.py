# src/services/fisico_service.py

import asyncio
import logging
from typing import Dict, Any
from src.utils.normalizer import normalize_data

# Configurar logger
logger = logging.getLogger("FisicoService")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class FisicoService:
    def __init__(self, source: str):
        self.source = source
        self.queue = asyncio.Queue()
        logger.info(f"FisicoService inicializado con fuente: {self.source}")

    async def ingest_data(self):
        """
        Simula la ingesta de datos físicos desde una fuente asíncrona.
        """
        while True:
            raw_data = await self.fetch_from_source()
            logger.debug(f"Datos crudos recibidos: {raw_data}")
            normalized = normalize_data(raw_data, data_type="fisico")
            await self.queue.put(normalized)
            logger.info(f"Datos normalizados en cola: {normalized['sample_id']}")
            await asyncio.sleep(0.3)  # Simula latencia

    async def fetch_from_source(self) -> Dict[str, Any]:
        """
        Simula la obtención de datos físicos.
        """
        return {
            "sample_id": "F789",
            "temperature": 36.7,
            "pressure": 101.3
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
        Analiza parámetros físicos.
        """
        result = {
            "sample_id": data["sample_id"],
            "temperature_alert": data["temperature"] < 35.0 or data["temperature"] > 38.0,
            "pressure_alert": data["pressure"] < 98.0 or data["pressure"] > 105.0
        }
        logger.debug(f"Resultado del análisis: {result}")
        return result

    def handle_result(self, result: Dict[str, Any]):
        """
        Maneja el resultado del análisis.
        """
        if result["temperature_alert"] or result["pressure_alert"]:
            logger.warning(f"[ALERTA] Parámetros físicos fuera de rango: {result}")
        else:
            logger.info(f"Resultado normal: {result}")