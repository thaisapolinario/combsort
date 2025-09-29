import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configurações ---
NOME_PASTA_DADOS = "DADOS"
NOME_PASTA_GRAFICOS = "GRAFICOS"

# Nomes dos arquivos de entrada
# ATENÇÃO: Verifique se o nome do arquivo da análise 1 corresponde ao seu arquivo gerado
FICHEIRO_1 = "analise_1_tempo_memoria.csv" 
FICHEIRO_2 = "analise_2_tipos_entrada_combsort.csv"
FICHEIRO_3 = "analise_3_comparativa_algoritmos.csv"

# Garante que a pasta para salvar os gráficos exista
os.makedirs(NOME_PASTA_GRAFICOS, exist_ok=True)


def grafico_1_tempo_e_memoria():
    """
    Gera um gráfico de escalabilidade com dois eixos Y (Tempo e Memória),
    adaptado para ler um arquivo CSV mal formatado com dados alternados.
    """
    print("Gerando Gráfico 1: Escalabilidade de Tempo e Memória do Comb Sort...")
    caminho_arquivo = os.path.join(NOME_PASTA_DADOS, FICHEIRO_1)
    
    # Carrega os dados. O cabeçalho está incorreto, mas vamos lidar com isso.
    df = pd.read_csv(caminho_arquivo)

    # --- INÍCIO DA MODIFICAÇÃO PARA LER DADOS ALTERNADOS ---
    
    # Renomeia as colunas para facilitar o manuseio
    df.columns = ['Tamanho_N', 'Valor']

    # Separa as linhas pares (índices 0, 2, 4...) que contêm o TEMPO
    df_tempo = df.iloc[0::2].copy()
    
    # Separa as linhas ímpares (índices 1, 3, 5...) que contêm a MEMÓRIA
    df_memoria = df.iloc[1::2].copy()
    
    # Converte a coluna 'Valor' de cada tabela para o tipo numérico
    df_tempo['Valor'] = pd.to_numeric(df_tempo['Valor'])
    df_memoria['Valor'] = pd.to_numeric(df_memoria['Valor'])

    # --- FIM DA MODIFICAÇÃO ---

    # --- Criação do Gráfico com Dois Eixos (mesma lógica de antes) ---
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Eixo 1 (Esquerda) - TEMPO
    cor_tempo = 'tab:blue'
    ax1.set_xlabel('Tamanho da Lista (N)')
    ax1.set_ylabel('Tempo de Execução (segundos)', color=cor_tempo)
    sns.lineplot(data=df_tempo, x='Tamanho_N', y='Valor', ax=ax1, color=cor_tempo, marker='o', label='Tempo')
    ax1.tick_params(axis='y', labelcolor=cor_tempo)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # Cria o segundo eixo Y
    ax2 = ax1.twinx()
    
    # Eixo 2 (Direita) - MEMÓRIA
    cor_memoria = 'tab:red'
    ax2.set_ylabel('Pico de Uso de Memória (Bytes)', color=cor_memoria)
    sns.lineplot(data=df_memoria, x='Tamanho_N', y='Valor', ax=ax2, color=cor_memoria, marker='x', label='Memória')
    ax2.tick_params(axis='y', labelcolor=cor_memoria)
    ax2.set_yscale('log') 

    # Título e Layout
    plt.title('Desempenho de Tempo e Memória do Comb Sort (Caso Médio)')
    fig.tight_layout()
    
    # Legenda
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')
    ax1.get_legend().remove()

    # Salva o gráfico
    caminho_saida = os.path.join(NOME_PASTA_GRAFICOS, '1_tempo_vs_memoria_combsort.png')
    plt.savefig(caminho_saida, dpi=300)
    plt.close()
    print(f"-> Gráfico salvo em: {caminho_saida}")


def grafico_2_cenarios_combsort():
    """
    Gera um gráfico comparando os 3 cenários (Melhor, Médio, Pior) para o Comb Sort.
    """
    print("\nGerando Gráfico 2: Comb Sort por Cenário de Entrada...")
    caminho_arquivo = os.path.join(NOME_PASTA_DADOS, FICHEIRO_2)
    df = pd.read_csv(caminho_arquivo)

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
    print(f"-> Gráfico salvo em: {caminho_saida}")


def grafico_3_comparativo_algoritmos():
    """
    Gera um gráfico comparando Comb Sort e Bubble Sort.
    """
    print("\nGerando Gráfico 3: Comb Sort vs. Bubble Sort...")
    caminho_arquivo = os.path.join(NOME_PASTA_DADOS, FICHEIRO_3)
    df = pd.read_csv(caminho_arquivo)

    df_pior_caso = df[df['Cenario'] == 'Lista Invertida (Pior Caso)']

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_pior_caso, x='Tamanho_N', y='Tempo_Execucao_s', hue='Algoritmo', marker='o')
    
    plt.yscale('log')
    plt.xscale('log')

    plt.title('Comparativo de Desempenho: Comb Sort vs. Bubble Sort (Pior Caso)')
    plt.xlabel('Tamanho da Lista (N) - Escala Log')
    plt.ylabel('Tempo de Execução (segundos) - Escala Log')
    plt.grid(True, which="both", ls="--")
    plt.legend(title='Algoritmo')
    
    caminho_saida = os.path.join(NOME_PASTA_GRAFICOS, '3_comparativo_comb_vs_bubble.png')
    plt.savefig(caminho_saida, dpi=300)
    plt.close()
    print(f"-> Gráfico salvo em: {caminho_saida}")


if __name__ == '__main__':
    sns.set_theme(style="whitegrid")
    
    grafico_1_tempo_e_memoria()
    grafico_2_cenarios_combsort()
    grafico_3_comparativo_algoritmos()
    
    print("\nTodos os gráficos foram gerados com sucesso!")