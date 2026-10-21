# Problema 1: Ordenação Paralela de Logs de Transações Financeiras

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

def separar_baldes(dados):
    # 4 baldes: [0-250], [250-500], [500-750], [750-1000]
    b1, b2, b3, b4 = [], [], [], []
    for valor in dados:
        if valor < 250:
            b1.append(valor)
        elif valor < 500:
            b2.append(valor)
        elif valor < 750:
            b3.append(valor)
        else:
            b4.append(valor)
    return [b1, b2, b3, b4]

def bucket_sort_seq(dados):
    baldes = separar_baldes(dados)
    resultado = []
    for b in baldes:
        resultado.extend(merge_sort_seq(b))
    return resultado

def bucket_sort_paralelo(dados, num_workers=4):
    baldes = separar_baldes(dados)
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        baldes_ordenados = list(executor.map(merge_sort_seq, baldes))

    resultado = []
    for b in baldes_ordenados:
        resultado.extend(b)
    return resultado

if __name__ == '__main__':
    N = 1_000_000
    print(f"=== PROBLEMA 1: BUCKET SORT PARALELO (N = {N}) ===")
    transacoes = [random.uniform(0, 1000) for _ in range(N)]

    t_start = time.perf_counter()
    res_seq = bucket_sort_seq(transacoes)
    t_seq = time.perf_counter() - t_start
    print(f"[Sequencial] Tempo: {t_seq:.4f}s")

    t_start = time.perf_counter()
    res_par = bucket_sort_paralelo(transacoes, num_workers=4)
    t_par = time.perf_counter() - t_start

    speedup = t_seq / t_par if t_par > 0 else 0
    eficiencia = (speedup / 4) * 100
    print(f"[Paralelo 4 Cores] Tempo: {t_par:.4f}s | Speedup: {speedup:.2f}x | Eficiência: {eficiencia:.1f}%")

    assert res_seq == res_par, "Erro na ordenação!"
    print("Validação: Resultados idênticos com sucesso!")
