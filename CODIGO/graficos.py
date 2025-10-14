import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.ticker import FuncFormatter

NOME_PASTA_DADOS = "../DADOS" 
NOME_PASTA_GRAFICOS = "../GRAFICOS"

# Nomes dos arquivos de entrada
FICHEIRO_1 = "analise_1_tempo_memoria.csv"
FICHEIRO_2 = "analise_2_tipos_entrada_combsort.csv"
FICHEIRO_3 = "analise_3_comparativa_algoritmos.csv"

os.makedirs(NOME_PASTA_GRAFICOS, exist_ok=True)

# 1. FUNÇÃO DE FORMATAÇÃO PARA VALORES PEQUENOS (Eixo Y: Tempo)
def time_formatter(y, pos):
    """Formata rótulos do eixo Y para decimal, evitando notação científica para valores comuns."""
    if y >= 1.0:
        return f"{int(y)}"
    if y >= 0.1:
        return f"{y:0.1f}".rstrip('0').rstrip('.')
    if y >= 0.01:
        return f"{y:0.2f}".rstrip('0').rstrip('.')
    if y >= 0.001:
        return f"{y:0.3f}".rstrip('0').rstrip('.')
    return f"{y:g}"
    
# 2. FUNÇÃO DE FORMATAÇÃO PARA INTEIROS GRANDES (Eixo X: N)
def integer_formatter(x, pos):
    """Formata rótulos do eixo X para números inteiros (10, 1000, 1000000), 
    usando ponto como separador de milhar para melhor legibilidade."""
    x_int = int(x)
    return f'{x_int:,}'.replace(',', '.')

def grafico_1_tempo_e_memoria():
    caminho_arquivo = os.path.join(NOME_PASTA_DADOS, FICHEIRO_1)
    
    try:
        df = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        return

    # Lógica de separação (assumimos que o CSV é limpo e contém as colunas Metrica/Valor)
    if 'Valor' in df.columns and 'Metrica' in df.columns:
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        # Usando os nomes das métricas corrigidas na análise (Tempo_Execucao_s e Memoria_Pico_Bytes)
        df_tempo = df[df['Metrica'] == 'Tempo_Execucao_s'].copy()
        df_memoria = df[df['Metrica'] == 'Memoria_Pico_Bytes'].copy()
    
    elif len(df.columns) == 2:
        df.columns = ['Tamanho_N', 'Valor']
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df_tempo = df.iloc[0::2].copy()    
        df_memoria = df.iloc[1::2].copy()  
    else:
        return

    # FILTRO CRÍTICO: Removendo valores <= 0 para escala logarítmica
    df_tempo = df_tempo[(df_tempo['Valor'] > 0) & (df_tempo['Tamanho_N'] > 0)]
    df_memoria = df_memoria[(df_memoria['Valor'] > 0) & (df_memoria['Tamanho_N'] > 0)]
    
    fig, ax1 = plt.subplots(figsize=(12, 7))

    cor_tempo = 'tab:blue'
    ax1.set_xlabel('Tamanho da Lista (N)')
    ax1.set_ylabel('Tempo de Execução (segundos)', color=cor_tempo)
    sns.lineplot(data=df_tempo, x='Tamanho_N', y='Valor', ax=ax1, color=cor_tempo, marker='o', label='Tempo')
    ax1.tick_params(axis='y', labelcolor=cor_tempo)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # APLICAÇÃO DOS FORMATADORES
    ax1.yaxis.set_major_formatter(FuncFormatter(time_formatter))
    ax1.xaxis.set_major_formatter(FuncFormatter(integer_formatter))

    ax2 = ax1.twinx()
    
    cor_memoria = 'tab:red'
    ax2.set_ylabel('Pico de Uso de Memória (Bytes)', color=cor_memoria)
    sns.lineplot(data=df_memoria, x='Tamanho_N', y='Valor', ax=ax2, color=cor_memoria, marker='x', label='Memória')
    ax2.tick_params(axis='y', labelcolor=cor_memoria)
    ax2.set_yscale('log') 

    # O Eixo Y Secundário (Memória)
    ax2.yaxis.set_major_formatter(FuncFormatter(integer_formatter))

    plt.title('Desempenho de Tempo e Memória do Comb Sort (Caso Médio)')
    fig.tight_layout()
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')
    ax1.get_legend().remove()

    # Salva o gráfico em PDF
    caminho_saida = os.path.join(NOME_PASTA_GRAFICOS, '1_tempo_vs_memoria_combsort.pdf')
    plt.savefig(caminho_saida, dpi=300)
    plt.close()


def grafico_2_cenarios_combsort():
    caminho_arquivo = os.path.join(NOME_PASTA_DADOS, FICHEIRO_2)
    try:
        df = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        return

    plt.figure(figsize=(10, 6))
    
    sns.lineplot(data=df, x='Tamanho_N', y='Num_Comparacoes', hue='Cenario', marker='o') 
    
    plt.title('Número de Comparações do Comb Sort por Cenário de Entrada')
    plt.xlabel('Tamanho da Lista (N)')
    plt.ylabel('Número de Comparações') 
    
    plt.xscale('log')
    plt.yscale('log')
    
    
    plt.grid(True, which="both", ls="--")
    plt.legend(title='Cenário')
    caminho_saida = os.path.join(NOME_PASTA_GRAFICOS, '2_comparacao_cenarios_combsort.pdf')
    plt.savefig(caminho_saida, dpi=300) 
    plt.close()

def grafico_3_comparativo_algoritmos():
    caminho_arquivo = os.path.join(NOME_PASTA_DADOS, FICHEIRO_3)
    try:
        df = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        return

    df['Tempo_Execucao_s'] = pd.to_numeric(df['Tempo_Execucao_s'], errors='coerce')
    cenarios = df['Cenario'].unique()

    for cenario in cenarios:
        df_cenario = df[df['Cenario'] == cenario]
        plt.figure(figsize=(12, 7))
        sns.lineplot(data=df_cenario, x='Tamanho_N', y='Tempo_Execucao_s', hue='Algoritmo', marker='o')
        
        plt.yscale('log')
        plt.xscale('log')
        
        plt.gca().yaxis.set_major_formatter(FuncFormatter(time_formatter))
        plt.gca().xaxis.set_major_formatter(FuncFormatter(integer_formatter))
        
        plt.title(f'Comparativo de Desempenho: {cenario}')
        plt.xlabel('Tamanho da Lista (N)')
        plt.ylabel('Tempo de Execução (segundos)')
        plt.grid(True, which="both", ls="--")
        plt.legend(title='Algoritmo')
        
        nome_arquivo_seguro = cenario.replace(' ', '_').replace('(', '').replace(')', '').lower()
        caminho_saida = os.path.join(NOME_PASTA_GRAFICOS, f'3_comparativo_{nome_arquivo_seguro}.pdf')
        plt.savefig(caminho_saida, dpi=300)
        plt.close()


if __name__ == '__main__':
    sns.set_theme(style="whitegrid")
    
    grafico_1_tempo_e_memoria()
    grafico_2_cenarios_combsort()
    grafico_3_comparativo_algoritmos()
    
    print("\nTodos os gráficos foram gerados com sucesso!")