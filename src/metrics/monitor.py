from src.metrics.monitor import MetricsMonitor
from src.alerts.notifier import send_alert
import time

class FisicoService:
    def __init__(self, source: str):
        self.source = source
        self.queue = asyncio.Queue()
        self.monitor = MetricsMonitor()  # Instancia del monitor
        logger.info(f"FisicoService inicializado con fuente: {self.source}")

    async def process_data(self):
        """
        Procesa datos normalizados desde la cola y registra métricas.
        """
        while True:
            data = await self.queue.get()
            start_time = time.perf_counter()  # Inicio para medir latencia

            logger.info(f"Procesando muestra: {data['sample_id']}")
            result = self.analyze(data)
            self.handle_result(result)

            # Calcular latencia
            latency_ms = (time.perf_counter() - start_time) * 1000
            status = "ALERTA" if result["temperature_alert"] or result["pressure_alert"] else "NORMAL"
            self.monitor.record_event(
                service_name="FisicoService",
                latency_ms=latency_ms,
                status=status
            )

            self.queue.task_done()

    def handle_result(self, result: Dict[str, Any]):
        """
        Maneja el resultado del análisis y envía alerta si hay anomalía.
        """
        if result["temperature_alert"] or result["pressure_alert"]:
            alert_event = {
                "sample_id": result["sample_id"],
                "temperature": result.get("temperature"),
                "pressure": result.get("pressure"),
                "message": "Parámetros físicos fuera de rango"
            }
            send_alert(alert_event)
        else:
            logger.info(f"Resultado normal: {result}")