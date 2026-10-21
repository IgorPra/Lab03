# 01_mergesort_paralelo.py
# Computação Paralela e Concorrente — Aulas 09
# Parallel MergeSort com Particionamento e Redução por Árvore

import time
import random
import math
from concurrent.futures import ProcessPoolExecutor

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_seq(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    return merge(merge_sort_seq(arr[:mid]), merge_sort_seq(arr[mid:]))

def parallel_merge_sort(arr, num_workers=4):
    if len(arr) <= 10000:
        return merge_sort_seq(arr)
    chunk_size = math.ceil(len(arr) / num_workers)
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        sorted_chunks = list(executor.map(merge_sort_seq, chunks))
    while len(sorted_chunks) > 1:
        next_chunks = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                next_chunks.append(merge(sorted_chunks[i], sorted_chunks[i + 1]))
            else:
                next_chunks.append(sorted_chunks[i])
        sorted_chunks = next_chunks
    return sorted_chunks[0]

if __name__ == '__main__':
    N = 1_000_000
    print(f"=== BENCHMARK MERGESORT PARALELO (N = {N:,}) ===")
    dados = [random.randint(1, 10_000_000) for _ in range(N)]

    # 1. Execução Sequencial
    t_start = time.perf_counter()
    res_seq = merge_sort_seq(dados.copy())
    t_seq = time.perf_counter() - t_start
    print(f"[Sequencial] Tempo: {t_seq:.4f}s")

    # 2. Execução Paralela (4 Cores)
    t_start = time.perf_counter()
    res_par = parallel_merge_sort(dados, num_workers=4)
    t_par = time.perf_counter() - t_start
    speedup = t_seq / t_par if t_par > 0 else 0
    eficiencia = (speedup / 4) * 100
    print(f"[Paralelo 4 Cores] Tempo: {t_par:.4f}s | Speedup: {speedup:.2f}x | Eficiência: {eficiencia:.1f}%")

    assert res_seq == res_par, "Erro: Inconsistência nos resultados!"
    print("Validação: Resultados idênticos com sucesso!")
