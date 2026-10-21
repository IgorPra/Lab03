# 05_benchmark_ordenacao.py
# Benchmark Completo dos Algoritmos de Ordenação Paralelos e Seriais
# Computação Paralela e Concorrente (UNIFOR)

import time
import random
import os
import math
from concurrent.futures import ProcessPoolExecutor

def merge(left, right):
    res, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:]); res.extend(right[j:])
    return res

def merge_sort_seq(arr):
    if len(arr) <= 1: return arr
    m = len(arr) // 2
    return merge(merge_sort_seq(arr[:m]), merge_sort_seq(arr[m:]))

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
    cores = os.cpu_count() or 4
    tamanhos = [10000, 100000, 500000, 1000000, 2000000]

    print("=========================================================")
    print(f" BENCHMARK DE ORDENACAO PARALELA - SISTEMA ({cores} CORES)")
    print("=========================================================\n")

    for N in tamanhos:
        dados = [random.randint(1, 10000000) for _ in range(N)]

        # Serial
        t0 = time.perf_counter()
        res_seq = merge_sort_seq(dados.copy())
        t_seq = time.perf_counter() - t0

        # Paralelo
        t0 = time.perf_counter()
        res_par = parallel_merge_sort(dados, num_workers=cores)
        t_par = time.perf_counter() - t0

        speedup = t_seq / t_par if t_par > 0 else 0
        eficiencia = (speedup / cores) * 100

        print(f"Tamanho N = {N:,}:")
        print(f" - Tempo Serial   : {t_seq:.4f} s")
        print(f" - Tempo Paralelo : {t_par:.4f} s")
        print(f" - Speedup        : {speedup:.2f}x")
        print(f" - Eficiencia     : {eficiencia:.1f}%\n")
