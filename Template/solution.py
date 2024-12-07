from lib.base_solver import BaseSolver


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self):
        return NotImplemented


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")

    test_1_run = test_1.run()

    assert test_1_run == 0, test_1_run
