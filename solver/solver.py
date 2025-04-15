from collections import deque
from ..puzzles.puzzle import *
from ..database.database import PuzzleDB
import os

class Solver:
    def __init__(self, puzzle: Puzzle):
        self.db = PuzzleDB(puzzle.id)
        self.puzzle = puzzle
        self.remoteness = {}
        self.primitives = set()
        self.parent_map = {}

    def solve(self, overwrite=False):
        self.db.create(overwrite)
        if overwrite:
            self.discover()
            print("discovered")
            self.propagate()
            print("solved")
            self.db.insert(self.remoteness)

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
            if value == Value.Loss:
                self.remoteness[position] = float('inf')
                self.primitives.add(position)
            elif value == Value.Win:
                self.remoteness[position] = 0
                self.primitives.add(position)
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
        visited = set(self.primitives)
        q = deque(self.primitives)
        while q:
            position = q.pop()
            rem = self.remoteness.get(position) + 1
            parents = self.parent_map.get(position, set())
            for parent in parents:
                if parent not in visited:
                    self.remoteness[parent] = rem
                    visited.add(parent)
                    q.appendleft(parent)
    
    def print(self):
        if self.remoteness:
            rem_map = self.remoteness.items()
        else:
            rem_map = self.db.get_all()
        for (position, rem) in rem_map:
            print(f'{position} : remoteness : {rem}')
                
    
    def get_remoteness(self, state: int) -> int:
        rem = self.db.get(state)
        if rem is None:
            return -1
        return rem
