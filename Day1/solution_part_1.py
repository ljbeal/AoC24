import time


class Solver:

    __slots__ = ["_perf", "_inp", "_data", "_sorted"]

    def __init__(self, inp: str):
        """
        Solver for Day 1 of AoC

        Args:
             inp (str): Path for input file
        """
        t0 = time.perf_counter()
        self._perf = {}

        self._inp = inp
        self._data = None
        self._sorted = False  # flag True if lists are sorted

        self._perf["init"] = time.perf_counter() - t0

    @property
    def lists(self) -> dict:
        """
        Returns a dict of the two lists

        Uses a local cache for repeated calls

        Returns:
             dict: {"l": [list], "r": [list]}
        """
        t0 = time.perf_counter()
        if self._data is not None:
            # if the cache exists, return that instead
            self._perf["list_get"] += time.perf_counter() - t0
            return self._data

        with open(self._inp, "r") as o:
            rows = o.readlines()

        lists = {
            "l": [],
            "r": [],
        }
        for row in rows:
            # rows are double spaced integers
            # e.g 10001  10002
            # integers are always 5 figure, but it feels
            # better to generalise to any length

            l, r = [item for item in row.strip().split(" ") if item != ""]
            lists["l"].append(int(l))
            lists["r"].append(int(r))
        # cache the data
        self._data = lists

        self._perf["list_get"] = time.perf_counter() - t0
        return lists

    @property
    def sorted_lists(self) -> dict:
        """
        return the left and right lists, sorted
        """
        t0 = time.perf_counter()
        if self._sorted:
            self._perf["list_sort"] += time.perf_counter() - t0
            return self._data

        self._data["l"] = sorted(self.lists["l"])
        self._data["r"] = sorted(self.lists["r"])

        self._sorted = True
        self._perf["list_sort"] = time.perf_counter() - t0
        return self._data

    def run(self) -> int:
        """Run the solution"""
        t0 = time.perf_counter()
        result = 0

        list_l = self.sorted_lists["l"]
        list_r = self.sorted_lists["r"]
        for a, b in zip(list_l, list_r):
            result += abs(a - b)

        self._perf["run"] = time.perf_counter() - t0
        return result

    def print_perf_info(self):
        for step, dt in self._perf.items():
            print(f"step: {step}, {dt:.2f}s")


if __name__ == "__main__":
    test_run = Solver("./Input/input_test.txt")

    assert test_run.run() == 11

    slv = Solver("./Input/input.txt")

    result = slv.run()

    print(f"result: {result}")
    slv.print_perf_info()
