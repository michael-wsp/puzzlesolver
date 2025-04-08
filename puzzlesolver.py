from .solver.solver import Solver
from .puzzles.ten_to_zero import TenToZero

t = TenToZero()
s = Solver(t)
s.solve()
s.print()