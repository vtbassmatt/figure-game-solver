from enum import Enum, auto

class Cell(Enum):
    Magenta = auto()
    Yellow = auto()
    Cyan = auto()
    White = auto()


class Board:
    def __init__(self):
        # puzzle 46
        self.puzzle = (
            # first column, top to bottom
            (Cell.Magenta, Cell.Magenta, Cell.Yellow,  Cell.Magenta, Cell.Magenta),
            (Cell.Magenta, Cell.White,   Cell.Cyan,    Cell.White,   Cell.Cyan),
            (Cell.White,   Cell.White,   Cell.White,   Cell.Cyan,    Cell.Magenta),
            (Cell.White,   Cell.Cyan,    Cell.Magenta, Cell.White,   Cell.Cyan),
            # last column, top to bottom
            (Cell.Cyan,    Cell.Cyan,    Cell.Magenta, Cell.White,   Cell.Magenta),
        )
    
    def print(self):
        cols = len(self.puzzle)
        rows = len(self.puzzle[0])
        for row in range(rows):
            for col in range(cols):
                match self.puzzle[col][row]:
                    case Cell.Magenta:
                        char = '🔺'
                    case Cell.Yellow:
                        char = '🟡'
                    case Cell.Cyan:
                        char = '🔹'
                    case Cell.White:
                        char = '⬜️'
                print(char, end='')
            print('')
