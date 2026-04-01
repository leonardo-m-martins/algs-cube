import numpy as np
from collections import deque

"""
              |--------|
              |BLU-BRU-|
              |--------|
              |FLU-FRU-|
              |--------|
     |--------|--------|--------|--------|
     |BLU-FLU-|FLU-FRU-|FRU-BRU-|BRU-BLU-|
     |--------|--------|--------|--------|
     |BLD-FLD-|FLD-FRD-|FRD-BRD-|BRD-BLD-|
     |--------|--------|--------|--------|
              |--------|
              |FLD-FRD-|
              |--------|
              |BLD-BRD-|
              |--------|

FLU = 0
FRU = 1
FLD = 2
FRD = 3
BLU = 4
BRU = 5
BRD = 6
BLD = 7

              |--------|
              |-4---5--|
              |--------|
              |-0---1--|
              |--------|
     |--------|--------|--------|--------|
     |-4---0--|-0---1--|-1---5--|-5---4--|
     |--------|--------|--------|--------|
     |-7---2--|-2---3--|-3---6--|-6---7--|
     |--------|--------|--------|--------|
              |--------|
              |-2---3--|
              |--------|
              |-7---6--|
              |--------|


INITIAL = [0,1,2,3,4,5,6,7] [0,0,0,0,0,0,0]

MOVE_U = 
    0 -> 1
    1 -> 5
    4 -> 0
    5 -> 4
AFTER_MOVE_U =  [1,5,2,3,0,4,6,7] [0,0,0,0,0,0,0,0]

MOVE_U2 =
    0 -> 5
    1 -> 4
    4 -> 1
    5 -> 0
AFTER_MOVE_U2 = [5,4,2,3,1,0,6,7] [0,0,0,0,0,0,0,0]

MOVE _U3 =
    0 -> 4
    1 -> 0
    4 -> 5
    5 -> 1
AFTER_MOVE_U3 = [4,0,2,3,5,1,6,7] [0,0,0,0,0,0,0,0]

MOVE_R = 
    1 -> 3
    3 -> 6
    5 -> 1
    6 -> 5
AFTER_MOVE_R =  [0,3,2,6,4,1,5,7] [0,1,0,2,0,2,1,0]

MOVE_R2 =
    1 -> 6
    3 -> 5
    5 -> 3
    6 -> 1
AFTER_MOVE_R2 = [0,6,2,5,4,3,1,7] [0,0,0,0,0,0,0,0]

MOVE_R3 =
    1 -> 5
    3 -> 1
    5 -> 6
    6 -> 3
AFTER_MOVE_R3 = [0,5,2,1,4,6,3,7] [0,1,0,2,0,2,1,0]

MOVE_F = 
    0 -> 2
    1 -> 0
    2 -> 3
    3 -> 1
AFTER_MOVE_F =  [2,0,3,1,4,5,6,7] [1,2,2,1,0,0,0,0]

MOVE_F2 =
    0 -> 3
    1 -> 2
    2 -> 1
    3 -> 0
AFTER_MOVE_F2 = [3,2,1,0,4,5,6,7] [0,0,0,0,0,0,0,0]

MOVE_F3 =
    0 -> 1
    1 -> 3
    2 -> 0
    3 -> 2
AFTER_MOVE_F3 = [1,3,0,2,4,5,6,7] [1,2,2,1,0,0,0,0]

------------------------------------------------------------------
"""

initial_state = np.array([
    0, 1, 2, 3, 4, 5, 6, 7, 
    0, 0, 0, 0, 0, 0, 0, 0
], dtype=np.uint8)

MOVE_U_PERM =   np.array([1,5,2,3,0,4,6,7], dtype=np.uint8) 
MOVE_U_ORI =    np.array([0,0,0,0,0,0,0,0], dtype=np.uint8)

MOVE_U2_PERM =  np.array([5,4,2,3,1,0,6,7], dtype=np.uint8) 
MOVE_U2_ORI =   np.array([0,0,0,0,0,0,0,0], dtype=np.uint8)

MOVE_U3_PERM =  np.array([4,0,2,3,5,1,6,7], dtype=np.uint8) 
MOVE_U3_ORI =   np.array([0,0,0,0,0,0,0,0], dtype=np.uint8)

MOVE_R_PERM =   np.array([0,3,2,6,4,1,5,7], dtype=np.uint8) 
MOVE_R_ORI =    np.array([0,1,0,2,0,2,1,0], dtype=np.uint8)

MOVE_R2_PERM =  np.array([0,6,2,5,4,3,1,7], dtype=np.uint8) 
MOVE_R2_ORI =   np.array([0,0,0,0,0,0,0,0], dtype=np.uint8)

