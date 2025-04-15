from .solver.solver import Solver
from .games.ten_to_zero import TenToZero

t = TenToZero()
s = Solver(t)
s.solve(overwrite=True)
s.print()