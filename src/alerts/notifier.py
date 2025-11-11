import logging
import smtplib
from email.mime.text import MIMEText
from typing import Dict
from src.config.settings import ALERT_CHANNEL

# Configuración del logger
logger = logging.getLogger("Notifier")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def send_alert(event: Dict[str, str]):
    """
    Envía una alerta según el canal configurado (email, webhook, log).
    """
    try:
        if ALERT_CHANNEL == "email":
            _send_email(event)
        elif ALERT_CHANNEL == "webhook":
            _send_webhook(event)
        elif ALERT_CHANNEL == "log":
            logger.warning(f"[ALERTA] Evento crítico: {event}")
        else:
            logger.error(f"Canal de alerta no soportado: {ALERT_CHANNEL}")
    except Exception as e:
        logger.error(f"Error al enviar alerta: {e}")

def _send_email(event: Dict[str, str]):
    """
    Envía alerta por correo electrónico (simulación).
    """
    try:
        msg = MIMEText(f"Se ha detectado un evento crítico:\n{event}")
        msg["Subject"] = "Alerta crítica - Sistema Umbrella"
        msg["From"] = "alertas@umbrella.com"
        msg["To"] = "destinatario@umbrella.com"

        # Simulación de envío (en producción usar credenciales seguras)
        with smtplib.SMTP("localhost") as server:
            server.send_message(msg)

        logger.info(f"Alerta enviada por email: {event}")
    except Exception as e:
        logger.error(f"Error al enviar email: {e}")

def _send_webhook(event: Dict[str, str]):
    """
    Envía alerta a un webhook (simulación).
    """
    try:
        # Aquí iría la lógica real con requests.post(url, json=event)
        logger.info(f"Alerta enviada a webhook: {event}")
    except Exception as e:
        logger.error(f"Error al enviar webhook: {e}")