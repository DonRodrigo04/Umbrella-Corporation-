"""
io_bound.py
Funciones para simular tareas I/O-bound (asyncio y ThreadPoolExecutor).
"""
import asyncio
import logging
from typing import List

# Configuración del logger
logger = logging.getLogger("IOBound")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

async def simulate_network_call(url: str) -> str:
    """Simula una llamada de red asíncrona."""
    logger.info(f"Simulando llamada a {url}")
    await asyncio.sleep(1)  # Simula latencia
    return f"Respuesta simulada de {url}"

async def read_file_async(file_path: str) -> str:
    """Lee un archivo de forma asíncrona (simulación)."""
    logger.info(f"Leyendo archivo: {file_path}")
    await asyncio.sleep(0.5)
    return f"Contenido simulado de {file_path}"

async def write_file_async(file_path: str, content: str) -> None:
    """Escribe contenido en un archivo de forma asíncrona (simulación)."""
    logger.info(f"Escribiendo en archivo: {file_path}")
    await asyncio.sleep(0.5)
    logger.info("Escritura completada")

async def batch_network_calls(urls: List[str]) -> List[str]:
    """Realiza múltiples llamadas de red concurrentes usando asyncio.gather."""
    tasks = [simulate_network_call(url) for url in urls]
    return await asyncio.gather(*tasks)