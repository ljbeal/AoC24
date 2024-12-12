import time

import numpy as np
from networkx.algorithms.distance_measures import periphery

from lib.base_solver import BaseSolver
from lib.bfs import BFS


class FloodFill(BFS):
    def extra_condition(self, node: tuple[int, int], test: tuple[int, int]) -> bool:
        return self.value(node) == self.value(test)


class Solver(BaseSolver):

    def __init__(self, inp: str):
        super().__init__(inp=inp)

    def run(self, discount: bool):
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

                    directions = ["-i", "-j", "+i", "+j"]
                    perimeter_points = {d: [] for d in directions}
                    for point in connected:
                        adj = search.get_adjacent(point, ignore_bounds=True)
                        for direction, node in enumerate(adj):
                            if node not in connected:
                                perimeter_points[directions[direction]].append(node)

                    if not discount:
                        perimeter = sum(len(lst) for lst in perimeter_points.values())
                    else:
                        # With the "bulk discount" applied, the perimeter is "side degenerate".
                        # That is to say, a side counts as 1 perimeter length
                        # regardless of actual length
                        if area == 1:
                            # trivial case where there is only a single point
                            perimeter = 4
                        else:
                            perimeter = 0

                            for direction, points in perimeter_points.items():
                                print(f"direction {direction}")
                                # walk each direction, counting all non-continuous point instances
                                test = (-10, -10)  # we should start from a test point far away
                                for point in points:
                                    # compare "test" against "point", ensuring that exactly one coordinate is the same
                                    print(f"comparing {test} to {point}")
                                    a, b = test
                                    x, y = point
                                    # print(a == x, b == y, a == y, b == x)
                                    if a == x or b == y or a == y or b == x:
                                        print("\tskip")
                                    else:
                                        perimeter += 1
                                        print(f"\tadding ({perimeter})")

                                    test = point

                            print(self.regenerate_coloured_text(self.array, colours={"red": connected}))
                            print(perimeter)

                    cost += area * perimeter

                    # print(cost)
                    # exit()

        return cost


if __name__ == "__main__":

    # test_1 = Solver(inp="Input/input_test.txt")
    # test_1_run = test_1.run(discount=False)
    # assert test_1_run == 1930, test_1_run

    test_2 = Solver(inp="Input/input_test.txt")
    test_2_run = test_2.run(discount=True)
    assert test_2_run == 1206, test_2_run

    sol = Solver(inp="Input/input.txt")
    print("Running Part 1")
    t0 = time.perf_counter()
    part_1 = sol.run(discount=False)
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")

    sol = Solver(inp="Input/input.txt")
    print("Running Part 2")
    t0 = time.perf_counter()
    part_2 = sol.run(discount=True)
    print(f"Part 2 result: {part_2} {time.perf_counter() - t0:.3f}s")
