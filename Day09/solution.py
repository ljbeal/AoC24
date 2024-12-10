import copy
import time

from lib.base_solver import BaseSolver


class FileSegment:
    __slots__ = ["_size", "_id", "_next", "_prev", "_segment_id"]

    def __init__(self, size: int, id: int):
        self._size = size
        self._id = id

        self._next = None
        self._prev = None

        self._segment_id = None

    def __str__(self):
        if self.id >= 0:
            return str(self.id)
        return "."

    def __repr__(self) -> str:
        return f"({self.id}@{self.seg_id})"

    @property
    def seg_id(self) -> int:
        if self._segment_id is not None:
            return self._segment_id

        if self.prevseg.seg_id is not None:
            return self.prevseg.seg_id + 1

        if self.nextseg.seg_id is not None:
            return self.nextseg.seg_id - 1

        raise ValueError("could not get segment id")

    @property
    def size(self) -> int:
        return self._size

    @property
    def id(self) -> int:
        return self._id

    @property
    def nextseg(self) -> "FileSegment":
        return self._next

    @property
    def prevseg(self) -> "FileSegment":
        return self._prev

    @property
    def links(self) -> tuple["FileSegment", "FileSegment"]:
        return self.prevseg, self.nextseg

    def add_next(self, nextseg: "FileSegment", internal_call: bool = False):
        if nextseg is not None and not internal_call:
            nextseg.add_prev(self, internal_call=True)
        self._next = nextseg
        self.seg_id  # update ids

    def add_prev(self, prevseg: "FileSegment", internal_call: bool = False):
        if prevseg is not None and not internal_call:
            prevseg.add_next(self, internal_call=True)
        self._prev = prevseg
        self.seg_id  # update ids

    def break_next(self, internal_call: bool = False):
        if self.prevseg is not None and not internal_call:
            self.prevseg.break_next(internal_call=True)
        self._next = None
        self._segment_id = None

    def break_prev(self, internal_call: bool = False):
        if self.nextseg is not None and not internal_call:
            self.nextseg.break_prev(internal_call=True)
        self._prev = None
        self._segment_id = None

    def break_links(self):
        self.break_next()
        self.break_prev()

    def add_links(self, prevseg: "FileSegment", nextseg: "FileSegment"):
        self.add_next(nextseg)
        self.add_prev(prevseg)

    def get_segment_size(self) -> int:
        size = 0
        seg = self
        while seg.id == self.id and seg.prevseg is not None:
            seg = seg.prevseg
            size += 1

        seg = self
        if seg.nextseg is not None:
            size -= 1
            while seg.id == self.id and seg.nextseg is not None:
                seg = seg.nextseg
                size += 1

        return size


class FileSystem:
    __slots__ = ["_sequence"]

    def __init__(self):
        self._sequence = []

    def __repr__(self) -> str:
        output = []
        for seg in self.sequence:
            output.append(str(seg))
        padding = len(str(len(self._sequence)))

        return "|".join([char.rjust(padding) for char in output])

    def dispay_seg_ids(self):
        output = []
        for seg in self.sequence:
            output.append(str(seg.seg_id))
        padding = len(str(len(self._sequence)))

        return "|".join([char.rjust(padding) for char in output])

    def append(self, segment: FileSegment):
        if len(self._sequence) != 0:
            prev = self._sequence[-1]
            prev.add_next(segment)

        self._sequence.append(segment)

    @property
    def sequence(self):
        return self._sequence

    @property
    def free_space(self) -> int:
        count = 0
        for segment in self._sequence:
            if segment.id == -1:
                count += 1
        return count

    def swap(self, index_u: int, index_v: int):
        # print(f"swapping {index_u} & {index_v}")
        self._sequence[index_u], self._sequence[index_v] = self._sequence[index_v], self._sequence[index_u]

        self._sequence[index_u]._next = None
        self._sequence[index_u]._prev = None
        self._sequence[index_v]._prev = None
        self._sequence[index_v]._next = None

        # relink
        if index_u > 0:
            self._sequence[index_u].add_prev(self._sequence[index_u - 1])
        if index_u < len(self._sequence) - 1:
            self._sequence[index_u].add_next(self._sequence[index_u + 1])
        if index_v > 0:
            self._sequence[index_v].add_prev(self._sequence[index_v - 1])
        if index_v < len(self._sequence) - 1:
            self._sequence[index_v].add_next(self._sequence[index_v + 1])

    def get_space(self, size: int | None = None) -> int:
        for idx, seg in enumerate(self.sequence):
            if seg.id == -1:
                if size is not None and seg.get_segment_size() >= size:
                    return idx
                elif size is None:
                    return idx

        return None


