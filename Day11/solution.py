import functools
import time

from lib.base_solver import BaseSolver


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self, blinks: int) -> int:
        stones = {}
        for stone in self.data.split(" "):
            try_add(stones, int(stone))
        print(stones)

        for blink in range(blinks):
            print(f"processing blink {blink + 1}/{blinks}")

            tmp = {}
            for stone, count in stones.items():
                newstones = blink_stone(stone)

                for num in newstones:
                    try_add(tmp, num, count)

            stones = tmp
            del tmp

        return sum(stones.values())


@functools.cache
def blink_stone(num: int) -> list[int]:
    if num == 0:
        return [1]
    if len(str(num)) % 2 == 0:
        string = str(num)
        mid = int(len(string) / 2)
        return [int(string[:mid]), int(string[mid:])]
    return [num * 2024]


def try_add(cache: dict, num: int, count: int = 1):
    try:
        cache[num] += count
    except KeyError:
        cache[num] = count


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")
    test_1_run = test_1.run(blinks=25)
    assert test_1_run == 55312, test_1_run

    sol = Solver(inp="Input/input.txt")
    print("Running Part 1")
    t0 = time.perf_counter()
    part_1 = sol.run(blinks=25)
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")

    sol = Solver(inp="Input/input.txt")
    print("Running Part 2")
    t0 = time.perf_counter()
    part_2 = sol.run(blinks=75)
    print(f"Part 2 result: {part_2} {time.perf_counter() - t0:.3f}s")
