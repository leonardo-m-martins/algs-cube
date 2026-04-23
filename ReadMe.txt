ALGS-CUBE: RESOLVEDOR DE CUBO MÁGICO 2X2X2

INSTRUÇÕES DE EXECUÇÃO

Requisitos de Software: Python 3.9 ou superior

Passo a Passo para Instalação e Execução:
Passo 1: Abra o terminal de comando e navegue até a pasta raiz do projeto algs-cube.
Passo 2: Instale as dependências do arquivo requirements.txt:
    pip install -r requirements.txt
Passo 3: Execute o arquivo principal:
    python main.py.

EXPLICAÇÃO DO PROGRAMA E DA INTERFACE GRÁFICA

O Programa:
Este projeto é um simulador e resolvedor do Cubo Magico 2x2x2. Ele aplica metodos e algoritmos clássicos de Inteligência Artificial para encontrar a solução a partir de um estado específico do cubo, permitindo avaliar e comparar estratégias.

Algoritmos Implementados:
Buscas Não Informadas (Cegas): Amplitude (BFS), Profundidade (DFS), Profundidade Limitada, Aprofundamento Iterativo (IDS), Bidirecional, Custo Uniforme.
Buscas Informadas (Heurísticas): Gulosa (Greedy), A-Estrela (A*) e AIA (IDA*).

Interface Gráfica:
A interface do programa foi desenvolvida utilizando a biblioteca Tkinter, sendo estruturada em diferentes seções para a utilização.

Planificação do Cubo (Cube Net): Fica no centro da tela, mostrando o cubo aberto. O usuário pode clicar nos adesivos para mudar as cores manualmente e montar o estado inicial que desejar.
Painel de Controle: Possui um menu de Seleção de Algoritmo, onde se escolhe a técnica de IA desejada. Tambem possui Parametros Dinâmicos, que exibem campos extras caso o algoritmo precise de limitacao de profundidade ou custo de movimento.
Visualizacao de Resultados: Após acionar o botão "Resolver Cubo", o programa faz a busca e exibe o caminho de movimentos. É possível utilizar os botoes de "Anterior" e "Proximo" para visualizar os estados do cubo em cada passo.

Estrutura de Arquivos:
O diretorio /src guarda toda a logica dos algoritmos (BuscaP.py, BuscaNP.py), o funcionamento logico do cubo (cube.py) e o codigo da interface visual (gui.py).
O diretorio /data guarda as tabelas de permutacao e orientacao pre-calculadas.
O arquivo main.py e o ponto de entrada que executa todo o sistema.
