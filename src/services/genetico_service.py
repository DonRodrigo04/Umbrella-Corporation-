# src/services/genetico_service.py

import asyncio
import logging
from typing import Dict, Any
from src.utils.normalizer import normalize_data

# Configurar logger
logger = logging.getLogger("GeneticoService")
logger.setLevel(logging.INFO)

# Puedes configurar el handler en main.py para centralizarlo
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class GeneticoService:
    def __init__(self, source: str):
        self.source = source
        self.queue = asyncio.Queue()
        logger.info(f"GeneticoService inicializado con fuente: {self.source}")

    async def ingest_data(self):
        """
        Simula la ingesta de datos genéticos desde una fuente asíncrona.
        """
        while True:
            raw_data = await self.fetch_from_source()
            logger.debug(f"Datos crudos recibidos: {raw_data}")
            normalized = normalize_data(raw_data, data_type="genetico")
            await self.queue.put(normalized)
            logger.info(f"Datos normalizados en cola: {normalized['sample_id']}")
            await asyncio.sleep(0.1)

    async def fetch_from_source(self) -> Dict[str, Any]:
        """
        Simula la obtención de datos genéticos.
        """
        # Simulación de datos
        return {
            "sample_id": "G123",
            "sequence": "ATCGTTAG",
            "quality": 0.98
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
        Analiza la secuencia genética.
        """
        # Lógica de análisis genético (placeholder)
        result = {
            "sample_id": data["sample_id"],
            "mutation_detected": "TP53",
            "confidence": 0.95
        }
        logger.debug(f"Resultado del análisis: {result}")
        return result

    def handle_result(self, result: Dict[str, Any]):
        """
        Maneja el resultado del análisis.
        """
        if result["confidence"] > 0.9:
            logger.warning(f"[ALERTA] Mutación crítica detectada: {result}")
        else:
            logger.info(f"Resultado no crítico: {result}")