from src.cube import Cube
from copy import deepcopy
import numpy as np

#------------------------
#- ENUMS
#------------------------

# Colors enum
class Colors:
    RED = 0
    BLUE = 1
    YELLOW = 2
    ORANGE = 3
    GREEN = 4
    WHITE = 5

# Subcubes enum
class Subcubes:
    FLU = 0
    FRU = 1
    FLD = 2
    FRD = 3
    BLU = 4
    BRU = 5
    BRD = 6
    BLD = 7

#------------------------
#- CONSTS
#------------------------

STICKER_COMBINATIONS = (
    {Colors.WHITE, Colors.GREEN, Colors.RED},
    {Colors.WHITE, Colors.GREEN, Colors.ORANGE},
    {Colors.WHITE, Colors.BLUE, Colors.RED},
    {Colors.WHITE, Colors.BLUE, Colors.ORANGE},
    {Colors.YELLOW, Colors.GREEN, Colors.RED},
    {Colors.YELLOW, Colors.GREEN, Colors.ORANGE},
    {Colors.YELLOW, Colors.BLUE, Colors.RED},
    {Colors.YELLOW, Colors.BLUE, Colors.ORANGE}
)

def create_ori_stickers_array():
    p012 = (0, 1, 2)
    p021 = (0, 2, 1)
    p102 = (1, 0, 2)
    p120 = (1, 2, 0)
    p201 = (2, 0, 1)
    p210 = (2, 1, 0)

    FRU = (
        (p102, p210, p021),
        (p012, p201, p120),
        (p012, p201, p120),
        (p102, p210, p021),
        (p012, p201, p120),
        (p102, p210, p021),
        (p012, p201, p120),
        (p012, p012, p012)
    )

    FLU = (
        (p012, p120, p201),
        (p102, p021, p210),
        (p102, p021, p210),
        (p012, p120, p201),
        (p102, p021, p210),
        (p012, p120, p201),
        (p102, p021, p210),
        (p012, p012, p012)
    )

    FRD = (
        (p012, p120, p201),
        (p102, p021, p210),
        (p102, p021, p210),
        (p012, p120, p201),
        (p102, p021, p210),
        (p012, p120, p201),
        (p102, p021, p210),
        (p012, p012, p012)
    )

    FLD = (
        (p102, p210, p021),
        (p012, p201, p120),
        (p012, p201, p120),
        (p102, p210, p021),
        (p012, p201, p120),
        (p102, p210, p021),
        (p012, p201, p120),
        (p012, p012, p012)
    )

    BRD = (
        (p102, p210, p021),
        (p012, p201, p120),
        (p012, p201, p120),
        (p102, p210, p021),
        (p012, p201, p120),
        (p102, p210, p021),
        (p012, p201, p120),
        (p012, p012, p012)
    )


    BRU = (
        (p012, p120, p201),
        (p102, p021, p210),
        (p102, p021, p210),
        (p012, p120, p201),
        (p102, p021, p210),
        (p012, p120, p201),
        (p102, p021, p210),
        (p012, p012, p012)
    )

    BLU = (
        (p102, p210, p021),
        (p012, p201, p120),
        (p012, p201, p120),
        (p102, p210, p021),
        (p012, p201, p120),
        (p102, p210, p021),
        (p012, p201, p120),
        (p012, p012, p012)
    )

    BLD = (
        (p102, p210, p021),
        (p012, p201, p120),
        (p012, p201, p120),
        (p102, p210, p021),
        (p012, p201, p120),
        (p102, p210, p021),
        (p012, p201, p120),
        (p012, p012, p012)
    )

    return np.array([
        FLU,
        FRU,
        FLD,
        FRD,
        BLU,
        BRU,
        BRD,
        BLD
    ], dtype=np.uint8)

ori_stickers = create_ori_stickers_array()

# alterar para que a ordem não importe
def hash_colors(colors: list):
    colors = deepcopy(colors)
    colors.sort()
    return colors[0] * 36 + colors[1] * 6 + colors[2]

