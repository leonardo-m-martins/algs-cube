import numpy as np
from src.cube_engine import generate_cubes, get_heuristic
from src.move import Move, MOVES
from src.static_data import perm_table, ori_table
import random as rd

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

    def scramble(self) -> None:
        for _ in range(100):
            self.move_inplace(rd.choice(MOVES))

    def validate_ori(self) -> bool:
        return sum(self.state[8:]) % 3 == 0

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
    
grafo = generate_cubes()
