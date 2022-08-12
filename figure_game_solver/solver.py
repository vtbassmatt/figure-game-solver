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
    
    @property
    def cols(self):
        return len(self._base_puzzle)
    
    @property
    def rows(self):
        return len(self._base_puzzle[0])
    
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
    
    @property
    def is_solved(self):
        "Determine if the puzzle has been solved."
        for row in self._puzzle:
            if len(self._puzzle[row]) > 0:
                return False
        return True
    
    @property
    def current_path(self):
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


class Solver:
    def __init__(self, board: Board):
        self._board = board
        self._solutions = []
        self._shortest_solution = board.cols * board.rows

    def find_solutions(self, max_length: int):
        self._find_solutions(0, max_length)
    
    def _find_solutions(self, depth, max_depth):
        if depth > max_depth: return

        b = self._board
        for col in range(b.cols):
            for _ in range(b.rows):

                # we might have found a shorter solution in the last
                # iteration, so we return from inside the loop
                if depth >= self._shortest_solution:
                    return

                try:
                    b.click(col)
                except EmptyColumn:
                    continue

                if b.is_solved:
                    if len(b.current_path) < self._shortest_solution:
                        print(b.current_path)
                        self._solutions.append(b.current_path)
                        self._shortest_solution = len(b.current_path)
                else:
                    self._find_solutions(depth+1, max_depth)

                b.unclick()


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
