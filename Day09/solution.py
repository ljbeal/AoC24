import copy
import time

from lib.base_solver import BaseSolver


class FileSegment:
    __slots__ = ["_size", "_id"]

    def __init__(self, size: int, id: int):
        self._size = size
        self._id = id

    def __repr__(self) -> str:
        return f"({self.id})"

    @property
    def size(self) -> int:
        return self._size

    @property
    def id(self) -> int:
        return self._id


class Solver(BaseSolver):

    __slots__ = ["_files", "_space", "_sequence"]

    def __init__(self, inp: str):
        super().__init__(inp=inp)

        self._files = [int(c) for c in self.data[0::2]]
        self._space = [int(c) for c in self.data[1::2]]

        self._sequence = None

    @property
    def files(self):
        return self._files

    @property
    def space(self):
        return self._space

    @property
    def sequence(self):
        if self._sequence is not None:
            return self._sequence

        structure = []
        idx = 0
        file = True
        for item in self.data:
            if file:
                structure += [FileSegment(int(item), idx)] * int(item)
                idx += 1
            else:
                structure += ["."] * int(item)

            file = not file

        return structure

    def compress(self, sequence: str) -> str:
        nspace = sequence.count(".")
        # print(f"there are {nspace} free space instances")

        # take from the end of the sequence, replacing "." characters
        tmp = copy.deepcopy(self.sequence)
        nreplacements = 0
        for item in sequence[::-1]:
            nextspace = tmp.index(".")

            tmp[nextspace] = item
            nreplacements += 1

            if nreplacements >= nspace:
                break
        tmp = tmp[:-nspace]

        return tmp

    def run(self) -> int:
        print("Compressing... ", end="")
        compressed = self.compress(self.sequence)

        checksum = 0
        print("Done.\nGenerating checksum... ", end=" ")
        for idx, item in enumerate(compressed):
            checksum += idx * item.id

        print("Done.")

        return checksum



if __name__ == "__main__":

    test_1 = Solver(inp="Input/input_test.txt")

    test_1_run = test_1.run()

    assert test_1_run == 1928, test_1_run

    sol = Solver(inp="Input/input.txt")

    print("Running Part 1")
    t0 = time.perf_counter()

    part_1 = sol.run()
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")
