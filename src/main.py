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

def monte_carlo_pi_partial(n_points: int) -> int:
    inside_circle = 0
    for _ in range(n_points):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1
    return inside_circle

def monte_carlo_concurrent(n_points: int, n_workers: int = 4) -> tuple[float, float]:
    points_per_worker = n_points // n_workers
    start = timer()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = executor.map(monte_carlo_pi_partial, [points_per_worker] * n_workers)

    inside_circle = sum(results)
    return (inside_circle / n_points) * 4, timer() - start


# Testando com 100 milhões de pontos
number_of_points = 100_000_000

print("=====Resultado para Sequêncial=====")
pi_value, duration = monte_carlo_seq(number_of_points)
print(f"Valor de PI calculado para {number_of_points} pontos -> {pi_value}\nTempo total: {duration} segundos")

print("=====Resultado para Concorrência=====")
pi_value, duration = monte_carlo_concurrent(number_of_points)
print(f"Valor de PI calculado para {number_of_points} pontos -> {pi_value}\nTempo total: {duration} segundos")