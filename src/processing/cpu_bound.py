"""
cpu_bound.py
Funciones para simular tareas intensivas en CPU (multiproceso).
"""
import math
import logging
from typing import List

logger = logging.getLogger("CPUBound")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def factorial(n: int) -> int:
    """Calcula el factorial de n usando recursión (simulación de carga pesada)."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def heavy_matrix_multiplication(size: int) -> List[List[int]]:
    """Simula multiplicación de matrices cuadradas de tamaño 'size'."""
    logger.info(f"Iniciando multiplicación de matrices de tamaño {size}x{size}")
    A = [[i + j for j in range(size)] for i in range(size)]
    B = [[i * j for j in range(size)] for i in range(size)]
    result = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += A[i][k] * B[k][j]
    logger.info("Multiplicación completada")
    return result

def compute_primes(limit: int) -> List[int]:
    """Calcula números primos hasta 'limit' (simulación CPU-bound)."""
    logger.info(f"Calculando números primos hasta {limit}")
    primes = []
    for num in range(2, limit + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    logger.info("Cálculo de primos completado")
    return primes