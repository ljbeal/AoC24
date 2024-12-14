import time

import numpy as np

from lib.base_solver import BaseSolver


class Machine:

    __slots__ = ["a", "b", "target", "_a_count", "_b_count", "offset"]

    def __init__(
            self,
            a: tuple[int, int],
            b: tuple[int, int],
            target: tuple[int, int],
            offset: True
    ):
        if offset:
            _o = 10000000000000
            target = (target[0] + _o, target[1] + _o)

        self.a = a
        self.b = b
        self.target = target

        self.offset = True

        self._a_count, self._b_count = self._get_npresses()

    def __repr__(self) -> str:
        return f"Machine(a={self.a}, b={self.b}, target={self.target})"

    def _get_npresses(self) -> tuple[float, float]:
        actions = np.array([self.a, self.b])

        a, b = np.linalg.solve(actions.T, self.target)

        return a, b

    @property
    def npresses(self) -> tuple[float, float]:
        return self._a_count, self._b_count

    @property
    def cost(self) -> int:
        a, b = self.npresses
        if not self.playable:
            return 0
        return int(round(3 * a + b, 0))

    @property
    def playable(self) -> bool:
        """machine is considered unplayable if a button has to be pressed more than 100 times"""
        if not is_int(self._a_count):
            return False
        if not is_int(self._b_count):
            return False
        if not self.offset:
            return self._a_count <= 100 and self._b_count <= 100
        return True

def get_press_actions(desc: str) -> tuple[int, int]:
    """Given a description of a button press, extract the X, Y coord effects"""
    # print(f"extracting from {desc}")
    desc = desc.split(":")[1].strip()
    x_eff, y_eff = desc.split(",")
    x_int = int(x_eff.split("X")[-1].strip("="))
    y_int = int(y_eff.split("Y")[-1].strip("="))

    return x_int, y_int


def is_int(num: float | int) -> bool:
    return round(num, 3) == round(num, 0)


class Solver(BaseSolver):

    __slots__ = ["_machines"]

    def __init__(self, inp: str):
        super().__init__(inp=inp)

        self._machines: list[Machine] | None = None

    def get_machines(self, offset) -> list:
        if self._machines is not None:
            return self._machines

        self._machines = []
        tmp = {}
        for line in self.data.split("\n"):
            if line.strip() == "":
                self._machines.append(Machine(offset=offset, **tmp))
                tmp = {}
            elif "Button A" in line:
                tmp["a"] = get_press_actions(line)
            elif "Button B" in line:
                tmp["b"] = get_press_actions(line)
            else:
                tmp["target"] = get_press_actions(line)

        return self._machines

    def run(self, offset: bool = False) -> int:
        costs = []
        for machine in self.get_machines(offset=offset):

            if machine.playable:
                print(machine)
                a, b = machine.npresses
                print(f"\tRequires {a} a presses, {b} b presses, costing {machine.cost} (playable? {machine.playable})")
                costs.append(machine.cost)

        return sum(costs)


if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")
    test_1_run = test_1.run()
    assert test_1_run == 480, test_1_run

    # test_2 = Solver(inp="Input/input_test.txt")
    # test_2_run = test_2.run()
    # assert test_2_run == 0, test_2_run

    sol = Solver(inp="Input/input.txt")
    print("Running Part 1")
    t0 = time.perf_counter()
    part_1 = sol.run()
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")

    sol = Solver(inp="Input/input.txt")
    print("Running Part 2")
    t0 = time.perf_counter()
    part_2 = sol.run(offset=True)
    print(f"Part 2 result: {part_2} {time.perf_counter() - t0:.3f}s")
