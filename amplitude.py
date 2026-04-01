import numpy as np
from algoritmos.BuscaNP import buscaNP
from cube import initial_state, apply_move

# 1. Carrega os arquivos .npy
nos_array = np.load("grafo_estados.npy")
adj_data = np.load("grafo_adj_data.npy")
adj_offsets = np.load("grafo_adj_offsets.npy")

# 2. Criamos uma classe "FakeList" para enganar o .index()
class FastNos(list):
    def __init__(self, array):
        self.array = array
        # Criamos o mapa de busca rápida uma única vez
        self.mapa = {self.array[i].tobytes(): i for i in range(len(self.array))}
    
    def index(self, estado):
        # Transforma o array do nó em bytes e busca no dicionário O(1)
        return self.mapa[estado.tobytes() if isinstance(estado, np.ndarray) else estado]
    
    def __getitem__(self, i):
        return self.array[i].tobytes()

# 3. Criamos um dicionário de adjacências para o parâmetro 'grafo'
# Para não mudar a função, 'grafo' precisa ser algo que retorne os vizinhos
grafo_dict = {}
for i in range(len(nos_array)):
    start = adj_offsets[i]
    end = adj_offsets[i+1]
    # Guardamos os estados (bytes) dos vizinhos
    indices_v = adj_data[start:end]
    grafo_dict[i] = [nos_array[idx].tobytes() for idx in indices_v]

# Instanciamos os objetos que sua função pede
nos_prontos = FastNos(nos_array)

buscador = buscaNP()

# caminho = buscador.amplitude_grafo(
#     inicio=inicio_bytes, 
#     fim=initial_state.tobytes(), 
#     nos=nos_prontos, 
#     grafo=grafo_dict
# )