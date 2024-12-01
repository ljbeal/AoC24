"""
Solution for Day 1 Part 1
"""
import bisect
import time


class Solver:
    """
    Main Solver Class
    """

    __slots__ = ["_perf", "_inp", "_data"]

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

        self._perf["init"] = time.perf_counter() - t0

    @property
    def lists(self) -> dict:
        """
        Returns a dict of the two lists (sorted)

        Uses a local cache for repeated calls

        Returns:
             dict: {"l": [list], "r": [list]}
        """
        t0 = time.perf_counter()
        if self._data is not None:
            # if the cache exists, return that instead
            self._perf["list_get"] += time.perf_counter() - t0
            return self._data

        with open(self._inp, "r", encoding="utf8") as o:
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

            int_l, int_r = [int(item) for item in row.strip().split(" ") if item != ""]

            id_l = bisect.bisect(lists["l"], int_l)
            lists["l"].insert(id_l, int_l)

            id_r = bisect.bisect(lists["r"], int_r)
            lists["r"].insert(id_r, int_r)

        # cache the data
        self._data = lists

        self._perf["list_get"] = time.perf_counter() - t0
        return lists

    def run(self) -> int:
        """Run the solution"""
        t0 = time.perf_counter()
        result = 0

        list_l = self.lists["l"]
        list_r = self.lists["r"]
        for a, b in zip(list_l, list_r):
            result += abs(a - b)

        self._perf["run"] = time.perf_counter() - t0
        return result

    def print_perf_info(self) -> None:
        """Prints a dict of performance info"""
        for step, dt in self._perf.items():
            print(f"step: {step}, {dt:.2f}s")


if __name__ == "__main__":
    test_run = Solver("./Input/input_test.txt")

    assert test_run.run() == 11

    slv = Solver("./Input/input.txt")

    print(f"result: {slv.run()}")
    slv.print_perf_info()
