# Relatório - Laboratório 03: Ordenação Paralela

## Passo 2: Análise de Sensibilidade ao Tamanho do Array (N)

Tabela 1 preenchida com os resultados obtidos no script `05_benchmark_ordenacao.py` (8 núcleos):

| Tamanho (N) | Tempo Serial (s) | Tempo Paralelo (s) | Speedup (S) | Eficiência (E%) |
| --- | --- | --- | --- | --- |
| 10.000 | 0,0303 s | 0,0413 s | 0,73x | 9,20% |
| 100.000 | 0,3912 s | 0,3936 s | 0,99x | 12,40% |
| 500.000 | 1,9715 s | 0,9225 s | 2,14x | 26,70% |
| 1.000.000 | 4,5622 s | 1,8131 s | 2,52x | 31,50% |
| 2.000.000 | 12,4953 s | 3,7453 s | 3,34x | 41,70% |

**Observação:** Para vetores pequenos (10.000 e 100.000), o tempo de criar os processos e transferir as listas entre eles (overhead de IPC) faz com que a versão paralela seja mais lenta ou empate com a sequencial. O paralelismo passa a superar a execução sequencial a partir de **N = 500.000**.

---

## Passo 3: Ajuste Fino do Threshold no MergeSort

Testando N = 1.000.000 no script `06_passo3_threshold_mergesort.py`:

- THRESHOLD = 100: 4,9489 s
- THRESHOLD = 1.000: 2,5268 s
- THRESHOLD = 10.000: 2,4702 s
- THRESHOLD = 50.000: 2,0095 s
- THRESHOLD = 100.000: 2,5030 s

**Resultado:** O menor tempo global foi alcançado com **THRESHOLD = 50.000** (2,0095 s). Quando o threshold é muito baixo (ex: 100), o vetor é dividido em pedaços pequenos demais, gerando muito custo de comunicação entre processos. Já quando é grande demais (100.000), a divisão aproveita menos o paralelismo.

---

## Problemas e Desafios (Seção 4)

### Problema 1: Ordenação Paralela de Logs de Transações Financeiras
Arquivo: `problema1_bucket_sort_transacoes.py`

- Tempo Sequencial: 5,68 s
- Tempo Paralelo (4 cores): 1,71 s
- Speedup: 3,32x
- Eficiência: 83,0%

Como os dados foram separados em 4 faixas de valores independentes (`[0-250]`, `[250-500]`, `[500-750]`, `[750-1000]`), cada processo ordenou um balde e no final bastou concatenar as listas sem precisar intercalar (merge) elemento por elemento, gerando uma eficiência alta.

### Problema 2: Impacto da Escolha do Pivô no QuickSort Paralelo
Arquivo: `problema2_quicksort_pivo.py`

- Estratégia (a) Primeiro Elemento (N = 5.000 parcialmente ordenado): ~0,85 s
- Estratégia (b) Mediana de Três (N = 5.000 parcialmente ordenado): ~0,12 s

**Resposta:** Em um vetor já ordenado ou quase ordenado, escolher o primeiro elemento como pivô gera partições totalmente desbalanceadas (a lista de menores fica vazia e a de maiores fica com quase todos os elementos). Com isso, o trabalho não é dividido entre os processos: um único worker faz quase tudo sozinho enquanto os outros ficam parados, além de cair no pior caso do QuickSort, que é $O(N^2)$. A mediana de três escolhe um pivô mais próximo do meio e divide o trabalho de forma equilibrada entre os processos.

### Problema 3: Comparação de Odd-Even Sort vs MergeSort em CPU
Arquivo: `problema3_oddeven_vs_mergesort.py`

- MergeSort Paralelo (N = 50.000): ~0,32 s
- Odd-Even Sort Paralelo (N = 50.000): ~10,29 s

**Resposta:** O Odd-Even Sort compara e troca apenas elementos vizinhos, tendo complexidade $O(N^2)$, o que exige dezenas de milhões de trocas para N = 50.000, enquanto o MergeSort tem complexidade $O(N \log N)$. Na CPU, temos poucos núcleos e um custo alto para sincronizar processos a cada fase. Já nas GPUs, existem milhares de threads leves trabalhando em paralelo (SIMD) com sincronização rápida via hardware, onde todas as comparações de uma fase podem ser feitas de uma só vez.

### Problema 4: Cálculo da Carga Ociosa (Work Load Idle Time)
Arquivo: `problema4_carga_ociosa_mergesort.py`

Para N = 1.000.000 com 4 workers:
- Tempo total de execução: ~1,58 s
- Tempo ativo de cada worker: ~0,95 s
- Tempo médio esperando na sincronização (`.result()`): ~0,05 s (~3,5% do tempo total)
- Tempo ocioso total por worker (contando inicialização dos processos e a etapa de merge final que roda em um núcleo só): ~0,62 s (~39,5% do tempo total).
