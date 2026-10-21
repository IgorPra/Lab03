# Problema 4: Cálculo da Carga Ociosa (Work Load Idle Time) no MergeSort

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

def worker_merge_sort(chunk):
    t_ini = time.perf_counter()
    ordenado = merge_sort_seq(chunk)
    t_fim = time.perf_counter()
    return ordenado, (t_fim - t_ini), t_fim

def parallel_merge_sort_idle(arr, num_workers=4):
    t_inicio_total = time.perf_counter()

    chunk_size = math.ceil(len(arr) / num_workers)
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

    sorted_chunks = []
    tempos_ativos = []
    tempos_espera = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker_merge_sort, c) for c in chunks]

        for i, fut in enumerate(futures):
            ordenado, t_ativo, t_fim_worker = fut.result()
            t_apos_result = time.perf_counter()

            espera = max(0.0, t_apos_result - t_fim_worker)
            sorted_chunks.append(ordenado)
            tempos_ativos.append(t_ativo)
            tempos_espera.append(espera)
            print(f"Worker {i}: tempo ativo = {t_ativo:.4f}s | espera no .result() = {espera:.4f}s")

    while len(sorted_chunks) > 1:
        next_chunks = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                next_chunks.append(merge(sorted_chunks[i], sorted_chunks[i + 1]))
            else:
                next_chunks.append(sorted_chunks[i])
        sorted_chunks = next_chunks

    t_total = time.perf_counter() - t_inicio_total

    # Tempo ocioso de cada worker em relação ao tempo total
    ociosos = [t_total - ativo for ativo in tempos_ativos]
    media_ocioso = sum(ociosos) / num_workers
    porcentagem_ociosa = (media_ocioso / t_total) * 100
    porcentagem_espera_result = (sum(tempos_espera) / num_workers / t_total) * 100

    print(f"\nTempo total de execução: {t_total:.4f}s")
    print(f"Tempo médio esperando .result(): {sum(tempos_espera)/num_workers:.4f}s ({porcentagem_espera_result:.2f}%)")
    print(f"Tempo médio ocioso total por worker: {media_ocioso:.4f}s ({porcentagem_ociosa:.2f}%)")

    return sorted_chunks[0]

if __name__ == '__main__':
    N = 1_000_000
    print(f"=== PROBLEMA 4: CARGA OCIOSA NO MERGESORT (N = {N}) ===")
    dados = [random.randint(1, 10_000_000) for _ in range(N)]

    res = parallel_merge_sort_idle(dados, num_workers=4)
    assert res == sorted(dados), "Erro na ordenação!"
    print("Validação: Resultados idênticos com sucesso!")
