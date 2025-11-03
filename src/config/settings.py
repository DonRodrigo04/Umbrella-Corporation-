# src/config/settings.py
import os
from pathlib import Path
# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración general
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

# Configuración de flujos de datos
DATA_SOURCES = {
    "genetico": os.getenv("GENETICO_SOURCE", "stream/genetico"),
    "bioquimico": os.getenv("BIOQUIMICO_SOURCE", "stream/bioquimico"),
    "fisico": os.getenv("FISICO_SOURCE", "stream/fisico"),
}

# Parámetros de procesamiento
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 4))
PROCESS_POOL_SIZE = int(os.getenv("PROCESS_POOL_SIZE", 2))
THREAD_POOL_SIZE = int(os.getenv("THREAD_POOL_SIZE", 4))

# Alertas
CRITICAL_THRESHOLD = float(os.getenv("CRITICAL_THRESHOLD", 0.9))
ALERT_CHANNEL = os.getenv("ALERT_CHANNEL", "email")  # email, webhook, etc.

# Métricas
METRICS_ENABLED = os.getenv("METRICS_ENABLED", "true").lower() == "true"
METRICS_INTERVAL = int(os.getenv("METRICS_INTERVAL", 10))  # segundos
# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = BASE_DIR / "logs"

# Otros
TIMEZONE = os.getenv("TIMEZONE", "UTC")

# Validación de configuración
def validate_settings():
    errors = []

    if ENVIRONMENT not in ["development", "production", "staging"]:
        errors.append(f"ENVIRONMENT inválido: {ENVIRONMENT}")

    if MAX_WORKERS <= 0:
        errors.append("MAX_WORKERS debe ser mayor que 0")

    if PROCESS_POOL_SIZE <= 0:
        errors.append("PROCESS_POOL_SIZE debe ser mayor que 0")

    if THREAD_POOL_SIZE <= 0:
        errors.append("THREAD_POOL_SIZE debe ser mayor que 0")

    if not (0.0 <= CRITICAL_THRESHOLD <= 1.0):
        errors.append("CRITICAL_THRESHOLD debe estar entre 0.0 y 1.0")

    if ALERT_CHANNEL not in ["email", "webhook", "log"]:
        errors.append(f"ALERT_CHANNEL no soportado: {ALERT_CHANNEL}")

    if METRICS_INTERVAL <= 0:
        errors.append("METRICS_INTERVAL debe ser mayor que 0")

    if errors:
        raise ValueError("Errores en configuración:\n" + "\n".join(errors))

# Ejecutar validación al importar
validate_settings()