import numpy as np


class BaseSolver:

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

    @property
    def rows(self):
        return self.data.split("\n")

    def points_where(self, test: str) -> list[tuple[int, int]]:
        """
        returns a list of points where array==test

        Args:
            test (Any):
                item to test against

        Returns:
            list of points
        """
        x, y = np.where(self.array == test)

        return list(zip([int(point) for point in x], [int(point) for point in y]))

    def check_inside_bounds(self, points: tuple[int, int]) -> bool:
        # assert that we have positive coords
        if not points[0] * points[1] >= 0 or not points[0] + points[1] >= 0:
            return False

        if not points[0] < self.array.shape[0]:
            return False

        if not points[1] < self.array.shape[1]:
            return False

        return True

    @staticmethod
    def regenerate_text(array: np.array, spacing: int = 0) -> str:
        """
        Regenerate the string input from a 2D array

        Args:
            array (np.array):
                array to process
            spacing (int):
                extra whitespace between points

        Returns:
            str: formatted array
        """
        joinchar = " " * (spacing + 1)
        return "\n".join([joinchar.join(row) for row in array])

    def regenerate_coloured_text(
            self,
            array: np.array,
            spacing = 0,
            coloured_red: list[tuple[int, int]] | None = None,
            coloured_grn: list[tuple[int, int]] | None = None,
    ):
        if coloured_red and coloured_grn is None:
            return self.regenerate_text(array, spacing)

        joinchar = " " * (spacing + 1)

        output = []
        for i, row in enumerate(array):
            tmp = []
            for j, col in enumerate(row):
                item = array[i, j]

                if (i, j) in coloured_red:
                    tmp.append(f"\033[91m{item}\033[00m")
                elif (i, j) in coloured_grn:
                    tmp.append(f"\033[92m{item}\033[00m")
                else:
                    tmp.append(item)
            output.append(joinchar.join(tmp))
        return "\n".join(output)
