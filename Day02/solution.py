"""
Day 2 Solution
"""
import copy
from ast import Index

from lib.base_solver import BaseSolver


class Solver(BaseSolver):
    """
    Read in levels and check safety
    """
    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def get_safety(
        self,
        dampener: bool = False,
    ) -> list[bool]:
        """Extract safety levels in accordance with rules"""

        def pairwise_compare(u: int, v: int, increasing: bool):
            """Compare 2 levels, applying rules"""
            # we're increasing, expecting v to be greater than u
            if increasing and u > v:
                return False
            if not increasing and u < v:
                return False
            dv = abs(u - v)
            if dv > 3:
                return False
            if dv < 1:
                return False
            return True

        def test_rules(levels_test, local_dampener):
            """
            Inner function to test rules:

            1. Levels must be either all increasing or decreasing. No inflections
                This can probably be done with a 2nd order derivative, also
            2. Adjacent levels must differ by no more than 3, and no less than 1
            """
            # print(f"\ntesting levels: {levels}")
            increasing = levels_test[0] < levels_test[1]

            for i in range(len(levels_test) - 1):
                # get two values to compare
                u = levels_test[i]
                v = levels_test[i + 1]

                safe = pairwise_compare(u, v, increasing)

                if not safe:
                    if local_dampener:
                        # oh god
                        recursive = []
                        for j in range(len(levels_test)):
                            tmp = copy.deepcopy(levels_test)
                            del tmp[j]
                            recursive.append(test_rules(tmp, local_dampener=False))

                        if not any(recursive):
                            return False
                    else:
                        return False

            return True

        output = []
        for report in self.data.split("\n"):
            # get integer levels of each report
            levels = [int(level) for level in report.strip().split(" ")]
            output.append(test_rules(levels, local_dampener=dampener))

        return output

    def total_safe(self) -> int:
        """Solution to part 1, returns a count of the number of safe reports"""
        # summation of bools is equivalent to counting the True
        return sum(self.get_safety(dampener=False))

    def total_damped_safe(self) -> int:
        """Solution to part 1, returns a count of the number of safe reports"""
        # summation of bools is equivalent to counting the True
        return sum(self.get_safety(dampener=True))


if __name__ == "__main__":
    test = Solver("Input/input_test.txt")

    print("verify part 1")
    test_1 = test.total_safe()
    assert test_1 == 2, test_1
    print("verify part 2")
    test_2 = test.total_damped_safe()
    assert test_2 == 4, test_2

    solution = Solver("Input/input.txt")

    print(f"Day 2, part 1 solution: {solution.total_safe()}")
    print(f"Day 2, part 1 solution: {solution.total_damped_safe()}")
