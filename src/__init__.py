"""
Umbrella Data Analysis Package
Este paquete implementa un sistema concurrente para análisis de datos biológicos.
Incluye servicios, procesamiento, alertas, métricas y utilidades.
"""

# Exponer clases principales
from .services.genetico_service import GeneticoService
from .services.bioquimico_service import BioquimicoService
from .services.fisico_service import FisicoService

# Exponer funciones de procesamiento
from .processing.cpu_bound import factorial, heavy_matrix_multiplication, compute_primes
from .processing.io_bound import simulate_network_call, batch_network_calls
from .processing.orchestrator import run_orchestration

# Exponer utilidades
from .utils.normalizer import normalize_data
from .alerts.notifier import send_alert

# Exponer configuración
from .config.settings import DATA_SOURCES, PROCESS_POOL_SIZE