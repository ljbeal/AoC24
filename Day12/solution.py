import time

import numpy as np

from lib.base_solver import BaseSolver
from lib.bfs import BFS


class FloodFill(BFS):
    def extra_condition(self, node: tuple[int, int], test: tuple[int, int]) -> bool:
        return self.value(node) == self.value(test)


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self):
        types = np.unique(self.array)

        explored = np.full(self.array.shape, 0)

        print(types)

        cost = 0
        for i in range(self.array.shape[0]):
            for j in range(self.array.shape[1]):
                if explored[i, j] == 0:

                    search = FloodFill(self.array)

                    connected = search.search((i, j))

                    explored[i, j] = 1
                    for node in connected:
                        explored[node[0], node[1]] = 1

                    # print(self.regenerate_coloured_text(self.array, colours={"red": connected}))
                    area = len(connected)

                    outside = []
                    for point in connected:
                        adj = search.get_adjacent(point, ignore_bounds=True)
                        for node in adj:
                            if node not in connected:
                                outside.append(node)
                    perimeter = len(outside)
                    cost += area * perimeter

        return cost



if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")
    test_1_run = test_1.run()
    assert test_1_run == 1930, test_1_run

    # test_2 = Solver(inp="Input/input_test.txt")
    # test_2_run = test_2.run()
    # assert test_2_run == 0, test_2_run

    sol = Solver(inp="Input/input.txt")
    print("Running Part 1")
    t0 = time.perf_counter()
    part_1 = sol.run()
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")

    # sol = Solver(inp="Input/input.txt")
    # print("Running Part 2")
    # t0 = time.perf_counter()
    # part_2 = sol.run()
    # print(f"Part 2 result: {part_2} {time.perf_counter() - t0:.3f}s")
