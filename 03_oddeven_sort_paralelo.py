# 03_oddeven_sort_paralelo.py
# Computação Paralela e Concorrente — Aulas 09
# Odd-Even Transposition Sort (Bubble Sort Paralelo em Fases Par/Ímpar)

import time
import random

def odd_even_sort_seq(arr):
    n = len(arr)
    is_sorted = False
    while not is_sorted:
        is_sorted = True
        # Fase Ímpar (Odd)
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
        # Fase Par (Even)
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
    return arr

if __name__ == '__main__':
    N = 5_000
    print(f"=== ODD-EVEN TRANSPOSITION SORT (N = {N:,}) ===")
    dados = [random.randint(1, 100_000) for _ in range(N)]

    t_start = time.perf_counter()
    res = odd_even_sort_seq(dados.copy())
    t_total = time.perf_counter() - t_start

    print(f"Tempo de Execução (Odd-Even): {t_total:.4f}s")
    assert res == sorted(dados), "Erro na ordenação!"
    print("Validação: Array ordenado corretamente!")
