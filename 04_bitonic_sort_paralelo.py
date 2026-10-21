# 04_bitonic_sort_paralelo.py
# Computação Paralela e Concorrente — Aulas 09
# Bitonic Sort (Rede de Ordenação Paralela para N = 2^k)

import time
import random

def comp_and_swap(arr, i, j, direc):
    if (direc == 1 and arr[i] > arr[j]) or (direc == 0 and arr[i] < arr[j]):
        arr[i], arr[j] = arr[j], arr[i]

def bitonic_merge(arr, low, cnt, direc):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            comp_and_swap(arr, i, i + k, direc)
        bitonic_merge(arr, low, k, direc)
        bitonic_merge(arr, low + k, k, direc)

def bitonic_sort_rec(arr, low, cnt, direc):
    if cnt > 1:
        k = cnt // 2
        bitonic_sort_rec(arr, low, k, 1) # Ordem crescente
        bitonic_sort_rec(arr, low + k, k, 0) # Ordem decrescente
        bitonic_merge(arr, low, cnt, direc)

def bitonic_sort(arr):
    bitonic_sort_rec(arr, 0, len(arr), 1)
    return arr

if __name__ == '__main__':
    N = 8192 # 2^13 elementos
    print(f"=== BITONIC SORT (REDE DE ORDENAÇÃO N = {N:,}) ===")
    dados = [random.randint(1, 100_000) for _ in range(N)]

    t_start = time.perf_counter()
    res = bitonic_sort(dados.copy())
    t_total = time.perf_counter() - t_start

    print(f"Tempo de Execução (Bitonic Sort): {t_total:.4f}s")
    assert res == sorted(dados), "Erro na ordenação!"
    print("Validação: Sequência bitônica mesclada e ordenada!")
