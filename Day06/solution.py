import copy

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

    def __hash__(self) -> int:
        return hash(self.i) + hash(self.j) + hash(self.d)

    def __eq__(self, other: "Position") -> bool:
        if not isinstance(other, Position):
            return False
        return hash(self) == hash(other)

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
        return self.i < bounds[0] and self.j < bounds[1]


class Solver(BaseSolver):

    __slots__ = ["_path"]

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run_path(self, added_obstacle: list | None = None) -> list:
        # get obstacle coords
        obs_i, obs_j = np.where(self.array == "#")
        # numpy int repr is ugly, convert
        obstacles = list(zip([int(i) for i in obs_i], [int(j) for j in obs_j]))
        print("obstacle list:")
        print(obstacles)

        # area boundaries
        # if coord == bound, we're outside
        imax, jmax = self.array.shape
        print(f"area bounds: {imax}, {jmax}")

        # starting location
        ui, uj = np.where(self.array == "^")
        # create an initial position
        pos = Position(int(ui[0]), int(uj[0]), "n")
        # step through all positions until we walk out of bounds
        path = []
        while pos.in_bounds(bounds=[imax, jmax]):
            path.append(pos)
            pos = pos.next(obstacles=obstacles)

        return path

    def run(self) -> int:
        path = self.run_path()
        # ooh nice display
        display = copy.deepcopy(self.array)
        for pos in path:
            display[pos.i, pos.j] = pos.d
        print(display)

        # now we need to get the count of all positions that were _touched_
        # NOT the total step count, since we're counting a rotation there
        checked = []
        for pos in path:
            if pos.location not in checked:
                checked.append(pos.location)

        return len(checked)

    def find_loops(self) -> int:
        """
        brute force yeeee
        """


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")

    test_1_run = test_1.run()

    assert test_1_run == 41, test_1_run

    print("Running part 1")
    sol = Solver(inp="Input/input.txt")

    print(f"Part 1 solution: {sol.run()}")
