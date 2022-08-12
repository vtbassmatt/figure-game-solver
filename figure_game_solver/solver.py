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
        self._base_puzzle = (
            # first column, bottom to top
            (Cell.Magenta, Cell.Magenta, Cell.Yellow,  Cell.Magenta, Cell.Magenta),
            (Cell.Cyan,    Cell.White,   Cell.Cyan,    Cell.White,   Cell.Magenta),
            (Cell.Magenta, Cell.Cyan,    Cell.White,   Cell.White,   Cell.White),
            (Cell.Cyan,    Cell.White,   Cell.Magenta, Cell.Cyan,    Cell.White),
            # last column, bottom to top
            (Cell.Magenta, Cell.White,   Cell.Magenta, Cell.Cyan,    Cell.Cyan),
        )
        self._puzzle = ChainMap(dict(enumerate(self._base_puzzle)))
        self._clicks = []
    
    def _remove_matches(self, column):
        # make a (mutable) copy of the last layer
        new_layer = { k: list(v) for k, v in self._puzzle.items() }
        # flood-fill adjacent same-color cells with None
        _flood_fill(new_layer, column, 0, self._puzzle[column][0], None)
        # filter the Nones out
        for col in new_layer.keys():
            new_layer[col] = [x for x in new_layer[col] if x is not None]
        return new_layer
    
    def click(self, column):
        "Click on a column to remove the bottom cell and adjacent same-color cells."
        if len(self._puzzle[column]) == 0:
            raise EmptyColumn(column)
        self._clicks.append(column)
        new_layer = self._remove_matches(column)
        self._puzzle = self._puzzle.new_child(new_layer)
    
    def unclick(self):
        "Remove the last click."
        if len(self._puzzle.maps) > 1:
            self._clicks.pop()
            self._puzzle = self._puzzle.parents
        else:
            raise IndexError("There's nothing to unclick")
    
    def is_solved(self):
        "Determine if the puzzle has been solved."
        for row in self._puzzle:
            if len(self._puzzle[row]) > 0:
                return False
        return True
    
    def solution(self):
        if self.is_solved():
            return list(self._clicks)
    
    def print(self):
        cols = len(self._base_puzzle)
        rows = len(self._base_puzzle[0])
        for row in range(rows - 1, -1, -1):
            for col in range(cols):
                try:
                    match self._puzzle[col][row]:
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


def _flood_fill(grid, col, row, match, to):
    if len(grid[col]) > row and grid[col][row] == match:
        grid[col][row] = to
        if col > 0:
            _flood_fill(grid, col - 1, row, match, to)
        if col < len(grid) - 1:
            _flood_fill(grid, col + 1, row, match, to)
        if row > 0:
            _flood_fill(grid, col, row - 1, match, to)
        if row < len(grid[col]) - 1:
            _flood_fill(grid, col, row + 1, match, to)
