import copy
import itertools
import time

import numpy as np

from lib.base_solver import BaseSolver


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self):
        block = [".", "\n"]
        freqlist = [char for char in list(set(self.data)) if char not in block]

        print(f"total list of frequencies: {freqlist}")
        print(f"array shape: {self.array.shape}")

        new_locations = []
        for freq in freqlist:
            # locations for this frequency
            points = self.points_where(freq)
            # every pair combo
            pairs = list(itertools.combinations(points, 2))

            for pair in pairs:
                di = pair[0][0] - pair[1][0]
                dj = pair[0][1] - pair[1][1]

                pos = (pair[0][0] + di, pair[0][1] + dj)
                neg = (pair[1][0] - di, pair[1][1] - dj)

                display = np.full_like(self.array, ".")
                display[pair[0][0], pair[0][1]] = "!"
                display[pair[1][0], pair[1][1]] = "!"

                if self.check_inside_bounds(pos):
                    new_locations.append(pos)
                    display[pos[0], pos[1]] = "#"
                if self.check_inside_bounds(neg):
                    new_locations.append(neg)
                    display[neg[0], neg[1]] = "#"

        # get unique locations
        display = copy.deepcopy(self.array)
        for loc in new_locations:
            display[loc[0], loc[1]] = "#"
        print(self.regenerate_text(display, spacing=1))

        reduction = np.unique(display, return_counts=True)

        return reduction[1][list(reduction[0]).index("#")]


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")

    test_1_run = test_1.run()

    assert test_1_run == 14, test_1_run

    sol = Solver(inp="Input/input.txt")

    print("Running Part 1")
    t0 = time.perf_counter()

    part_1 = sol.run()
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")
