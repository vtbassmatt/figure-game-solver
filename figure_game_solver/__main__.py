from .solver import Board, Solver

if __name__ == '__main__':

    b = Board()
    b.print()
    print()

    s = Solver(b)

    # start at 15 so we get at least some output
    # the solution should be length 10
    s.find_solutions(15)
