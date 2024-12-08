import unittest

from lib.base_solver import BaseSolver

solver = BaseSolver(inp="Input/test.txt")
class TestBounds(unittest.TestCase):
    def test_basic(self):
        assert solver.check_inside_bounds((5, 5))

    def test_zero(self):
        assert solver.check_inside_bounds((0, 0))

    def test_negative(self):
        assert not solver.check_inside_bounds((-1, -1))

    def test_larger_negative(self):
        assert not solver.check_inside_bounds((-5, -5))
