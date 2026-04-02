import numpy as np
import pandas as pd

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

temp_perms = np.array([m[0] for m in MOVES.values()], dtype=np.uint8)
PERMS = np.hstack([temp_perms, temp_perms + 8]).copy()
ORIS = np.array([m[1] for m in MOVES.values()], dtype=np.uint8)
MOVE_NAMES = list(MOVES.keys())

del temp_perms

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
    

# 1. Gerar todos os estados em um array bidimensional com tamamho 3674160 X 16
# 2. para cada estado gerar cada movimento em um 
# array tridimensional de tamanho 3674160 X 9 X 16
def gerar_grafo(initial_state_arr: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    N_STATES = 3674160
    all_unique_states = np.array([initial_state_arr])
    state_mapping = np.empty((N_STATES, 9, 16), dtype=np.uint8)
    current_layer = np.array([initial_state_arr])
    offset = 0

    nivel = 0
    for i in range(12):
        print(f'Nível {nivel}: {len(current_layer)} elementos na camada\n{len(all_unique_states)} estados únicos encontrados\n')
        offset_high = offset + len(current_layer)
        nivel += 1

        next_layer = None

        for i in range(len(PERMS)):

            new_states = current_layer[:, PERMS[i]]

            new_states[:, 8:] += ORIS[i]

            new_states[:, 8:][new_states[:, 8:] >= 3] -= 3

            new_states = np.ascontiguousarray(new_states)
            
            state_mapping[offset:offset_high, i] = new_states

            if next_layer is None: 
                next_layer = new_states
            else: 
                next_layer = np.vstack([next_layer, new_states])

        next_layer_view = next_layer.view(dtype='S16').ravel()

        next_layer_view: np.ndarray = pd.unique(next_layer_view)

        next_layer_view = np.ascontiguousarray(next_layer_view)
        all_unique_states = np.ascontiguousarray(all_unique_states)

        mask = np.isin(next_layer_view, all_unique_states.view(dtype='S16').ravel(), assume_unique=True, invert=True)

        next_layer = next_layer_view.view(np.uint8).reshape(-1,16)
        current_layer = next_layer[mask]

        all_unique_states = np.vstack([all_unique_states, current_layer])
        
        offset = offset_high

    return all_unique_states, state_mapping
