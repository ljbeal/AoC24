from lib.base_solver import BaseSolver


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")
