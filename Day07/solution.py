import itertools
import math
import time

from lib.base_solver import BaseSolver


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self, concat: bool = False):

        achievable = []
        for row in self.rows:
            target, input = row.split(":")

            target = int(target)
            input = [int(item.strip()) for item in input.split(" ") if item.strip() != ""]

            # print(f"Assessing inputs: {input} for target {target}")

            # max_reachable = math.prod(input)
            # the "largest" operation we can do is multiplication
            # therefore the largest number we can achieve is the product of the list
            # throw these out before wasting calculations on them
            # if max_reachable < target:
            #     print(f"\tTarget {target} cannot be reached")
            #     continue
            # NOTE: this actually does not work
            # we can prove this trivially with the numbers:
            # [100, 1]
            # prod = 100, sum = 101
            # That trailing +1 trips up the prod method

            # now "brute force" with permutations
            available_ops = ["+", "*"]
            if concat:
                available_ops.append("||")

            operations = itertools.product(available_ops, repeat=len(input)-1)

            for opset in operations:
                # print(f"\tperforming: {opset}. Result:", end=" ")

                tmp = input[0]
                for idx in range(len(input) - 1):
                    v = input[idx + 1]
                    op = opset[idx]

                    if op == "+":
                        tmp += v
                    elif op == "*":
                        tmp *= v
                    elif op == "||":
                        tmp = int(f"{tmp}{v}")

                # print(tmp)
                if tmp == target:
                    # print(f"\tTarget Achieved, storing {target}")
                    achievable.append(target)
                    break

        return sum(achievable)


if __name__ == "__main__":

    test = Solver(inp="Input/input_test.txt")

    t0 = time.perf_counter()
    test_1_run = test.run()
    print(f"Part 1 test, {time.perf_counter() - t0:.3f}s")
    assert test_1_run == 3749, test_1_run

    t0 = time.perf_counter()
    test_2_run = test.run(concat=True)
    print(f"Part 1 test, {time.perf_counter() - t0:.3f}s")
    assert test_2_run == 11387, test_2_run



    sol = Solver(inp="Input/input.txt")

    print("Running Part 1")
    t0 = time.perf_counter()

    part_1 = sol.run()
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")

    print("Running Part 2")
    t0 = time.perf_counter()

    part_2 = sol.run(concat=True)
    print(f"Part 2 result: {part_2} {time.perf_counter() - t0:.3f}s")
