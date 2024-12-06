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
