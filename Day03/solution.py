import re


class Solver:
    def __init__(self, inp: str):
        with open(inp, "r", encoding="utf8") as o:
            self._data = o.read()

    @property
    def data(self) -> str:
        return self._data

    def run(self, flow: bool) -> int:
        """
        Run the day 3 solution

        Args:
            flow:
                enable the flow control of part 2
        """
        # first, get each pair and extract the integers and their location index
        instruct_mul = {}
        for mul in re.finditer(r"mul\((\d*),(\d*)\)", self.data):
            instruct_mul[mul.start(0)] = (mul.group(1), mul.group(2))
        # generate a list of "breakpoints" where multiplication should be turned on or off
        # but only if flow control is enabled
        do = []
        dont = []
        if flow:
            for m in re.finditer(r"do\(\)", self.data):
                do.append(m.start(0))

            for m in re.finditer(r"don't\(\)", self.data):
                dont.append(m.start(0))
        # keep a running total, summing all valid mul(a,b) strings
        sum = 0
        enable = True  # start with addition enabled
        for idx, pair in instruct_mul.items():
            # consume do and dont lists, enabling or disabling as wed go
            if len(do) > 0 and idx > do[0]:
                enable = True
                del do[0]
            if len(dont) > 0 and idx > dont[0]:
                enable = False
                del dont[0]
            # if we can, sum
            if enable:
                sum += int(pair[0]) * int(pair[1])

        return sum


if __name__ == "__main__":
    test = Solver("Input/input_test_2.txt")
    test_1 = test.run(flow=False)
    assert test_1 == 161

    test = Solver("Input/input_test_2.txt")
    test_2 = test.run(flow=True)
    assert test_2 == 48

    print("run part 1")
    sol = Solver("Input/input.txt")

    print(f"part 1 solution: {sol.run(flow=False)}")

    print("run part 2")
    print(f"part 2 solution: {sol.run(flow=True)}")
