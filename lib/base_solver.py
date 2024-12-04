class BaseSolver:

    __slots__ = ["_data"]

    def __init__(self, inp: str):
        with open(inp, "r", encoding="utf8") as o:
            self._data = o.read()

    @property
    def data(self) -> str:
        return self._data
