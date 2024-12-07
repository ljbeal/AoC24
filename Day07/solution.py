import math

from lib.base_solver import BaseSolver


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self):
        for row in self.rows:
            target, input = row.split(":")

            target = int(target)
            input = [int(item.strip()) for item in input.split(" ") if item.strip() != ""]

            max_reachable = math.prod(input)
            # the "largest" operation we can do is multiplication
            # therefore the largest number we can achieve is the product of the list
            # throw these out before wasting calculations on them
            if max_reachable < target:
                print(f"Target {target} cannot be reached")
                continue


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")

    test_1_run = test_1.run()

    assert test_1_run == 0, test_1_run
