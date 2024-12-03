import re


class Solver:
    def __init__(self, inp: str):
        with open(inp, "r", encoding="utf8") as o:
            self._data = o.readlines()

    @property
    def data(self):
        return self._data

    def run(self) -> int:
        match = re.compile(r"mul\((\d*),(\d*)\)")

        sum = 0
        for line in self.data:
            # collects a list of (a, b) pairs from each mul(a,b) group
            pairs = re.findall(match, line)

            for pair in pairs:
                a, b = pair

                sum += int(a) * int(b)

        return sum


if __name__ == "__main__":
    test = Solver("Input/input_test.txt")
    assert test.run() == 161

    print("run part 1")
    sol = Solver("Input/input.txt")

    print(f"part 1 solution: {sol.run()}")
