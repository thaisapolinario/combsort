import random # gera listas com números aleatórios
import time # mede o tempo de execução
import tracemalloc # verifica o uso de memória
import sys # aumenta o limite de recursão 
import csv
import os

NOME_PASTA = "../DADOS"
FICHEIRO_TEMPO_MEMORIA = "analise_1_tempo_memoria.csv"
FICHEIRO_TIPOS_ENTRADA = "analise_2_tipos_entrada_combsort.csv"
FICHEIRO_COMPARATIVO = "analise_3_comparativa_algoritmos.csv"

def novo_intervalo(intervalo):
    intervalo = (intervalo * 10)//13
    if intervalo < 1:
        return 1
    return intervalo

def combsort (lista):

    tamanho = len(lista)
    intervalo = tamanho

    troca = True

    while intervalo !=1 or troca:

        intervalo = novo_intervalo(intervalo)

        troca = False

        for i in range(0, tamanho-intervalo):
            if lista[i] > lista[i + intervalo]:
                lista[i], lista[i + intervalo]=lista[i + intervalo], lista[i]
                troca = True
    return lista
                
def bubble_sort(lista):

    tamanho_lista = len(lista)
    for i in range(tamanho_lista):
        troca = False
        for j in range(0, tamanho_lista - i - 1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
                troca = True
        if not troca:
            break

    return lista

def tim_sort(lista):
    lista.sort()
    return lista


def insertion_sort(lista):
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and chave < lista[j]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
    return lista

def selection_sort(lista):
    for i in range(len(lista)):
        idx_minimo = i
        for j in range(i + 1, len(lista)):
            if lista[j] < lista[idx_minimo]:
                idx_minimo = j
        lista[i], lista[idx_minimo] = lista[idx_minimo], lista[i]
    return lista


def gerar_lista_aleatoria(tamanho):
    return [random.randint(0, tamanho) for _ in range(tamanho)]

def gerar_lista_ordenada(tamanho):
    return list(range(tamanho))

def gerar_lista_invertida(tamanho):
    return list(range(tamanho, 0, -1))

def salvar_em_csv(nome_ficheiro, cabecalho, linha_dados):
    caminho_completo = os.path.join(NOME_PASTA, nome_ficheiro)
    escrever_cabecalho = not os.path.exists(caminho_completo)
    
    try:
        with open(caminho_completo, 'a', newline='', encoding='utf-8') as f:
            escritor_csv = csv.writer(f)
            if escrever_cabecalho:
                escritor_csv.writerow(cabecalho)
            escritor_csv.writerow(linha_dados)
    except IOError as e:
        print(f"\n>>> Erro ao salvar linha no CSV '{caminho_completo}': {e}\n")

# Análises 1 e 3
def executar_analise_tempo_memoria(tamanho_entrada):
    cabecalho = ['Tamanho_N', 'Tempo_Execucao_s']
    lista_aleatoria = gerar_lista_aleatoria(tamanho_entrada)
    inicio = time.perf_counter()
    combsort(lista_aleatoria)
    fim = time.perf_counter()
    tempo_execucao = fim - inicio
    salvar_em_csv(FICHEIRO_TEMPO_MEMORIA, cabecalho, [tamanho_entrada, tempo_execucao ])

    lista_para_memoria = gerar_lista_aleatoria(tamanho_entrada)
    tracemalloc.start()
    combsort(lista_para_memoria)
    memoria_pico = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    tempo_formatado = f'{tempo_execucao:.8f}'
    salvar_em_csv(FICHEIRO_TEMPO_MEMORIA, cabecalho, [tamanho_entrada, memoria_pico])
    

# Análise 2
def analise_diferentes_entradas(tamanho_lista):
    cabecalho = ['Tamanho_N', 'Cenario', 'Tempo_Execucao_s']
    cenarios = {
        "Caso Médio (Aleatoria)": gerar_lista_aleatoria,
        "Melhor Caso (Ordenada)": gerar_lista_ordenada,
        "Pior Caso (Invertida)": gerar_lista_invertida
    }

    for nome_cenario, func_geradora in cenarios.items():
        lista_teste = func_geradora(tamanho_lista)
        inicio = time.perf_counter()
        combsort(lista_teste)
        fim = time.perf_counter()
        tempo_execucao = fim - inicio
        tempo_formatado = f'{tempo_execucao:.8f}'
        salvar_em_csv(FICHEIRO_TIPOS_ENTRADA, cabecalho, [tamanho_lista, nome_cenario, tempo_execucao])


# Análise 4
def analise_comparativa(tamanho_lista):
    cabecalho = ['Tamanho_N', 'Cenario', 'Algoritmo', 'Tempo_Execucao_s']

    algoritmos = {
        "Comb Sort": combsort,
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort
    }
    

    cenarios = {
        "Lista Não Ordenada (Caso Médio)": gerar_lista_aleatoria,
        "Lista Já Ordenada (Melhor Caso)": gerar_lista_ordenada,
        "Lista Invertida (Pior Caso)": gerar_lista_invertida
    }

    for nome_cenario, func_geradora in cenarios.items():
        lista_original = func_geradora(tamanho_lista)
        
        for nome_algo, func_algo in algoritmos.items():
            lista_para_ordenar = lista_original.copy()
            
            inicio = time.perf_counter()
            func_algo(lista_para_ordenar)
            fim = time.perf_counter()
            tempo_execucao = fim - inicio
            tempo_formatado = f'{tempo_execucao:.8f}'
            
            salvar_em_csv(FICHEIRO_COMPARATIVO, cabecalho, [tamanho_lista, nome_cenario, nome_algo, tempo_formatado])
            




def salvar_linha_csv(dados_linha):
    """
    Adiciona uma única linha de dados ao ficheiro CSV consolidado.
    Cria o ficheiro e o cabeçalho se não existirem.
    """
    nome_pasta = "DADOS"
    nome_ficheiro = "resultados_analises.csv"
    caminho_completo = os.path.join(nome_pasta, nome_ficheiro)
    os.makedirs(nome_pasta, exist_ok=True)
    
    # Verifica se o ficheiro já existe para decidir se escreve o cabeçalho
    ficheiro_existe = os.path.isfile(caminho_completo)
    
    try:
        with open(caminho_completo, 'a', newline='', encoding='utf-8') as f:
            escritor_csv = csv.writer(f)
            if not ficheiro_existe:
                escritor_csv.writerow(['Timestamp', 'Tamanho_N', 'Cenario', 'Algoritmo', 'Metrica', 'Valor', 'Unidade'])
            escritor_csv.writerow(dados_linha)
    except IOError as e:
        print(f"\n>>> Erro ao salvar a linha no CSV: {e}\n")

def menu_principal():
    os.makedirs(NOME_PASTA, exist_ok=True)
    
    while True:
        print("\n" + "="*60)
        print(" ESCOLHA UMA ANÁLISE: ")
        print("="*60)
        print("1. Análise de Tempo e Memória")
        print("2. Análise por Tipo de Entrada")
        print("3. Análise Comparativa")
        print("4. Sair")
        print("-" * 60)
        
        escolha = input("Digite o número da sua escolha: ")

        if escolha == '4':
            print("FIM.")
            break
        
        if escolha in ['1', '2', '3']:
            try:
                n_inicial_str = input("Digite o N inicial (ex: 10): ")
                num_passos_str = input("Digite o número de passos (ex: 4 para ir até 10.000): ")
                n_inicial = int(n_inicial_str)
                num_passos = int(num_passos_str)
            except ValueError:
                print("\nErro: Digite um número válido")
                continue

            analises = {
                '1': (executar_analise_tempo_memoria, FICHEIRO_TEMPO_MEMORIA),
                '2': (analise_diferentes_entradas, FICHEIRO_TIPOS_ENTRADA),
                '3': (analise_comparativa, FICHEIRO_COMPARATIVO)
            }
            
            funcao_analise, nome_ficheiro = analises[escolha]
            caminho_ficheiro = os.path.join(NOME_PASTA, nome_ficheiro)

 
            tamanho_atual_n = n_inicial
            for i in range(num_passos):
                funcao_analise(tamanho_atual_n)
                tamanho_atual_n *= 10
            
            
        else:
            print("\nErro: Digite um número válido")


if __name__ == "__main__":
    menu_principal()