class Solver(BaseSolver):
    __slots__ = ["_files", "_space", "_filesystem"]

    def __init__(self, inp: str):
        super().__init__(inp=inp)

        self._files = [int(c) for c in self.data[0::2]]
        self._space = [int(c) for c in self.data[1::2]]

        self._filesystem = None

    @property
    def files(self):
        return self._files

    @property
    def space(self):
        return self._space

    @property
    def filesytem(self) -> FileSystem:
        if self._filesystem is not None:
            return self._filesystem

        fs = FileSystem()
        idx = 0
        file = True
        for item in self.data:
            if file:
                for i in range(int(item)):
                    segment = FileSegment(int(item), idx)
                    segment._segment_id = len(fs._sequence)
                    fs.append(segment)
                idx += 1
            else:
                for i in range(int(item)):
                    segment = FileSegment(int(item), -1)
                    segment._segment_id = len(fs._sequence)
                    fs.append(segment)

            file = not file
        self._filesystem = fs
        return self._filesystem

    def compress(self, fs: FileSystem) -> FileSystem:
        seq = fs.sequence

        for seg_id in range(len(seq)):
            free_id = fs.get_space()
            back_id = len(seq) - seg_id - 1

            if back_id <= free_id:
                # print("free id > seg_id, breaking")
                break
            fs.swap(free_id, back_id)

        return fs

    def compress_nonfrag(self, fs: FileSystem) -> FileSystem:
        seq = fs.sequence
        # print(seq)
        swapped = []
        for seg_id in range(len(seq)):
            back_id = len(seq) - seg_id - 1

            file = seq[back_id]
            if file.id == -1:
                continue

            if file.id in swapped:
                continue

            filesize = file.get_segment_size()
            free_id = fs.get_space(size=filesize)
            if free_id is None:
                continue
            # print(repr(file))
            # print(f"filesize: {filesize}")
            # print(f"found suitable space at {free_id}")

            if back_id <= free_id:
                # print("free id > seg_id, breaking")
                continue

            for i in range(filesize):
                # print(f"swapping segment at {back_id - i} ({fs.sequence[back_id - i]}) with {free_id + i} ({fs.sequence[free_id + i]})")
                fs.swap(free_id + i, back_id - i)

            swapped.append(file.id)

            # print(fs)

        return fs

    def run(self, frag: bool = True) -> int:
        print("Compressing... ", end="")
        if frag:
            compressed = self.compress(self.filesytem)
        else:
            compressed = self.compress_nonfrag(self.filesytem)

        return self.get_checksum(compressed)

    def get_checksum(self, compressed: FileSystem, verbose=True) -> int:
        checksum = 0
        if verbose:
            print("Done.\nGenerating checksum... ", end=" ")
        for idx, item in enumerate(compressed.sequence):
            if item.id != -1:
                checksum += idx * item.id
        if verbose:
            print("Done.")

        return checksum


if __name__ == "__main__":
    test = Solver(inp="Input/input_test.txt")
    test_1_run = test.run()
    assert test_1_run == 1928, test_1_run

    test = Solver(inp="Input/input_test.txt")
    test_2_run = test.run(frag=False)
    assert test_2_run == 2858, test_2_run


    sol = Solver(inp="Input/input.txt")
    print("Running Part 1")
    t0 = time.perf_counter()
    part_1 = sol.run()
    print(f"Part 1 result: {part_1} {time.perf_counter() - t0:.3f}s")

    sol = Solver(inp="Input/input.txt")
    print("Running Part 2")
    t0 = time.perf_counter()
    part_2 = sol.run(frag=False)
    print(f"Part 2 result: {part_2} {time.perf_counter() - t0:.3f}s")
