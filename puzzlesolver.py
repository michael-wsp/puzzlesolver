from .solver.solver import Solver
from .puzzles.ten_to_zero import TenToZero
from .database.database import PuzzleDB

t = TenToZero()
s = Solver(t)
s.solve()
s.print()