import copy
import time
from multiprocessing import Pool, cpu_count

import numpy as np

from lib.base_solver import BaseSolver


class Position:

    __slots__ = ["i", "j", "d", "_dirs"]

    def __init__(self, i: int, j: int, d: str):
        self.i = i
        self.j = j

        self._dirs = ["n", "e", "s", "w"]
        if d not in self._dirs:
            raise ValueError(f"Direction must be one of {self._dirs}")
        self.d = d

    def __repr__(self) -> str:
        return f'Position({self.i}, {self.j}, "{self.d}")'

    @property
    def location(self) -> tuple[int, int]:
        return self.i, self.j

    def turn_right(self) -> str:
        """Turn right by stepping through the list of directions"""
        current_direction_id = self._dirs.index(self.d)

        try:
            self.d = self._dirs[current_direction_id + 1]
        except IndexError:
            self.d = self._dirs[0]

        return self.d

    def next(self, obstacles: list[list]) -> "Position":
        """Go to the next position, dictated by position and direction"""
        i_next = self.i
        j_next = self.j
        if self.d == "n":
            i_next -= 1
        elif self.d == "e":
            j_next += 1
        elif self.d == "s":
            i_next += 1
        elif self.d == "w":
            j_next -= 1

        if (i_next, j_next) in obstacles:
            # if we're turning, just turn in place and return that as a step
            nextpos = Position(self.i, self.j, self.d)
            nextpos.turn_right()
        else:
            nextpos = Position(i_next, j_next, self.d)

        return nextpos

    def in_bounds(self, bounds: list[int]):
        return bounds[0] > self.i >= 0 and bounds[1] > self.j >= 0


class Solver(BaseSolver):

    __slots__ = ["_obstacles"]

    def __init__(self, inp: str):
        super().__init__(inp=inp)

        obs_i, obs_j = np.where(self.array == "#")
        # numpy int repr is ugly, convert
        self._obstacles = list(zip([int(i) for i in obs_i], [int(j) for j in obs_j]))

    def run_path(self, added_obstacle: tuple | None = None) -> [list, bool]:
        # get obstacle coords
        obstacles = copy.deepcopy(self._obstacles)
        if added_obstacle is not None:
            obstacles.append(added_obstacle)

        # area boundaries
        # if coord == bound, we're outside
        imax, jmax = self.array.shape

        # starting location
        ui, uj = np.where(self.array == "^")
        # create an initial position
        pos = Position(int(ui[0]), int(uj[0]), "n")
        # step through all positions until we walk out of bounds
        path = [pos]
        cardinal = {
            "n": [pos],
            "e": [],
            "s": [],
            "w": [],
        }
        loop = False
        while True:  # keep stepping
            pos = pos.next(obstacles=obstacles)
            # if we exit the bounds, break
            if not pos.in_bounds(bounds=[imax, jmax]):
                break
            # if the path loops, break
            if (pos.i, pos.j) in cardinal[pos.d]:
                loop = True
                break
            path.append(pos)
            cardinal[pos.d].append((pos.i, pos.j))

        return path, loop

    def run(self) -> int:
        path, loop = self.run_path()
        # now we need to get the count of all positions that were _touched_
        # NOT the total step count, since we're counting a rotation there
        checked = []
        for pos in path:
            if pos.location not in checked:
                checked.append(pos.location)

        return len(checked)

    def find_loops(self) -> int:
        """
        find obstacle locations that create loops
        """
        # loops can only occur when traversing a previously touched spot,
        # where turning right at that intersection would put you back on that path

        base_path, loop = self.run_path()

        new = []
        for pos in base_path:
            new.append((pos.i, pos.j))

        loops = 0
        new = list(set(new))
        for idx, addition in enumerate(new):
            print(f"running with added obstacle {idx+1}/{len(new)}: {addition}")
            path, loop = self.run_path(added_obstacle=addition)

            if loop:
                loops += 1

        # with Pool(cpu_count()) as p:
        #     cache = p.map(self.run_path, new)
        #
        # loops = 0
        # for run in cache:
        #     if run[1]:
        #         loops += 1

        return loops - 1  # exclude the position right in front of the guard


if __name__ == "__main__":

    test = Solver(inp="Input/input_test.txt")

    t0 = time.perf_counter()
    test_1_run = test.run()
    assert test_1_run== 41, test_1_run
    t1 = time.perf_counter()
    print(f"test 1, {t1 - t0:.2f}s")

    test_2_run = test.find_loops()
    assert test_2_run == 6, test_2_run
    t2 = time.perf_counter()
    print(f"test 2, {t2 - t1:.2f}s")

    print("Running part 1")
    sol = Solver(inp="Input/input.txt")

    t0 = time.perf_counter()
    print(f"Part 1 solution: {sol.run()}, {time.perf_counter() - t0:.2f}s")

    print("Running part 2")
    t0 = time.perf_counter()
    print(f"Part 2 solution: {sol.find_loops()}, {time.perf_counter() - t0:.2f}s")
