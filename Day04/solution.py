import re
from typing import Union

import numpy as np
from tomlkit import register_encoder


class Solver:

    __slots__ = ["_data"]

    def __init__(self, inp: str):
        with open(inp, "r", encoding="utf8") as o:
            self._data = o.read()

    @property
    def data(self) -> str:
        return self._data

    def run(self) -> int:
        # use a sliding window to search. This window can be 4x1, 1x4 or 4x4 (diag)
        # convert string data into a numpy array
        array = [list(line.strip()) for line in self.data.split("\n")]
        # create transposed array, since numpy coordinate systems are y,x
        array = np.array(array)

        # horizontal search
        count = self.findall(self.data)  # no reason to regenerate the text here
        # vertical search
        count += self.findall(array.T)

        # for the diagonals, we can simulate this by padding the array and rolling it by index
        pad = np.concat((array.T, np.full_like(array, " ")), axis=1)

        diag_down = []
        for idx, row in enumerate(pad):
            diag_down.append(np.roll(row, idx))

        diag_down = np.array(diag_down).T

        count += self.findall(diag_down)

        # diag_up
        pad = np.concat((np.full_like(array, " "), array.T), axis=1)
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


if __name__ == "__main__":
    test = Solver("Input/input_test.txt")

    test_1 = test.run()

    assert test_1 == 18, test_1

    solv = Solver("Input/input.txt")

    print(f"part 1 solution: {solv.run()}")
