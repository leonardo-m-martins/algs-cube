import numpy as np
import os
from src.move import MOVES

def init_get_state_tables() -> None:
    perm_table = np.zeros((5040, 16), dtype=np.uint8)
    ori_table = np.zeros((729, 16), dtype=np.uint8)

    facts = [720, 120, 24, 6, 2, 1]
    
    for p_id in range(5040):
        temp = p_id
        avail = list(range(7)) 
        p = np.zeros(8, dtype=np.uint8)
        
        for i in range(6):
            idx = temp // facts[i]
            temp %= facts[i]
            p[i] = avail.pop(idx) 
            
        p[6] = avail[0]
        p[7] = 7
        
        perm_table[p_id, :8] = p

    for o_id in range(729):
        temp = o_id
        o = np.zeros(8, dtype=np.uint8)
        o_sum = 0
        
        for i in range(6):
            o[i] = temp % 3
            temp //= 3
            o_sum += o[i]
        o[6] = (3 - (o_sum % 3)) % 3
        
        ori_table[o_id, 8:] = o

    return perm_table, ori_table

def get_perm_id(perm: np.ndarray):
    counts = np.zeros(8, dtype=np.uint32)
    
    for i in range(8):
        smaller_to_left = np.sum(perm[i] > perm[:i])
        counts[i] = perm[i] - smaller_to_left
        
    perm_weights = np.array([720, 120, 24, 6, 2, 1, 0, 0], dtype=np.uint32)
    perm_id = np.dot(counts, perm_weights)
    return perm_id

def get_ori_id(ori: np.ndarray):
    ori_id = 0
    for i in range(6):
        ori_id += int(ori[i + 8]) * (3 ** i)
    return ori_id

def init_get_moves(perm_table, ori_table):
    perm_moves = np.zeros((5040, 9), dtype=np.uint16)
    ori_moves = np.zeros((729, 9), dtype=np.uint16)

    for i in range(5040):
        perm = perm_table[i]
        for j, move in enumerate(MOVES):
            new_perm = perm[move.shuffle_mask]
            perm_moves[i, j] = get_perm_id(new_perm)
    
    for i in range(729):
        ori = ori_table[i]
        for j, move in enumerate(MOVES):
            new_ori = ori[move.shuffle_mask]
            new_ori += move.twist_data
            new_ori %= 3

            ori_moves[i, j] = get_ori_id(new_ori)

    return perm_moves, ori_moves

def generate():
    perm_table, ori_table = init_get_state_tables()
    perm_moves, ori_moves = init_get_moves(perm_table, ori_table)

    if not os.path.exists("data"):
        os.mkdir("data")

    np.save("data/ori_table.npy", ori_table)
    np.save("data/ori_moves.npy", ori_moves)
    np.save("data/perm_table.npy", perm_table)
    np.save("data/perm_moves.npy", perm_moves)

try:
    ori_table = np.load("data/ori_table.npy")
    perm_table = np.load("data/perm_table.npy")
    ori_moves = np.load("data/ori_moves.npy").astype(np.uint32)
    perm_moves = np.load("data/perm_moves.npy").astype(np.uint32)
except:
    generate()
    ori_table = np.load("data/ori_table.npy")
    perm_table = np.load("data/perm_table.npy")
    ori_moves = np.load("data/ori_moves.npy").astype(np.uint32)
    perm_moves = np.load("data/perm_moves.npy").astype(np.uint32)