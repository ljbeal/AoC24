import re
from typing import Union

import numpy as np


class Solver:

    __slots__ = ["_data", "_array"]

    def __init__(self, inp: str):
        with open(inp, "r", encoding="utf8") as o:
            self._data = o.read()

        self._array = None

    @property
    def data(self) -> str:
        return self._data

    @property
    def array(self):
        if self._array is not None:
            return self._array

        # convert string data into a numpy array
        array = [list(line.strip()) for line in self.data.split("\n")]
        # create transposed array, since numpy coordinate systems are y,x
        self._array = np.array(array)
        return self._array

    def run(self) -> int:
        # use a sliding window to search. This window can be 4x1, 1x4 or 4x4 (diag)
        # horizontal search
        count = self.findall(self.data)  # no reason to regenerate the text here
        # vertical search
        count += self.findall(self.array.T)

        # for the diagonals, we can simulate this by padding the array and rolling it by index
        pad = np.concat((self.array.T, np.full_like(self.array, " ")), axis=1)

        diag_down = []
        for idx, row in enumerate(pad):
            diag_down.append(np.roll(row, idx))

        diag_down = np.array(diag_down).T

        count += self.findall(diag_down)

        # diag_up
        pad = np.concat((np.full_like(self.array, " "), self.array.T), axis=1)
        diag_up = []
        for idx, row in enumerate(pad):
            diag_up.append(np.roll(row, -idx))

        diag_up = np.array(diag_up).T

        with open("Input/skew_test.txt", "w+") as o:
            o.write(self.regenerate_text(diag_up))

        count += self.findall(diag_up)

        return count

    def regenerate_text(self, array: np.array) -> str:
        """Regenerate the string input from a 2D array"""
        return "\n".join(["".join(row) for row in array])

    def findall(self, string: Union[str, "np.array"]) -> int:
        """Find all XMAS/SAMX instances"""
        if not isinstance(string, str):
            string = self.regenerate_text(string)

        return len(re.findall(r"XMAS", string)) + len(re.findall("SAMX", string))


class Solver2(Solver):
    """Part 2 is different enough that it requires a different approach"""
    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self) -> int:
        # use a 3x3 window centered on each A instance

        coords = zip(*np.where(self.array == "A"))

        count = 0
        for point in coords:
            x, y = [int(p) for p in point]

            # throw out any values on the edge
            if x in (0, self.array.shape[1] - 1):
                continue
            if y in (0, self.array.shape[0] - 1):
                continue

            window = self.array[x-1:x+2,y-1:y+2]
            # possible X-MAS states:
            # M   S | M   M | S   S | S   M
            #   A   |   A   |   A   |   A
            # M   S | S   S | M   M | S   M

            # first corner invalid, easy throw
            tl = str(window[0, 0])
            bl = str(window[2, 0])
            tr = str(window[0, 2])
            br = str(window[2, 2])

            joined = "".join((tl, bl, tr, br))

            # print(window)

            if not (joined.count("M") == joined.count("S") == 2):
                # print("\tnot 2M 2S")
                continue

            if tl == br or bl == tr:
                # print("\tequal corners")
                continue

            count += 1

        return count


if __name__ == "__main__":
    test = Solver("Input/input_test.txt")

    test_1_run = test.run()
    assert test_1_run == 18, test_1_run

    test_2 = Solver2("Input/input_test.txt")
    test_2_run = test_2.run()

    assert test_2_run == 9, test_2_run

    solv = Solver("Input/input.txt")
    print(f"part 1 solution: {solv.run()}")

    solv2 = Solver2("Input/input.txt")
    print(f"part 2 solution: {solv2.run()}")
