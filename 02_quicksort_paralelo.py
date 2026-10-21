# 02_quicksort_paralelo.py
# Computação Paralela e Concorrente — Aulas 09
# Parallel QuickSort com Particionamento Inicial em Processos

import time
import random
import math
from concurrent.futures import ProcessPoolExecutor

def quicksort_seq(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort_seq(left) + middle + quicksort_seq(right)

def parallel_quicksort(arr, num_workers=4):
    if len(arr) <= 10000:
        return quicksort_seq(arr)

    chunk_size = math.ceil(len(arr) / num_workers)
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        sorted_chunks = list(executor.map(quicksort_seq, chunks))

    def merge_two(left, right):
        res = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                res.append(left[i]); i += 1
            else:
                res.append(right[j]); j += 1
        res.extend(left[i:]); res.extend(right[j:])
        return res

    while len(sorted_chunks) > 1:
        next_chunks = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                next_chunks.append(merge_two(sorted_chunks[i], sorted_chunks[i + 1]))
            else:
                next_chunks.append(sorted_chunks[i])
        sorted_chunks = next_chunks

    return sorted_chunks[0]

if __name__ == '__main__':
    N = 500_000
    print(f"=== BENCHMARK QUICKSORT PARALELO (N = {N:,}) ===")
    dados = [random.randint(1, 5_000_000) for _ in range(N)]

    t_start = time.perf_counter()
    res_seq = quicksort_seq(dados.copy())
    t_seq = time.perf_counter() - t_start
    print(f"[Sequencial] Tempo: {t_seq:.4f}s")

    t_start = time.perf_counter()
    res_par = parallel_quicksort(dados, num_workers=4)
    t_par = time.perf_counter() - t_start
    speedup = t_seq / t_par if t_par > 0 else 0
    print(f"[Paralelo 4 Cores] Tempo: {t_par:.4f}s | Speedup: {speedup:.2f}x")

    assert res_seq == res_par, "Erro na ordenação!"
    print("Validação: Ordenação paralela validada com sucesso!")
