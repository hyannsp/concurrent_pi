import random
from timeit import default_timer as timer
import concurrent.futures

def monte_carlo_seq(n_points: int) -> tuple[float, float]:
    inside_circle = 0
    start = timer()
    for _ in range(n_points):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if x**2 + y**2 <= 1:  # Verifica se está dentro do círculo
            inside_circle += 1

    return (inside_circle / n_points) * 4, timer() - start

def monte_carlo_worker(n_points: int) -> int:
    # Função auxiliar para calcular parte do Monte Carlo.
    inside_circle = 0
    for _ in range(n_points):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1
    return inside_circle

def monte_carlo_concurrent(n_points: int, n_workers: int = 4) -> tuple[float, float]:
    points_per_worker = n_points // n_workers
    start = timer()

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_workers) as executor:
        results = executor.map(monte_carlo_worker, [points_per_worker] * n_workers)

    inside_circle = sum(results)
    return (inside_circle / n_points) * 4, timer() - start


# Testando com 1, 10 e 100 milhões de pontos
number_of_points = [1_000_000,10_000_000, 100_000_000]

for total_points in number_of_points:
    print("===== Realizando Sequencial =====")
    pi_value, duration = monte_carlo_seq(total_points)
    print(f"Valor de π calculado para {format(total_points, '_').replace('_', '.')} pontos -> {pi_value}\nTempo total: {duration} segundos")

    print("===== Realizando Concorrência =====")
    pi_value, duration = monte_carlo_concurrent(total_points)
    print(f"Valor de π calculado para {format(total_points, '_').replace('_', '.')} pontos -> {pi_value}\nTempo total: {duration} segundos")
    print("________________________________________________________________________")
