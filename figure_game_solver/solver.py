from collections import ChainMap
from enum import Enum, auto


class EmptyColumn(UserWarning):
    def __init__(self, column=None):
        if column:
            self.column = column


class Cell(Enum):
    Magenta = auto()
    Yellow = auto()
    Cyan = auto()
    White = auto()


class Board:
    def __init__(self):
        # puzzle 46
        self.base_puzzle = (
            # first column, bottom to top
            (Cell.Magenta, Cell.Magenta, Cell.Yellow,  Cell.Magenta, Cell.Magenta),
            (Cell.Cyan,    Cell.White,   Cell.Cyan,    Cell.White,   Cell.Magenta),
            (Cell.Magenta, Cell.Cyan,    Cell.White,   Cell.White,   Cell.White),
            (Cell.Cyan,    Cell.White,   Cell.Magenta, Cell.Cyan,    Cell.White),
            # last column, bottom to top
            (Cell.Magenta, Cell.White,   Cell.Magenta, Cell.Cyan,    Cell.Cyan),
        )
        self.puzzle = ChainMap(self.base_puzzle)
    
    def _remove_matches(self, column):
        for i in range(1, len(self.puzzle[column])):
            if self.puzzle[column][i] != self.puzzle[column][0]:
                return self.puzzle[column][i:]
        return []
    
    def click(self, column):
        "Click on a column to remove the bottom cell and same-column same-color cells."
        if len(self.puzzle[column]) == 0:
            raise EmptyColumn(column)
        new_col = self._remove_matches(column)
        self.puzzle = self.puzzle.new_child({column: new_col})
    
    def unclick(self):
        "Remove the last click."
        if len(self.puzzle.maps) > 1:
            self.puzzle = self.puzzle.parents
        else:
            raise IndexError("There's nothing to unclick")
    
    def print(self):
        cols = len(self.base_puzzle)
        rows = len(self.base_puzzle[0])
        for row in range(rows - 1, -1, -1):
            for col in range(cols):
                try:
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
                except IndexError:
                    print('  ', end='')
            print('')
