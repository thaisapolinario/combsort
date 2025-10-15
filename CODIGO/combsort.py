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

    num_comparacoes = 0 


    troca = True

    while intervalo !=1 or troca:

        intervalo = novo_intervalo(intervalo)

        troca = False

        for i in range(0, tamanho-intervalo):
            num_comparacoes += 1
            if lista[i] > lista[i + intervalo]:
                lista[i], lista[i + intervalo]=lista[i + intervalo], lista[i]
                troca = True
    return lista, num_comparacoes
                
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
        print(f"\nErro ao salvar linha no CSV '{caminho_completo}': {e}\n")

# Análises 1 e 3
def executar_analise_tempo_memoria(tamanho_entrada):
    cabecalho_metrica = ['Tamanho_N', 'Metrica', 'Valor']
    
    lista_aleatoria = gerar_lista_aleatoria(tamanho_entrada)
    inicio = time.perf_counter()
    combsort(lista_aleatoria) 
    fim = time.perf_counter()
    tempo_execucao = fim - inicio
    
    salvar_em_csv(FICHEIRO_TEMPO_MEMORIA, cabecalho_metrica, [tamanho_entrada, 'Tempo_Execucao_s', tempo_execucao]) 

    tracemalloc.start()
    
    lista_para_memoria = gerar_lista_aleatoria(tamanho_entrada) 
    
    combsort(lista_para_memoria)
    
    memoria_pico = tracemalloc.get_traced_memory()[1] 
    tracemalloc.stop()
    
    salvar_em_csv(FICHEIRO_TEMPO_MEMORIA, cabecalho_metrica, [tamanho_entrada, 'Memoria_Pico_Bytes', memoria_pico])

# Análise 2
def analise_diferentes_entradas(tamanho_lista):
    cabecalho = ['Tamanho_N', 'Cenario', 'Num_Comparacoes', 'Tempo_Execucao_s']
    
    cenarios = {
        "Caso Médio (Aleatoria)": gerar_lista_aleatoria,
        "Melhor Caso (Ordenada)": gerar_lista_ordenada,
        "Pior Caso (Invertida)": gerar_lista_invertida
    }

    for nome_cenario, funcao_geradora in cenarios.items():
        lista_teste = funcao_geradora(tamanho_lista)
        
        _, num_comparacoes = combsort(lista_teste) 
        inicio = time.perf_counter()
        _, num_comparacoes = combsort(lista_teste) 
        fim = time.perf_counter()
        tempo_execucao = fim - inicio
        
        # Salva o número de comparações no CSV
        salvar_em_csv(FICHEIRO_TIPOS_ENTRADA, cabecalho, [tamanho_lista, nome_cenario, num_comparacoes, tempo_execucao])


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
    }

    for nome_cenario, funcao_geradora in cenarios.items():
        lista_original = funcao_geradora(tamanho_lista)
        
        for nome_algoritmo, funcao_algoritmo in algoritmos.items():
            lista_para_ordenar = lista_original.copy()
            
            inicio = time.perf_counter()
            funcao_algoritmo(lista_para_ordenar)
            fim = time.perf_counter()
            tempo_execucao = fim - inicio
            tempo_formatado = f'{tempo_execucao:.8f}'
            
            salvar_em_csv(FICHEIRO_COMPARATIVO, cabecalho, [tamanho_lista, nome_cenario, nome_algoritmo, tempo_formatado])
            

def menu_principal():
    os.makedirs(NOME_PASTA, exist_ok=True)
    
    # Define o passo de 5.000 fixo para a Progressão Aritmética
    PASSO_INCREMENTO = 5000
    LIMITE_ALTA_RESOLUCAO = 100000
    
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
                inicio = input("Digite o N inicial (ex: 10): ")
                num_passos_str = input("Digite o número de passos: ")
                
                n_inicial = int(inicio)
                passos_log = int(num_passos_str)
                
                if n_inicial <= 0 or passos_log <= 0:
                    print("\nErro: N deve ser positivo e o número de passos deve ser maior que zero.")
                    continue
                
            except ValueError:
                print("\nErro: Digite um número inteiro válido.")
                continue

            analises = {
                '1': (executar_analise_tempo_memoria, FICHEIRO_TEMPO_MEMORIA),
                '2': (analise_diferentes_entradas, FICHEIRO_TIPOS_ENTRADA),
                '3': (analise_comparativa, FICHEIRO_COMPARATIVO)
            }
            
            funcao_analise, nome_ficheiro = analises[escolha]
            caminho_ficheiro = os.path.join(NOME_PASTA, nome_ficheiro)

            if os.path.exists(caminho_ficheiro):
                os.remove(caminho_ficheiro)
                print(f"\nAVISO: Arquivo de dados antigo '{nome_ficheiro}' foi removido para garantir uma nova análise limpa.")

            
            tamanho_atual_n = n_inicial
            
            while tamanho_atual_n <= LIMITE_ALTA_RESOLUCAO:
                print(f"-> Executando N = {tamanho_atual_n}")
                funcao_analise(tamanho_atual_n)
                
                if tamanho_atual_n < PASSO_INCREMENTO:
                    tamanho_atual_n = PASSO_INCREMENTO
                else:
                    tamanho_atual_n += PASSO_INCREMENTO
            
            tamanho_atual_n = 100000 
            
            for i in range(passos_log):
                print(f"-> Executando N = {tamanho_atual_n}")
                funcao_analise(tamanho_atual_n)
                tamanho_atual_n *= 10
            
            
        else:
            print("\nErro: Digite um número válido")


if __name__ == "__main__":
    menu_principal()