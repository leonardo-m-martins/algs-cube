import numpy as np
from numba import njit

global perm_moves, ori_moves, TOTAL_STATES, MOVE_NUMBER

TOTAL_STATES = 3674160
MOVE_NUMBER = 9
perm_moves = np.load("perm_moves.npy", "r").astype(np.uint32)
ori_moves = np.load("ori_moves.npy", "r").astype(np.uint32)

def generate_cubes() -> np.ndarray:
    grafo = np.empty((TOTAL_STATES, MOVE_NUMBER), dtype=np.uint32)

    np.add(perm_moves[:, np.newaxis, :] * 729, ori_moves[np.newaxis, :, :], out=grafo.reshape(5040, 729, 9))

    return grafo

@njit
def get_move_from_id(id: int, move: int) -> int:
    perm_id = id // 729
    ori_id = id % 729

    perm_id = perm_moves[perm_id][move]
    ori_id = ori_moves[ori_id][move]

    return perm_id * 729 + ori_id

@njit
def get_heuristic(initial_id: int) -> np.ndarray:
    pruning_table = np.full((TOTAL_STATES, ), 255, dtype=np.uint8)
    pruning_table[initial_id] = 0
    current_dist = 0
    found_count = 1

    while (found_count < TOTAL_STATES):

        for id in range(TOTAL_STATES):
            if pruning_table[id] != current_dist: continue
            
            for move in range(9):
                neighbor = get_move_from_id(id, move)
                if pruning_table[neighbor] != 0xFF: continue
                
                pruning_table[neighbor] = current_dist + 1
                found_count += 1

        current_dist += 1
        if (current_dist > 12): break

    return pruning_table