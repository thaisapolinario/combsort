# Análise Comparativa de Algoritmos de Ordenação - CombSort
## Funcionalidades

- Análise: Compara o desempenho do Comb Sort em diversos casos.
- Cenários: Testa os algoritmos com listas aleatórias (caso médio), ordenadas (melhor caso) e invertidas (pior caso).
- Escalabilidade: Executa testes para múltiplos tamanhos de entrada (`N`) de forma exponencial.
- Dados: Salva todos os dados das análises em arquivos `.csv`.
- Gráficos: Gera automaticamente gráficos comparativos de desempenho.

## Pastas

O projeto utiliza a seguinte estrutura:

combsort/                 
├── README.md              
├── CODIGO/    

│   ├── combsort.py          # script principal para executar as análises

│   ├── graficos.py          # script para gerar os gráficos
│
├── DADOS/                 
│   ├── analise_1_tempo_memoria.csv
│   ├── analise_2_tipos_entrada_combsort.csv
│   └── analise_3_comparativa_algoritmos.csv
│
└── GRAFICOS/             
    ├── 1_tempo_vs_memoria_combsort.png
    ├── 2_comparacao_cenarios_combsort.png
    ├── 3_comparativo_lista_ja_ordenada_melhor_caso.png
    ├── 3_comparativo_lista_nao_ordenada_caso_medio.png
    └── 3_comparativo_lista_invertida_pior_caso.png


# Como Compilar

- 1º Passo: Entrar na pasta CODIGO
    cd CODIGO

- 2º Passo: Compilar o programa
    python combsort.py

    # Dentro do Programa
        - Escolher o tipo de análise a ser feita;
        - Escolher um ponto de partida do algoritmo (O algoritmo irá realizar multiplicações por 10 a partir desse ponto);
        - EScolher o número de passos (Multiplicações por 10)
        - Digitar 4 para fechar o programa;
    
- 3º Passo: Geração de Gráficos
    - python graficos.py
