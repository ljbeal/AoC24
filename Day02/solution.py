"""
Day 2 Solution
"""


class SolverDay2:
    """
    Read in levels and check safety
    """
    __slots__ = ["_data"]

    def __init__(self, inp: str):
        with open(inp, "r", encoding="utf8") as o:
            self._data: list = o.readlines()

    @property
    def data(self):
        """Private data property"""
        return self._data

    def get_safety(
        self,
    ) -> list[bool]:
        """Extract safety levels in accordance with rules"""
        def test_rules(levels_test):
            """
            Inner function to test rules:

            1. Levels must be either all increasing or decreasing. No inflections
                This can probably be done with a 2nd order derivative, also
            2. Adjacent levels must differ by no more than 3, and no less than 1
            """
            # print(f"\ntesting levels: {levels}")
            increasing = levels_test[0] < levels_test[1]

            safe = True
            for i in range(len(levels_test) - 1):
                # get two values to compare
                u = levels_test[i]
                v = levels_test[i + 1]
                # max and min shifts
                # print(f"testing {u} -> {v}")
                dv = abs(u - v)
                if 1 > dv or dv > 3:
                    # print("\tshift out of bounds")
                    safe = False
                    break

                locally_increasing = u < v
                if increasing is not None:
                    if (increasing and not locally_increasing) or (
                        not increasing and locally_increasing
                    ):
                        # print("\tinflection")
                        safe = False
                        break

            return safe

        output = []
        for report in self.data:
            # get integer levels of each report
            levels = [int(level) for level in report.strip().split(" ")]
            output.append(test_rules(levels))

        return output

    def total_safe(self) -> int:
        """Solution to part 1, returns a count of the number of safe reports"""
        # summation of bools is equivalent to counting the True
        return sum(self.get_safety())


if __name__ == "__main__":
    test = SolverDay2("Input/input_test.txt")

    assert test.total_safe() == 2, test.total_safe()

    solution = SolverDay2("Input/input.txt")

    print(f"Day 2, part 1 solution: {solution.total_safe()}")
