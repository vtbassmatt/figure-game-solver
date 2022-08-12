from .solver import Board

if __name__ == '__main__':
    b = Board()
    b.print()
    print()

    # clear column 0
    b.click(0)
    b.click(0)
    b.click(0)
    b.print()
    print(b.is_solved())
    print()

    # clear column 1
    b.click(1)
    b.click(1)
    b.click(1)
    b.click(1)
    b.click(1)
    b.print()
    print(b.is_solved())
    print()

    # # clear column 2
    b.click(2)
    b.click(2)
    b.print()
    print(b.is_solved())
    print()

    # # clear column 3
    b.click(3)
    b.click(3)
    b.click(3)
    b.print()
    print(b.is_solved())
    print()

    # # clear column 4
    b.click(4)
    b.click(4)
    b.print()
    print(b.is_solved())
    print(b.solution())
