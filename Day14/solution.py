import copy
import math
import time

import numpy as np

from lib.base_solver import BaseSolver


class Robot:
    __slots__ = ["_x", "_y", "_vx", "_vy", "_steps", "_bounds"]
    def __init__(self, init_loc: tuple[int, ...], init_vel: tuple[int, ...], bounds: tuple[int, int]):
        self._x = init_loc[0]
        self._y = init_loc[1]

        self._vx = init_vel[0]
        self._vy = init_vel[1]

        self._bounds = bounds
        self._steps: int = 0

    def __repr__(self) -> str:
        return f"Robot({self._x}, {self._y}, {self._vx}, {self._vy})"

    def step(self):
        self._x += self._vx
        self._y += self._vy

        if self._x >= self._bounds[0]:
            self._x -= self._bounds[0]
        elif self._x < 0:
            self._x += self._bounds[0]

        if self._y >= self._bounds[1]:
            self._y -= self._bounds[1]
        elif self._y < 0:
            self._y += self._bounds[1]

        self._steps += 1

    @property
    def position(self):
        return self._x, self._y

    @property
    def steps(self):
        return self._steps


class Solver(BaseSolver):

    __slots__ = ["_robots"]

    def __init__(self, inp: str):
        super().__init__(inp=inp)

        self._robots = []

    def create_robots(self, bounds: tuple[int, int]):
        for line in self.data.split("\n"):
            loc, vel = line.split(" ")
            loc = tuple(int(p) for p in loc.split("=")[1].split(","))
            vel = tuple(int(p) for p in vel.split("=")[1].split(","))

            self._robots.append(Robot(init_loc=loc, init_vel=vel, bounds=bounds))

    @property
    def robots(self):
        return self._robots

    def run(self, bounds: tuple[int, int]):
        self.create_robots(bounds=bounds)
        area = np.full(shape=bounds, fill_value=0)

        nsteps = 100
        for step in range(nsteps):
            for robot in self.robots:

                # display = copy.deepcopy(area)
                # display[*robot.position] = 1
                # print(self.regenerate_text(display.T, spacing=0))

                robot.step()

            print(f"performed step {step+1}/{nsteps}")

        print("area shape:", area.shape)
        for robot in self.robots:
            area[*robot.position] += 1

        area = area.T
        print(self.regenerate_text(area))

        print("top left region")
        tl = area[:int(area.shape[0]/2), :int(area.shape[1]/2)]
        print(self.regenerate_text(tl))
        tlsum = np.sum(tl, axis=(0, 1))

        print("top right region")
        tr = area[:int(area.shape[0]/2), math.ceil(area.shape[1]/2):]
        print(self.regenerate_text(tr))
        trsum = np.sum(tr, axis=(0, 1))

        print("top left region")
        bl = area[math.ceil(area.shape[0]/2):, :int(area.shape[1]/2)]
        print(self.regenerate_text(bl))
        blsum = np.sum(bl, axis=(0, 1))

        print("bottom right region")
        br = area[math.ceil(area.shape[0]/2):, math.ceil(area.shape[1]/2):]
        print(self.regenerate_text(br))
        brsum = np.sum(br, axis=(0, 1))

        return tlsum * trsum * blsum * brsum


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")
    test_1_run = test_1.run(bounds=(11, 7))
    assert test_1_run == 12, test_1_run

    # test_2 = Solver(inp="Input/input_test.txt")
    # test_2_run = test_2.run()
    # assert test_2_run == 0, test_2_run

    sol = Solver(inp="Input/input.txt")
    print("Running Part 1")
    t0 = time.perf_counter()
    part_1 = sol.run(bounds=(101, 103))
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")

    # sol = Solver(inp="Input/input.txt")
    # print("Running Part 2")
    # t0 = time.perf_counter()
    # part_2 = sol.run()
    # print(f"Part 2 result: {part_2} {time.perf_counter() - t0:.3f}s")
