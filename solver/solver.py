from collections import deque
from ..puzzles.puzzle import *
from ..database.database import PuzzleDB
import os

REMOTENESS_TERMINAL = 0

class Solver:
    def __init__(self, puzzle: Puzzle):
        self.db = PuzzleDB(puzzle.id)
        self.puzzle = puzzle
        self.solution = {}
        self.parent_map = {}

    def solve(self, overwrite=False):
        self.db.create(overwrite)
        if overwrite:
            self.discover()
            print("discovered")
            self.propagate()
            print("solved")
            self.db.insert(self.solution)

    def get_children(self, position):
        moves = self.puzzle.generate_moves(position)
        return map(lambda m: self.puzzle.do_move(position, m), moves)

    def discover(self):
        visited = set()
        q = deque()
        start = self.puzzle.start()
        q.appendleft(start)
        visited.add(start)
        while q:
            position = q.pop()
            value = self.puzzle.primitive(position)
            if value is not None:
                self.solution[position] = (REMOTENESS_TERMINAL, value)
            else:
                children = self.get_children(position)
                for child in children:
                    if not self.parent_map.get(child):
                        self.parent_map[child] = set()
                    self.parent_map[child].add(position)
                    if child not in visited:
                        visited.add(child)
                        q.appendleft(child)
    
    def propagate(self):
        q = deque(self.solution.keys())
        while q:
            position = q.pop()
            parent_rem, val = self.solution.get(position)
            parent_rem += 1
            parent_val = self.parent_value(val)
            parents = self.parent_map.get(position, set())
            for parent in parents:
                parent_sol = self.solution.get(parent)
                if not parent_sol:
                    self.solution[parent] = (parent_rem, parent_val)
                    q.appendleft(parent)
                elif parent_sol[1] < parent_val:
                    self.solution[parent] = (parent_rem, parent_val)

    
    def parent_value(self, val: Value) -> Value:
        if self.puzzle.n_players == 1:
            return val
        else:
            if val == Value.Win:
                return Value.Loss
            elif val == Value.Loss:
                return Value.Win
            else:
                return val
    
    def print(self):
        if self.solution:
            sol = [(position, rem, value) for position, (rem, value) in self.solution.items()]
        else:
            sol = self.db.get_all()
        for (position, rem, value) in sol:
            print(f'{position} : remoteness : {rem} : value : {value}')
                
    
    def get_remoteness(self, state: int) -> int:
        rem, _ = self.db.get(state)
        if rem is None:
            return -1
        return rem
