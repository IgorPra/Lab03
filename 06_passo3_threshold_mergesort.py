# Passo 3: Ajuste Fino do Threshold no MergeSort

import time
import random
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

def parallel_merge_sort(arr, threshold, num_workers=4):
    if len(arr) <= threshold:
        return merge_sort_seq(arr)

    chunks = [arr[i:i + threshold] for i in range(0, len(arr), threshold)]

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
    thresholds = [100, 1000, 10000, 50000, 100000]
    dados = [random.randint(1, 10_000_000) for _ in range(N)]

    print(f"Teste de Threshold no MergeSort (N = {N})")
    melhor_tempo = float('inf')
    melhor_th = 0

    for THRESHOLD in thresholds:
        t_start = time.perf_counter()
        res = parallel_merge_sort(dados, THRESHOLD, num_workers=4)
        tempo = time.perf_counter() - t_start
        print(f"THRESHOLD = {THRESHOLD} -> Tempo: {tempo:.4f}s")

        if tempo < melhor_tempo:
            melhor_tempo = tempo
            melhor_th = THRESHOLD

    print(f"\nMenor tempo: {melhor_tempo:.4f}s com THRESHOLD = {melhor_th}")