MOVE_R3_PERM =  np.array([0,5,2,1,4,6,3,7], dtype=np.uint8) 
MOVE_R3_ORI =   np.array([0,1,0,2,0,2,1,0], dtype=np.uint8)

MOVE_F_PERM =   np.array([2,0,3,1,4,5,6,7], dtype=np.uint8) 
MOVE_F_ORI =    np.array([1,2,2,1,0,0,0,0], dtype=np.uint8)

MOVE_F2_PERM =  np.array([3,2,1,0,4,5,6,7], dtype=np.uint8) 
MOVE_F2_ORI =   np.array([0,0,0,0,0,0,0,0], dtype=np.uint8)

MOVE_F3_PERM =  np.array([1,3,0,2,4,5,6,7], dtype=np.uint8)
MOVE_F3_ORI =   np.array([1,2,2,1,0,0,0,0], dtype=np.uint8)

MOVES = {
    'U':    (MOVE_U_PERM, MOVE_U_ORI),
    'U2':   (MOVE_U2_PERM, MOVE_U2_ORI),
    'U3':   (MOVE_U3_PERM, MOVE_U3_ORI),

    'R':    (MOVE_R_PERM, MOVE_R_ORI),
    'R2':   (MOVE_R2_PERM, MOVE_R2_ORI),
    'R3':   (MOVE_R3_PERM, MOVE_R3_ORI),

    'F':    (MOVE_F_PERM, MOVE_F_ORI),
    'F2':   (MOVE_F2_PERM, MOVE_F2_ORI),
    'F3':   (MOVE_F3_PERM, MOVE_F3_ORI),
}

PERMS = np.array([m[0] for m in MOVES.values()], dtype=np.uint8)
ORIS = np.array([m[1] for m in MOVES.values()], dtype=np.uint8)
MOVE_NAMES = list(MOVES.keys())

def print_state(state):
    print(f'Estado: {state}')

def apply_move(self, move: str):
    move_perm = MOVES[move][0]
    move_ori = MOVES[move][1]
            
    # 1. Permuta as posições e as orientações antigas simultaneamente
    new_pos = self.state[:8][move_perm]

    # 2. Soma as novas orientações (apenas na metade do array de orientação)
    # Usamos o truque do (soma >= 3) para evitar o % 3
    new_ori = (self.state[8:][move_perm] + move_ori)
    new_ori = np.where(new_ori >= 3, new_ori - 3, new_ori)
            
    return np.concatenate([new_pos, new_ori], dtype=np.uint8)

class Cube:
    def __init__(self, state):
        # expected state: np.array([
        #     0, 1, 2, 3, 4, 5, 6, 7, 
        #     0, 0, 0, 0, 0, 0, 0, 0
        # ], dtype=np.uint8)
        self.state = state
        pass

    def move(self, move: str):
        move_perm = MOVES[move][0]
        move_ori = MOVES[move][1]
            
        # 1. Permuta as posições e as orientações antigas simultaneamente
        new_pos = self.state[:8][move_perm]

        # 2. Soma as novas orientações (apenas na metade do array de orientação)
        # Usamos o truque do (soma >= 3) para evitar o % 3
        new_ori = (self.state[8:][move_perm] + move_ori)
        new_ori = np.where(new_ori >= 3, new_ori - 3, new_ori)
            
        return Cube(np.concatenate([new_pos, new_ori], dtype=np.uint8))
    
    def all_moves(self):
        return [self.move(m) for m in MOVES.keys()]
    
    def __eq__(self, other):
        if not isinstance(other, Cube):
            return False
        # Compara se todos os elementos do array são iguais
        return np.array_equal(self.state, other.state)

    def __hash__(self):
        # Converte o array para tupla para gerar um hash único e imutável
        return hash(self.state.tobytes())
    
def gerar_grafo(cubo: Cube):
    inicial = cubo

    grafo_dict = {
        inicial: inicial.all_moves()
    }

    fila = deque()
    fila.append(inicial)
    visitados = set()
    while len(fila) > 0:
        if len(visitados) % 1000 == 0:
            print(f'Visitados: {len(visitados)}')

        atual = fila.popleft()
        all_moves_atual = atual.all_moves()
        grafo_dict[atual] = all_moves_atual
        for state in all_moves_atual:
            if state not in visitados:
                fila.append(state)
        visitados.add(atual)



