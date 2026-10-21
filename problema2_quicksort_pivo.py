# Problema 2: Impacto da Escolha do Pivô no QuickSort Paralelo
# Estratégias: (a) Primeiro Elemento vs (b) Mediana de Três

import time
import random
import sys
from concurrent.futures import ProcessPoolExecutor

sys.setrecursionlimit(20000)

def mediana_de_tres(arr):
    a = arr[0]
    b = arr[len(arr) // 2]
    c = arr[-1]
    return sorted([a, b, c])[1]

def quicksort_primeiro(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort_primeiro(left) + middle + quicksort_primeiro(right)

def quicksort_mediana(arr):
    if len(arr) <= 1:
        return arr
    pivot = mediana_de_tres(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort_mediana(left) + middle + quicksort_mediana(right)

def parallel_quicksort_pivo(arr, estrategia='primeiro', num_workers=4):
    if len(arr) <= 1:
        return arr

    if estrategia == 'primeiro':
        pivot = arr[0]
        func_seq = quicksort_primeiro
    else:
        pivot = mediana_de_tres(arr)
        func_seq = quicksort_mediana

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        fut_left = executor.submit(func_seq, left)
        fut_right = executor.submit(func_seq, right)
        res_left = fut_left.result()
        res_right = fut_right.result()

    return res_left + middle + res_right

if __name__ == '__main__':
    N = 5000
    print(f"=== PROBLEMA 2: IMPACTO DO PIVO NO QUICKSORT PARALELO (N = {N}) ===")

    # Vetor parcialmente ordenado (90% ordenado, apenas o final embaralhado)
    dados = list(range(N))
    for _ in range(200):
        i = random.randint(int(N * 0.9), N - 1)
        j = random.randint(int(N * 0.9), N - 1)
        dados[i], dados[j] = dados[j], dados[i]

    # (a) Primeiro Elemento
    t_start = time.perf_counter()
    res_a = parallel_quicksort_pivo(dados.copy(), estrategia='primeiro')
    t_a = time.perf_counter() - t_start
    print(f"[Pivo: Primeiro Elemento] Tempo: {t_a:.4f}s")

    # (b) Mediana de Três
    t_start = time.perf_counter()
    res_b = parallel_quicksort_pivo(dados.copy(), estrategia='mediana')
    t_b = time.perf_counter() - t_start
    print(f"[Pivo: Mediana de Tres]   Tempo: {t_b:.4f}s")

    assert res_a == res_b == sorted(dados), "Erro na ordenação!"
    print("Validação: Resultados idênticos com sucesso!")
