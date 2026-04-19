import numpy as np
from src.cube_engine import generate_cubes, get_heuristic
import random as rd

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

# -------------------------------------------------------------------------
# BASIC STRUCTURES AND MOVES
# -------------------------------------------------------------------------

class Move:
    def __init__(self, shuffle_mask, twist_data):
        self.shuffle_mask = np.array(shuffle_mask, dtype=np.uint8)
        self.twist_data = np.array(twist_data, dtype=np.uint8)

class MoveName:
    U = 0; U2 = 1; U3 = 2; R = 3; R2 = 4; R3 = 5; F = 6; F2 = 7; F3 = 8
    MOVE_COUNT = 9

MOVES = [
    # MOVE_U
    Move([1, 5, 2, 3, 0, 4, 6, 7, 9, 13, 10, 11, 8, 12, 14, 15],
         [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]),
    # MOVE_U2
    Move([5, 4, 2, 3, 1, 0, 6, 7, 13, 12, 10, 11, 9, 8, 14, 15],
         [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]),
    # MOVE_U3
    Move([4, 0, 2, 3, 5, 1, 6, 7, 12, 8, 10, 11, 13, 9, 14, 15],
         [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]),
    # MOVE_R
    Move([0, 3, 2, 6, 4, 1, 5, 7, 8, 11, 10, 14, 12, 9, 13, 15],
         [0,0,0,0,0,0,0,0, 0,1,0,2,0,2,1,0]),
    # MOVE_R2
    Move([0, 6, 2, 5, 4, 3, 1, 7, 8, 14, 10, 13, 12, 11, 9, 15],
         [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]),
    # MOVE_R3
    Move([0, 5, 2, 1, 4, 6, 3, 7, 8, 13, 10, 9, 12, 14, 11, 15],
         [0,0,0,0,0,0,0,0, 0,1,0,2,0,2,1,0]),
    # MOVE_F
    Move([2, 0, 3, 1, 4, 5, 6, 7, 10, 8, 11, 9, 12, 13, 14, 15],
         [0,0,0,0,0,0,0,0, 1,2,2,1,0,0,0,0]),
    # MOVE_F2
    Move([3, 2, 1, 0, 4, 5, 6, 7, 11, 10, 9, 8, 12, 13, 14, 15],
         [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]),
    # MOVE_F3
    Move([1, 3, 0, 2, 4, 5, 6, 7, 9, 11, 8, 10, 12, 13, 14, 15],
         [0,0,0,0,0,0,0,0, 1,2,2,1,0,0,0,0])
]

# -------------------------------------------------------------------------
# CUBE CLASS
# -------------------------------------------------------------------------

class Cube:
    def __init__(self, state=None):
        """Initializes the cube. If no state is provided, creates a solved 2x2x2 cube."""
        if state is not None:
            self.state = np.array(state, dtype=np.uint8)
        else:
            # Identity state: Permutation (0-7), Orientation (0s)
            self.state = np.array([0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)

    def move_inplace(self, move_obj: Move) -> None:
        # Shuffle the state
        self.state = self.state[move_obj.shuffle_mask]
        
        # Add the twist data
        self.state += move_obj.twist_data
        
        # Modulo 3 constraint purely on the Orientation half (indices 8-15)
        # Replaces the SIMD subtraction/min logic in C++
        self.state[8:] %= 3
        pass

    def move(self, move_obj: Move) -> 'Cube':
        """Returns a new Cube object after applying the move."""
        new_cube = Cube(self.state.copy())
        new_cube.move_inplace(move_obj)
        return new_cube

    def get_id(self) -> int:

        ori_id = 0
        for i in range(6):
            ori_id += int(self.state[i + 8]) * (3 ** i)

        perm_state = self.state[:8]
        counts = np.zeros(8, dtype=np.uint32)
        
        for i in range(8):
            smaller_to_left = np.sum(perm_state[i] > perm_state[:i])
            counts[i] = perm_state[i] - smaller_to_left
            
        # Multiply inversion counts by their factorial weights
        perm_weights = np.array([720, 120, 24, 6, 2, 1, 0, 0], dtype=np.uint32)
        perm_id = np.dot(counts, perm_weights)
        
        return int((perm_id * 729) + ori_id)

    def print(self) -> None:
        perm_str = " ".join(str(x) for x in self.state[:8])
        ori_str = " ".join(str(x) for x in self.state[8:])
        print(f"Perm: {perm_str} | Ori: {ori_str} | Id: {self.get_id()}")
        pass

    def scramble(self) -> None:
        for _ in range(100):
            self.move_inplace(rd.choice(MOVES))

    def __eq__(self, value):
        return type(value) == type(self) and hash(self) == hash(value)

    def __hash__(self):
        return self.get_id()

# Tiny global lookup tables
perm_table = np.zeros((5040, 16), dtype=np.uint8)
ori_table = np.zeros((729, 16), dtype=np.uint8)

def init_get_state_tables() -> None:
    """Precomputes the permutation and orientation lookup tables."""
    # 1. Precompute all 5040 permutations
    facts = [720, 120, 24, 6, 2, 1]
    
    for p_id in range(5040):
        temp = p_id
        # Using a list allows us to replicate the C++ array shifting natively
        avail = list(range(7)) 
        p = np.zeros(8, dtype=np.uint8)
        
        for i in range(6):
            idx = temp // facts[i]
            temp %= facts[i]
            # .pop() automatically shifts the remaining elements
            p[i] = avail.pop(idx) 
            
        p[6] = avail[0]
        p[7] = 7
        
        # Store just the permutation half (zeros in the orientation half)
        perm_table[p_id, :8] = p

    # 2. Precompute all 729 orientations
    for o_id in range(729):
        temp = o_id
        o = np.zeros(8, dtype=np.uint8)
        o_sum = 0
        
        for i in range(6):
            o[i] = temp % 3
            temp //= 3
            o_sum += o[i]
        o[6] = (3 - (o_sum % 3)) % 3
            
        # Store just the orientation half (zeros in the permutation half)
        ori_table[o_id, 8:] = o

def get_state_lup(state_id: int) -> 'Cube':
    """Reconstructs a Cube from a unique state ID using the lookup tables."""
    # 1. Separate the IDs using the 729 divisor
    perm_id = state_id // 729
    ori_id = state_id % 729

    # 2. Fetch the precomputed numpy arrays
    p_vec = perm_table[perm_id]
    o_vec = ori_table[ori_id]

    # 3. Bitwise OR them together to combine into a single state
    # (Since p_vec has zeros at 8:16 and o_vec has zeros at 0:8, this cleanly merges them)
    combined_state = np.bitwise_or(p_vec, o_vec)
    
    return Cube(combined_state)
    
class Nos(list):
    def index(self, state):
        return state
    
init_get_state_tables()
grafo = generate_cubes()
nos = Nos([x for x in range(len(grafo))])