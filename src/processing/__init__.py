"""
Módulos de procesamiento concurrente.
"""
from .cpu_bound import factorial, heavy_matrix_multiplication, compute_primes
from .io_bound import simulate_network_call, batch_network_calls
from .orchestrator import run_orchestration
