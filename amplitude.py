# Exemplo de como aplicar o algoritmo de amplitude para um cubo aleatório

import algoritmos.BuscaNP as BuscaNP
from Cube import Cube, grafo, nos, MOVES, get_state_lup
from numpy import uint32
import random as rd

busca_np = BuscaNP.buscaNP()

cube = Cube()
cube.print()

for i in range(100):
    cube.move_inplace(MOVES[rd.randint(0, 8)])

print('\n')
caminho = busca_np.amplitude_grafo(inicio=uint32(cube.get_id()), fim=uint32(0), nos=nos, grafo=grafo)

print(f'Caminho de tamanho {len(caminho) - 1}: {caminho}')

for c in caminho:
    get_state_lup(c).print()