def gerar_grafo_otimizado(initial_state_arr: np.ndarray):
    # O set armazena bytes, que é MUITO mais rápido para hash que objetos
    initial_bytes = initial_state_arr.tobytes()
    
    # distancia ou pai (para reconstruir o caminho depois)
    # Usar dict de bytes -> bytes ou bytes -> int
    visitados = {initial_bytes: None}
    fila = deque([initial_bytes])
    
    count = 0
    while fila:
        atual_bytes = fila.popleft()
        
        # Converte de volta para array apenas para o cálculo
        atual_arr = np.frombuffer(atual_bytes, dtype=np.uint8)
        pos = atual_arr[:8]
        ori = atual_arr[8:]
        
        # Aplicamos todos os movimentos de uma vez usando broadcasting do NumPy
        # Isso gera todos os 9 estados vizinhos quase instantaneamente
        new_positions = pos[PERMS]
        
        # Soma de orientações e ajuste (mod 3) sem np.where
        new_orientations = ori[PERMS] + ORIS
        new_orientations[new_orientations >= 3] -= 3

        neighbor_states_bytes = []
        
        # Gera os novos estados
        for i in range(len(MOVE_NAMES)):
            # Concatenação manual rápida
            neighbor_arr = np.concatenate([new_positions[i], new_orientations[i]])
            neighbor_bytes = neighbor_arr.tobytes()
            neighbor_states_bytes.append(neighbor_bytes)

            if neighbor_bytes not in visitados:
                fila.append(neighbor_bytes)
            
        visitados[atual_bytes] = neighbor_states_bytes
        
        count += 1
        if count >= 100000:
            print(f'Estados únicos encontrados: {len(visitados)}')
            return

    return visitados


def gerar_grafo_turbo(initial_state_arr):
    initial_bytes = initial_state_arr.tobytes()
    visitados = {initial_bytes}
    camada_atual = {initial_bytes}
    
    nivel = 0
    while camada_atual:
        print(f"Nível {nivel}: {len(camada_atual)} estados. Total: {len(visitados)}")
        proxima_camada = set()
        
        # Converte a camada inteira para um blocão NumPy
        bloco_camada = np.frombuffer(b''.join(camada_atual), dtype=np.uint8).reshape(-1, 16)
        
        pos = bloco_camada[:, :8]
        ori = bloco_camada[:, 8:]
        
        # Calcula TODOS os vizinhos de TODOS os estados da camada de uma vez
        for i in range(len(PERMS)):
            # Permutação e Orientação vetorizada
            new_p = pos[:, PERMS[i]]
            new_o = (ori[:, PERMS[i]] + ORIS[i])
            new_o[new_o >= 3] -= 3
            
            # Reconstrói os estados
            vizinhos_bloco = np.concatenate([new_p, new_o], axis=1)
            
            # Aqui está o truque: converte o bloco de volta para lista de bytes
            novos_bytes = [b.tobytes() for b in vizinhos_bloco]
            proxima_camada.update(novos_bytes)
        
        # Filtra o que já foi visitado
        proxima_camada -= visitados
        visitados.update(proxima_camada)
        camada_atual = proxima_camada
        nivel += 1

def gerar_grafo_mapeado(initial_state_arr):
    initial_bytes = initial_state_arr.tobytes()
    
    # Estruturas de mapeamento
    lista_estados = [initial_bytes]
    mapa_indices = {initial_bytes: 0}
    adjacencias = [] # Será preenchida conforme expandimos
    
    fila = deque([0]) # Guardamos apenas o ÍNDICE na fila
    
    while fila:
        idx_atual = fila.popleft()
        estado_bytes = lista_estados[idx_atual]
        
        # Se já processamos as adjacências deste índice, pulamos
        if idx_atual < len(adjacencias):
            continue
            
        # Preparamos o array para o NumPy
        atual_arr = np.frombuffer(estado_bytes, dtype=np.uint8)
        pos = atual_arr[:8]
        ori = atual_arr[8:]
        
        vizinhos_do_no = []
        
        # Aplicamos os 9 movimentos
        for i in range(len(PERMS)):
            new_p = pos[PERMS[i]]
            new_o = (ori[PERMS[i]] + ORIS[i])
            new_o[new_o >= 3] -= 3
            
            v_bytes = np.concatenate([new_p, new_o]).tobytes()
            
            # Se é um estado novo, registramos
            if v_bytes not in mapa_indices:
                novo_idx = len(lista_estados)
                mapa_indices[v_bytes] = novo_idx
                lista_estados.append(v_bytes)
                fila.append(novo_idx)
            
            # Adicionamos o índice do vizinho à lista deste nó
            vizinhos_do_no.append(mapa_indices[v_bytes])
            
        adjacencias.append(vizinhos_do_no)

    return lista_estados, adjacencias
