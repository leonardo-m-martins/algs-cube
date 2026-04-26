import numpy as np
from numba import njit, uint8, uint32, int64, uint16, typed
from src.static_data import perm_moves, ori_moves

TOTAL_STATES = 3674160
MOVE_NUMBER = 9

def generate_cubes() -> np.ndarray:
    grafo = np.empty((TOTAL_STATES, MOVE_NUMBER), dtype=np.uint32)

    np.add(perm_moves[:, np.newaxis, :] * 729, ori_moves[np.newaxis, :, :], out=grafo.reshape(5040, 729, 9))

    return grafo

@njit(uint32(uint32, uint32))
def get_move_from_id(id: int, move: int) -> int:
    perm_id = id // 729
    ori_id = id % 729

    perm_id = perm_moves[perm_id][move]
    ori_id = ori_moves[ori_id][move]

    return perm_id * 729 + ori_id

@njit(uint16[::1](uint32, uint16[::1]))
def get_heuristic(initial_id: int, weights) -> np.ndarray:
    NULL = (1 << 16) - 1
    pruning_table = np.full((TOTAL_STATES, ), NULL, dtype=np.uint16)
    pruning_table[initial_id] = 0
    worst_case = max(weights) * 11
    bucket = [typed.List.empty_list(uint32) for _ in range(worst_case + 1)]
    bucket[0].append(initial_id)
    
    current_dist = 0

    # O caminho de A -> B não é necessariamente igual ao de B -> A
    # portanto faz-se necessário calcular a heurística com os movimentos inversos
    # onde inverso(U) = U3, inverso(U2) = U2, inverso(U3) = U 
    invert_mask = np.array([2, 1, 0, 5, 4, 3, 8, 7, 6], dtype=np.uint8)
    weights = weights[invert_mask]

    while current_dist <= worst_case:

        for id in bucket[current_dist]:
            if pruning_table[id] < current_dist: continue
            
            for move in range(9):
                neighbor = get_move_from_id(id, move)
                cost = current_dist + weights[move]
                
                if cost >= pruning_table[neighbor]: continue
                
                bucket[cost].append(neighbor)
                pruning_table[neighbor] = cost

        current_dist += 1
    return pruning_table
