from cube import Cube

# Colors enum
class Colors:
    WHITE = 0 
    RED = 1
    BLUE = 2
    ORANGE = 3
    GREEN = 4
    YELLOW = 5

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

class StickersCube:
    def __init__(self, state: dict=None):
        if state == None:
            self.state = {
                Subcubes.FLU: [Colors.RED, Colors.BLUE, Colors.YELLOW],
                Subcubes.FRU: [Colors.RED, Colors.GREEN, Colors.YELLOW],
                Subcubes.FLD: [Colors.RED, Colors.BLUE, Colors.WHITE],
                Subcubes.FRD: [Colors.RED, Colors.GREEN, Colors.WHITE],
                Subcubes.BLU: [Colors.ORANGE, Colors.BLUE, Colors.YELLOW],
                Subcubes.BRU: [Colors.ORANGE, Colors.GREEN, Colors.YELLOW],
                Subcubes.FRD: [Colors.ORANGE, Colors.GREEN, Colors.WHITE],
                Subcubes.BLD: [Colors.ORANGE, Colors.BLUE, Colors.WHITE]
            }
        else:
            self.state = state
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
