import collections

import numpy as np

from Day10.solution import Solver


class BFS:

    __slots__ = ["_array", "_queue"]

    def __init__(self, array: np.array):
        self._array = array
        self._queue = collections.deque()

    def search(self, head: tuple[int, int]):
        self._queue.append(head)

        explored = []
        while len(self._queue) > 0:
            test = self._queue.popleft()

            adj = self.get_adjacent(test)

            for node in adj:
                if node not in explored and self.extra_condition(node, test):
                    self._queue.append(node)
                    explored.append(node)

        return explored

    def get_adjacent(self, point: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Gets cardinally adjacent points

        Ignores diagonal for now, but we may add a flag for this
        """
        max_i = self._array.shape[0]
        max_j = self._array.shape[1]
        adj = []
        if point[0] > 0:
            pos = (point[0] - 1, point[1])
            adj.append(pos)
        if point[1] > 0:
            pos = (point[0], point[1] - 1)
            adj.append(pos)
        if point[0] < max_i - 1:
            pos = (point[0] + 1, point[1])
            adj.append(pos)
        if point[1] < max_j - 1:
            pos = (point[0], point[1] + 1)
            adj.append(pos)

        return adj

    def value(self, point: tuple[int, int]):
        return self._array[point[0], point[1]]

    def extra_condition(self, node: tuple[int, int], test: tuple[int, int]) -> bool:
        return True


if __name__ == "__main__":
    class HeightSearch(BFS):
        def extra_condition(self, node: tuple[int, int], test: tuple[int, int]) -> bool:
            return self.value(node) == self.value(test) + 1

    # use day 10 data for testing

    data = Solver(inp="../Day10/Input/input_test.txt")

    first = data.points_where("0")[0]

    print(data.regenerate_coloured_text(data.array, colours={"blue": [first]}))

    search = HeightSearch(array=data.array.astype(int))

    result = search.search(first)

    print(result)
    print(len(result))

    print(data.regenerate_coloured_text(data.array, colours={"blue": [first], "red": result}))
