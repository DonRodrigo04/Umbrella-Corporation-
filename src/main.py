import asyncio
import logging
import time
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import matplotlib.pyplot as plt

from src.services.genetico_service import GeneticoService
from src.services.bioquimico_service import BioquimicoService
from src.services.fisico_service import FisicoService
from src.config.settings import DATA_SOURCES, PROCESS_POOL_SIZE
from src.processing.orchestrator import run_orchestration

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")

# Clase para métricas
class MetricsMonitor:
    def __init__(self):
        self.records = []

    def log_event(self, service_name: str, latency: float, status: str):
        self.records.append({"service": service_name, "latency": latency, "status": status})

    def to_dataframe(self):
        return pd.DataFrame(self.records)

metrics_monitor = MetricsMonitor()

async def main():
    genetico_service = GeneticoService(DATA_SOURCES["genetico"])
    bioquimico_service = BioquimicoService(DATA_SOURCES["bioquimico"])
    fisico_service = FisicoService(DATA_SOURCES["fisico"])

    process_pool = ProcessPoolExecutor(max_workers=PROCESS_POOL_SIZE)

    async def process_with_executor(service, data):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(process_pool, service.analyze, data)

    async def process_data(service):
        while True:
            data = await service.queue.get()
            start = time.perf_counter()
            result = await process_with_executor(service, data)
            latency = time.perf_counter() - start
            status = "ALERT" if "alert" in str(result).lower() else "OK"
            metrics_monitor.log_event(service.__class__.__name__, latency, status)
            service.handle_result(result)
            service.queue.task_done()

    tasks = [
        asyncio.create_task(genetico_service.ingest_data()),
        asyncio.create_task(process_data(genetico_service)),
        asyncio.create_task(bioquimico_service.ingest_data()),
        asyncio.create_task(process_data(bioquimico_service)),
        asyncio.create_task(fisico_service.ingest_data()),
        asyncio.create_task(process_data(fisico_service)),
        asyncio.create_task(run_orchestration())
    ]

    await asyncio.gather(*tasks)

    # Visualización de métricas
    df = metrics_monitor.to_dataframe()
    logging.info("\nMétricas registradas:\n%s", df)

    # Gráfico de barras: latencia promedio por servicio
    avg_latency = df.groupby("service")["latency"].mean()
    avg_latency.plot(kind="bar", title="Latencia promedio por servicio", color="skyblue")
    plt.ylabel("Segundos")
    plt.tight_layout()
    plt.savefig("avg_latency.png")

    # Gráfico de pastel: distribución de estados
    status_counts = df["status"].value_counts()
    status_counts.plot(kind="pie", autopct="%1.1f%%", title="Distribución de estados")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("status_distribution.png")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Sistema detenido manualmente.")