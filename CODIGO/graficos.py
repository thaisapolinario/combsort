import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

NOME_PASTA_DADOS = "../DADOS" 
NOME_PASTA_GRAFICOS = "../GRAFICOS"

# Nomes dos arquivos de entrada
FICHEIRO_1 = "analise_1_tempo_memoria.csv"
FICHEIRO_2 = "analise_2_tipos_entrada_combsort.csv"
FICHEIRO_3 = "analise_3_comparativa_algoritmos.csv"

os.makedirs(NOME_PASTA_GRAFICOS, exist_ok=True)


def grafico_1_tempo_e_memoria():
    caminho_arquivo = os.path.join(NOME_PASTA_DADOS, FICHEIRO_1)
    
    try:
        df = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        return

    if 'Valor' in df.columns and 'Metrica' in df.columns:
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df_tempo = df[df['Metrica'] == 'Tempo_Execucao']
        df_memoria = df[df['Metrica'] == 'Memoria_Pico']
    
    elif len(df.columns) == 2:
        df.columns = ['Tamanho_N', 'Valor']
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df_tempo = df.iloc[0::2].copy()    
        df_memoria = df.iloc[1::2].copy()  
    else:
        return

    fig, ax1 = plt.subplots(figsize=(12, 7))

    cor_tempo = 'tab:blue'
    ax1.set_xlabel('Tamanho da Lista (N)')
    ax1.set_ylabel('Tempo de Execução (segundos)', color=cor_tempo)
    sns.lineplot(data=df_tempo, x='Tamanho_N', y='Valor', ax=ax1, color=cor_tempo, marker='o', label='Tempo')
    ax1.tick_params(axis='y', labelcolor=cor_tempo)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    ax2 = ax1.twinx()
    
    cor_memoria = 'tab:red'
    ax2.set_ylabel('Pico de Uso de Memória (Bytes)', color=cor_memoria)
    sns.lineplot(data=df_memoria, x='Tamanho_N', y='Valor', ax=ax2, color=cor_memoria, marker='x', label='Memória')
    ax2.tick_params(axis='y', labelcolor=cor_memoria)
    ax2.set_yscale('log') 

    plt.title('Desempenho de Tempo e Memória do Comb Sort (Caso Médio)')
    fig.tight_layout()
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')
    ax1.get_legend().remove()

    # Salva o gráfico
    caminho_saida = os.path.join(NOME_PASTA_GRAFICOS, '1_tempo_vs_memoria_combsort.png')
    plt.savefig(caminho_saida, dpi=300)
    plt.close()


def grafico_2_cenarios_combsort():
    caminho_arquivo = os.path.join(NOME_PASTA_DADOS, FICHEIRO_2)
    try:
        df = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        return

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Tamanho_N', y='Tempo_Execucao_s', hue='Cenario', marker='o')
    plt.title('Desempenho do Comb Sort por Cenário de Entrada')
    plt.xlabel('Tamanho da Lista (N)')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, which="both", ls="--")
    plt.legend(title='Cenário')
    caminho_saida = os.path.join(NOME_PASTA_GRAFICOS, '2_comparacao_cenarios_combsort.png')
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
        plt.title(f'Comparativo de Desempenho: {cenario}')
        plt.xlabel('Tamanho da Lista (N) - Escala Log')
        plt.ylabel('Tempo de Execução (segundos) - Escala Log')
        plt.grid(True, which="both", ls="--")
        plt.legend(title='Algoritmo')
        
        nome_arquivo_seguro = cenario.replace(' ', '_').replace('(', '').replace(')', '').lower()
        caminho_saida = os.path.join(NOME_PASTA_GRAFICOS, f'3_comparativo_{nome_arquivo_seguro}.png')
        plt.savefig(caminho_saida, dpi=300)
        plt.close()


if __name__ == '__main__':
    sns.set_theme(style="whitegrid")
    
    grafico_1_tempo_e_memoria()
    grafico_2_cenarios_combsort()
    grafico_3_comparativo_algoritmos()
    
    print("\nTodos os gráficos foram gerados com sucesso!")