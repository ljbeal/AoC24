import itertools
import math
import time

from lib.base_solver import BaseSolver


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self):

        achievable = []
        for row in self.rows:
            target, input = row.split(":")

            target = int(target)
            input = [int(item.strip()) for item in input.split(" ") if item.strip() != ""]

            print(f"Assessing inputs: {input} for target {target}")
            throw = False
            max_reachable = math.prod(input)
            # the "largest" operation we can do is multiplication
            # therefore the largest number we can achieve is the product of the list
            # throw these out before wasting calculations on them
            if max_reachable < target:
                print(f"\tTarget {target} cannot be reached")
                # continue
                throw = True

            # now "brute force" with permutations
            operations = itertools.product(["+", "*"], repeat=len(input)-1)

            for opset in operations:
                print(f"\tperforming: {opset}. Result:", end=" ")

                tmp = input[0]
                for idx in range(len(input) - 1):
                    v = input[idx + 1]
                    op = opset[idx]

                    if op == "+":
                        tmp += v
                    else:
                        tmp *= v

                print(tmp)
                if tmp == target:
                    print(f"\tTarget Achieved, storing {target}")
                    achievable.append(target)

                    if throw:
                        exit()
                    break

        return sum(achievable)



if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")

    t0 = time.perf_counter()
    test_1_run = test_1.run()

    print(f"Part 1 test, {time.perf_counter() - t0:.3f}s")
    assert test_1_run == 3749, test_1_run

    sol = Solver(inp="Input/input.txt")

    print("Running Part 1")
    t0 = time.perf_counter()

    part_1 = sol.run()
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")
