import collections
import copy
import math
import time

from lib.base_solver import BaseSolver


class Position:

    __slots__ = ["_i", "_j", "_h", "explored", "_children"]

    def __init__(self, i: int, j: int, h: int):
        self._i = int(i)
        self._j = int(j)
        self._h = int(h)

        self._children = []

        self.explored = False

    def __repr__(self) -> str:
        return f"P({self.i},{self.j},{self.h})"

    def __hash__(self) -> int:
        """
        Uses Cantor's pair enumeration (or "zig-zag" method)

        https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function
        """
        return int(( (self.i + self.j) * (self.i + self.j + 1) / 2 ) + self.i)

    def __eq__(self, other):
        return hash(self) == hash(other)

    @property
    def i(self):
        return self._i

    @property
    def j(self):
        return self._j

    @property
    def h(self):
        return self._h

    def all_adjacent(self, max_i: int, max_j: int):
        adj = []
        if self.i > 0:
            pos = (self.i - 1, self.j)
            adj.append(pos)
        if self.j > 0:
            pos = (self.i, self.j - 1)
            adj.append(pos)
        if self.i < max_i - 1:
            pos = (self.i + 1, self.j)
            adj.append(pos)
        if self.j < max_j - 1:
            pos = (self.i, self.j + 1)
            adj.append(pos)

        return adj


def bfs(array: list[list[Position]], node: Position) -> list[Position]:
    queue = collections.deque()
    queue.append(node)

    max_i = len(array)
    max_j = len(array[0])

    explored = []
    while len(queue) > 0:
        test = queue.popleft()

        # print(f"testing {test}, {test.h}")
        adj = [array[pos[0]][pos[1]] for pos in test.all_adjacent(max_i, max_j)]

        for node in adj:
            if not node.explored and node.h == test.h + 1:
                # print(f"marking node {node}")
                node.explored = True
                queue.append(node)
                explored.append(node)

    return explored


def dfs(array: list[list[Position]], node: Position, full_search: bool = False) -> list[Position]:
    if not full_search:
        node.explored = True

    max_i = len(array)
    max_j = len(array[0])

    adj = [array[pos[0]][pos[1]] for pos in node.all_adjacent(max_i, max_j)]
    traversed = [node]
    for test in adj:
        if not test.explored and test.h == node.h + 1:
            if node not in traversed:
                traversed.append(test)
            traversed += dfs(array, test, full_search)

    return traversed


class Solver(BaseSolver):

    __slots__ = ["_points_array"]

    def __init__(self, inp: str):
        super().__init__(inp=inp)

        self._points_array = None

    @property
    def pos_array(self) -> list[list[Position]]:
        if self._points_array is not None:
            return self._points_array

        self._points_array = []
        for i in range(self.array.shape[0]):
            tmp = []
            for j in range(self.array.shape[1]):
                tmp.append(Position(i, j, self.array[i, j]))
            self._points_array.append(tmp)

        return self._points_array

    def run(self, full_search: bool):
        points = self.pos_array

        heads = self.points_where("0")
        # peaks = self.points_where("9")

        peaks = 0
        for loc in heads:
            first = points[loc[0]][loc[1]]

            dfs_path = dfs(copy.deepcopy(self.pos_array), first, full_search=full_search)

            # print(self.regenerate_coloured_text(self.array, colours={
            #     "green": [(first.i, first.j)],
            #     "red": pth,
            #     "blue": pks,
            # }))

            for node in dfs_path:
                if node.h == 9:
                    peaks += 1

        return peaks


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")
    test_1_run = test_1.run(full_search=False)
    assert test_1_run == 36, test_1_run

    test_2 = Solver(inp="Input/input_test.txt")
    test_2_run = test_2.run(full_search=True)
    assert test_2_run == 81, test_2_run

    sol = Solver(inp="Input/input.txt")
    print("Running Part 1")
    t0 = time.perf_counter()
    part_1 = sol.run(full_search=False)
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")

    sol = Solver(inp="Input/input.txt")
    print("Running Part 2")
    t0 = time.perf_counter()
    part_2 = sol.run(full_search=True)
    print(f"Part 2 result: {part_2} {time.perf_counter() - t0:.3f}s")