class StickersCube:
    state: dict

    def __init__(self, state: dict=None, BLD: list=None, cube: Cube=None):
        if state != None:
            self.state = state

        elif cube == None:
            self.state = {
                Subcubes.FLU: [Colors.RED, Colors.BLUE, Colors.YELLOW],
                Subcubes.FRU: [Colors.RED, Colors.GREEN, Colors.YELLOW],
                Subcubes.FLD: [Colors.RED, Colors.BLUE, Colors.WHITE],
                Subcubes.FRD: [Colors.RED, Colors.GREEN, Colors.WHITE],
                Subcubes.BLU: [Colors.ORANGE, Colors.BLUE, Colors.YELLOW],
                Subcubes.BRU: [Colors.ORANGE, Colors.GREEN, Colors.YELLOW],
                Subcubes.BRD: [Colors.ORANGE, Colors.GREEN, Colors.WHITE],
                Subcubes.BLD: [Colors.ORANGE, Colors.BLUE, Colors.WHITE]
            }

        else:
            self.state = dict()

            b, l, d = BLD
            f, r, u = (b + 3) % 6, (l + 3) % 6, (d + 3) % 6



            solved = {
                Subcubes.FLU: [f, l, u],
                Subcubes.FRU: [f, r, u],
                Subcubes.FLD: [f, l, d],
                Subcubes.FRD: [f, r, d],
                Subcubes.BLU: [b, l, u],
                Subcubes.BRU: [b, r, u],
                Subcubes.BRD: [b, r, d],
                Subcubes.BLD: [b, l, d]
            }
            for subcube in range(8):
                goal = int(cube.state[subcube])
                colors = solved[cube.state[subcube]]
                ori = int(cube.state[subcube + 8])

                stickers = ori_stickers[subcube, goal, ori]
                zero = stickers[0]
                one = stickers[1]
                two = stickers[2]

                self.state[subcube] = [colors[zero], colors[one], colors[two]]
        pass

    def validate_stickers(self) -> bool:
        combinations = list(STICKER_COMBINATIONS)
        for stickers in self.state.values():
            stickers_set = set(stickers)
            if stickers_set in combinations:
                combinations.remove(stickers_set)
            else:
                return False
            
        return True
    
    def get_BLD(self):
        return self.state[Subcubes.BLD]
    
    def get_cube(self) -> Cube:
        b_color, l_color, d_color = self.state[Subcubes.BLD]
        f_color, r_color, u_color = (b_color + 3) % 6, (l_color + 3) % 6, (d_color + 3) % 6

        b, l, d = Colors.ORANGE, Colors.BLUE, Colors.WHITE 
        f, r, u = Colors.RED, Colors.GREEN, Colors.YELLOW

        relative_map = {
            b_color: b,
            l_color: l,
            d_color: d,
            f_color: f,
            r_color: r,
            u_color: u
        }

        cube_state = [-1 for _ in range(16)]

        goals = {
            hash_colors([f, l, u]): Subcubes.FLU,
            hash_colors([f, r, u]): Subcubes.FRU,
            hash_colors([f, l, d]): Subcubes.FLD,
            hash_colors([f, r, d]): Subcubes.FRD,
            hash_colors([b, l, u]): Subcubes.BLU,
            hash_colors([b, r, u]): Subcubes.BRU,
            hash_colors([b, r, d]): Subcubes.BRD,
            hash_colors([b, l, d]): Subcubes.BLD
        }

        for subcube, colors in self.state.items():
            relative_colors = [relative_map[color] for color in colors]

            # Perm
            goal = goals[hash_colors(relative_colors)]
            cube_state[subcube] = goal

            # Ori
            current_ori_pattern = tuple(np.array(relative_colors) % 3)
            available_patterns = [tuple(row) for row in ori_stickers[subcube, goal]]
            
            cube_state[subcube + 8] = available_patterns.index(current_ori_pattern)

        return Cube(cube_state)
    
    def scramble(self):
        cube = self.get_cube()
        cube.scramble()
        self.state = StickersCube(cube=cube, BLD=self.get_BLD()).state

    def rotate_x(self):
        """Rotates the entire cube on the X axis (R face direction)."""
        new_state = {}
        # Mapping the movement of the pieces
        mapping = {
            Subcubes.FLU: Subcubes.BLU,
            Subcubes.BLU: Subcubes.BLD,
            Subcubes.BLD: Subcubes.FLD,
            Subcubes.FLD: Subcubes.FLU,
            Subcubes.FRU: Subcubes.BRU,
            Subcubes.BRU: Subcubes.BRD,
            Subcubes.BRD: Subcubes.FRD,
            Subcubes.FRD: Subcubes.FRU
        }
        for old_pos, new_pos in mapping.items():
            colors = self.state[old_pos]
            # X rotation swaps F/B (index 0) with U/D (index 2)
            new_state[new_pos] = [colors[2], colors[1], colors[0]]
        self.state = new_state

    def rotate_y(self):
        """Rotates the entire cube on the Y axis (U face direction)."""
        new_state = {}
        mapping = {
            Subcubes.FLU: Subcubes.BLU,
            Subcubes.BLU: Subcubes.BRU,
            Subcubes.BRU: Subcubes.FRU,
            Subcubes.FRU: Subcubes.FLU,
            Subcubes.FLD: Subcubes.BLD,
            Subcubes.BLD: Subcubes.BRD,
            Subcubes.BRD: Subcubes.FRD,
            Subcubes.FRD: Subcubes.FLD
        }
        for old_pos, new_pos in mapping.items():
            colors = self.state[old_pos]
            # Y rotation swaps F/B (index 0) with L/R (index 1)
            new_state[new_pos] = [colors[1], colors[0], colors[2]]
        self.state = new_state

    def rotate_z(self):
        """Rotates the entire cube on the Z axis (F face direction)."""
        new_state = {}
        mapping = {
            Subcubes.FLU: Subcubes.FRU,
            Subcubes.FRU: Subcubes.FRD,
            Subcubes.FRD: Subcubes.FLD,
            Subcubes.FLD: Subcubes.FLU,
            Subcubes.BLU: Subcubes.BRU,
            Subcubes.BRU: Subcubes.BRD,
            Subcubes.BRD: Subcubes.BLD,
            Subcubes.BLD: Subcubes.BLU
        }
        for old_pos, new_pos in mapping.items():
            colors = self.state[old_pos]
            # Z rotation swaps L/R (index 1) with U/D (index 2)
            new_state[new_pos] = [colors[0], colors[2], colors[1]]
        self.state = new_state

    def match_BLD(self, BLD: list) -> bool:
        """
        Rotates the cube through its 24 possible spatial orientations 
        until the BLD subcube matches the target_BLD colors.
        Returns True if a match is found, False otherwise.
        """
        def _check_and_y():
            for _ in range(4):
                if self.get_BLD() == BLD:
                    return True
                self.rotate_y()
            return False

        if self.get_BLD() == BLD:
            return True

        # Cycle through all 6 faces pointing Down, and rotate Y 4 times for each
        
        # 1. Start orientation (D face is down)
        if _check_and_y(): return True
        
        # 2. B face is down
        self.rotate_x()
        if _check_and_y(): return True
        
        # 3. U face is down
        self.rotate_x()
        if _check_and_y(): return True
        
        # 4. F face is down
        self.rotate_x()
        if _check_and_y(): return True
        
        # Return to start orientation (X x 4 = 360 degrees)
        self.rotate_x()
        
        # 5. R face is down
        self.rotate_z()
        if _check_and_y(): return True
        
        # 6. L face is down (Z x 2 from R-down puts L-down)
        self.rotate_z()
        self.rotate_z()
        if _check_and_y(): return True
        
        # If no match is found, return the cube to its original spatial orientation
        self.rotate_z()
        return False
    
    def copy_match_BLD(self, BLD):
        new = StickersCube(cube=self.get_cube(), BLD=self.get_BLD())
        new.match_BLD(BLD)
        return new

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
"""
OFFSETS_L = {
    Subcubes.BLU: (0, 2), # (x, y)
    Subcubes.BLD: (0, 3),
    Subcubes.FLU: (1, 2),
    Subcubes.FLD: (1, 3)
}

OFFSETS_F = {
    Subcubes.FLU: (2, 2),
    Subcubes.FLD: (2, 3),
    Subcubes.FRU: (3, 2),
    Subcubes.FRD: (3, 3)
}

OFFSETS_U = {
    Subcubes.BLU: (2, 0),
    Subcubes.FLU: (2, 1),
    Subcubes.BRU: (3, 0),
    Subcubes.FRU: (3, 1)
}

OFFSETS_D = {
    Subcubes.FLD: (2, 4),
    Subcubes.BLD: (2, 5),
    Subcubes.FRD: (3, 4),
    Subcubes.BRD: (3, 5)
}

OFFSETS_R = {
    Subcubes.FRU: (4, 2),
    Subcubes.FRD: (4, 3),
    Subcubes.BRU: (5, 2),
    Subcubes.BRD: (5, 3)
}

OFFSETS_B = {
    Subcubes.BRU: (6, 2),
    Subcubes.BRD: (6, 3),
    Subcubes.BLU: (7, 2),
    Subcubes.BLD: (7, 3)
}

OFFSETS = [OFFSETS_F, OFFSETS_L, OFFSETS_U, 
           OFFSETS_B, OFFSETS_R, OFFSETS_D]


if __name__ == "__main__":
    s = StickersCube()
    print(s.validate_stickers())
    cube = s.get_cube()
    print(cube.state)