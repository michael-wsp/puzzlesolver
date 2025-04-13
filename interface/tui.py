from ..solver.solver import Solver
from ..database.database import PuzzleDB

class TUI:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        solver = Solver(self.puzzle)
        solver.solve()
        