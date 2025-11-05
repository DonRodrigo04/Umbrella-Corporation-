# src/main.py

import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor
from src.services.genetico_service import GeneticoService
from src.services.bioquimico_service import BioquimicoService
from src.services.fisico_service import FisicoService
from src.config.settings import DATA_SOURCES, PROCESS_POOL_SIZE

# Configuración centralizada de logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
)

async def main():
    # Instanciar servicios
    genetico_service = GeneticoService(DATA_SOURCES["genetico"])
    bioquimico_service = BioquimicoService(DATA_SOURCES["bioquimico"])
    fisico_service = FisicoService(DATA_SOURCES["fisico"])

    # Crear un ProcessPoolExecutor para análisis CPU-bound
    process_pool = ProcessPoolExecutor(max_workers=PROCESS_POOL_SIZE)

    async def process_with_executor(service, data):
        """
        Ejecuta el análisis en un proceso separado para evitar bloquear el loop.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(process_pool, service.analyze, data)

    async def process_data(service):
        """
        Extrae datos de la cola y los procesa usando el pool de procesos.
        """
        while True:
            data = await service.queue.get()
            logging.info(f"Procesando muestra {data['sample_id']} con {service.__class__.__name__}")
            result = await process_with_executor(service, data)
            service.handle_result(result)
            service.queue.task_done()

    # Crear tareas para ingesta y procesamiento concurrente
    tasks = [
        asyncio.create_task(genetico_service.ingest_data()),
        asyncio.create_task(process_data(genetico_service)),
        asyncio.create_task(bioquimico_service.ingest_data()),
        asyncio.create_task(process_data(bioquimico_service)),
        asyncio.create_task(fisico_service.ingest_data()),
        asyncio.create_task(process_data(fisico_service))
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Sistema detenido manualmente.")