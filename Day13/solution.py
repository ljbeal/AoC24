import time

from lib.base_solver import BaseSolver


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self):
        return NotImplemented


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")
    test_1_run = test_1.run()
    assert test_1_run == 100, test_1_run

    # test_2 = Solver(inp="Input/input_test.txt")
    # test_2_run = test_2.run()
    # assert test_2_run == 0, test_2_run

    sol = Solver(inp="Input/input.txt")
    print("Running Part 1")
    t0 = time.perf_counter()
    part_1 = sol.run()
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")

    # sol = Solver(inp="Input/input.txt")
    # print("Running Part 2")
    # t0 = time.perf_counter()
    # part_2 = sol.run()
    # print(f"Part 2 result: {part_2} {time.perf_counter() - t0:.3f}s")
