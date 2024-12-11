import time

from lib.base_solver import BaseSolver


class Stone:

    __slots__ = ["_num"]

    def __init__(self, num: int | None = None):
        self._num = num or 0

    def __repr__(self):
        return f"({self.num})"

    @property
    def num(self) -> int:
        return self._num

    def blink(self) -> list["Stone"]:
        if self.num == 0:
            return [Stone(1)]
        if len(str(self.num)) % 2 == 0:
            string = str(self.num)
            mid = int(len(string) / 2)
            return [Stone(int(string[:mid])), Stone(int(string[mid:]))]
        return [Stone(self.num * 2024)]


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self) -> int:
        stones = [Stone(int(num)) for num in self.data.split(" ")]

        for blink in range(25):
            tmp = []
            for stone in stones:
                tmp += stone.blink()
            stones = tmp
            print(stones)

        return len(stones)


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")

    test_1_run = test_1.run()

    assert test_1_run == 55312, test_1_run

    sol = Solver(inp="Input/input.txt")

    print("Running Part 1")
    t0 = time.perf_counter()

    part_1 = sol.run()
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")
