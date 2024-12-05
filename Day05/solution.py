import math
from typing import Union

import networkx.exception
from networkx.classes import subgraph

from lib.base_solver import BaseSolver

import networkx as nx


class Rule:

    __slots__ = ["a", "b", "_parent", "_child"]

    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

        self._parent = None
        self._child = None

    def __repr__(self) -> str:
        return f"Rule({self.a}, {self.b})"

    def __hash__(self) -> int:
        return hash(self.a) + hash(self.b)

    @property
    def parent(self) -> Union["Rule", None]:
        return self._parent

    @property
    def child(self) -> Union["Rule", None]:
        return self._child

    def add_parent(self, parent: "Rule", recursive_call: bool = False) -> None:
        """
        Add a "parent" to this Rule

        Args:
            parent (Rule):
                parent to add
            recursive_call (bool):
                internal flag to prevent infinite recursion
        """
        if not recursive_call:
            parent.add_child(self, recursive_call=True)
        self._parent = parent

    def add_child(self, child: "Rule", recursive_call: bool = False) -> None:
        """
        Add a "child" to this Rule

        Args:
            child (Rule):
                child to add
            recursive_call (bool):
                internal flag to prevent infinite recursion
        """
        if not recursive_call:
            child.add_parent(self, recursive_call=True)
        self._child = child


class Solver(BaseSolver):

    __slots__ = ["_rules", "_updates"]

    def __init__(self, inp: str):
        super().__init__(inp=inp)

        self._rules: list[Rule] = []
        self._updates: list[list[int]] = []
        for line in self.data.split("\n"):
            if "|" in line:
                self._rules.append(Rule(*self._sanitise_to_int(line.split("|"))))
            elif line.strip() != "":
                self._updates.append(self._sanitise_to_int(line.split(",")))

    @staticmethod
    def _sanitise_to_int(inp: list[str]) -> list[int]:
        """Convert a list of string numbers into a list of ints"""
        return [int(item) for item in inp]

    @property
    def rules(self) -> list[list[int]]:
        return self._rules

    @property
    def updates(self) -> list[list[int]]:
        return self._updates

    def get_graph(self) -> nx.DiGraph:
        """
        generate a graph of all rules
        """
        G = nx.DiGraph()
        for rule in self.rules:
            G.add_edge(rule.a, rule.b)

        return G

    def run(self) -> (int, int):
        # first, get the true path
        graph = self.get_graph()

        valid_updates = []
        fixed_updates = []
        for update in self.updates:
            print(f"assessing update {update}", end = "... ")
            valid = True
            for idx in range(len(update) - 1):
                u = update[idx]
                v = update[idx+1]
                # print(f"checking {u}->{v}")

                path = None
                if nx.has_path(graph, u, v):
                    path = nx.shortest_path(graph, u, v)

                if path is None or len(path) != 2:
                    valid = False
                    break

            if valid:
                print("valid")
                valid_updates.append(update)
            else:
                print("invalid")
                # if we're invalid, we need to conform this list to the graph
                # lets create a subgraph containing only those nodes and then
                # find the longest path
                subgraph = graph.subgraph(update)
                fixed_updates.append(nx.dag_longest_path(subgraph))


        # now get the central number from each valid update
        valid_midpoints = self.get_midpoints(valid_updates)
        fixed_midpoints = self.get_midpoints(fixed_updates)

        return sum(valid_midpoints), sum(fixed_midpoints)

    @staticmethod
    def get_midpoints(inp: list[list]) -> list:
        midpoints = []
        for lst in inp:
            mid_id = math.floor(len(lst)/2)
            midpoints.append(lst[mid_id])

        return midpoints

if __name__ == "__main__":
    import time

    t0 = time.perf_counter()
    test = Solver(inp="Input/input_test.txt")
    t_init = time.perf_counter()
    test_1_run, test_2_run = test.run()
    t_run = time.perf_counter()

    print(f"Test, time: {t_run-t0:.2f}s")

    assert test_1_run == 143, test_1_run
    assert test_2_run == 123, test_2_run

    print("running solution")
    t0 = time.perf_counter()
    sol = Solver(inp="Input/input.txt")

    sol_run_1, sol_run_2 = sol.run()
    t_run = time.perf_counter()

    print(f"Solution time: {t_run-t0:.2f}s")
    print(f"Part 1 solution: {sol_run_1}")
    print(f"Part 2 solution: {sol_run_2}")
