# Problema 3: Comparação de Odd-Even Sort vs MergeSort em CPU (N = 50.000)

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

def odd_even_sort_bloco(arr):
    n = len(arr)
    is_sorted = False
    while not is_sorted:
        is_sorted = True
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
    return arr

def parallel_odd_even_sort(arr, num_workers=4):
    chunk_size = math.ceil(len(arr) / num_workers)
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        sorted_chunks = list(executor.map(odd_even_sort_bloco, chunks))

    # Fases Par e Ímpar entre os blocos ordenados
    n_blocos = len(sorted_chunks)
    for fase in range(n_blocos):
        inicio = 1 if fase % 2 == 1 else 0
        for i in range(inicio, n_blocos - 1, 2):
            combinado = merge(sorted_chunks[i], sorted_chunks[i + 1])
            meio = len(sorted_chunks[i])
            sorted_chunks[i] = combinado[:meio]
            sorted_chunks[i + 1] = combinado[meio:]

    res = []
    for c in sorted_chunks:
        res.extend(c)
    return res

if __name__ == '__main__':
    N = 50_000
    print(f"=== PROBLEMA 3: ODD-EVEN SORT vs MERGESORT (N = {N}) ===")
    dados = [random.randint(1, 100_000) for _ in range(N)]

    t_start = time.perf_counter()
    res_merge = parallel_merge_sort(dados.copy(), num_workers=4)
    t_merge = time.perf_counter() - t_start
    print(f"[MergeSort Paralelo] Tempo: {t_merge:.4f}s")

    t_start = time.perf_counter()
    res_oddeven = parallel_odd_even_sort(dados.copy(), num_workers=4)
    t_oddeven = time.perf_counter() - t_start
    print(f"[Odd-Even Paralelo]  Tempo: {t_oddeven:.4f}s")

    assert res_merge == res_oddeven, "Erro na ordenação!"
    print("Validação: Resultados idênticos com sucesso!")
