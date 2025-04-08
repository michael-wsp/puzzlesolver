from .puzzle import *


class TenToZero(Puzzle[int]):
    def start(self):
        return 10000000
    
    def generate_moves(self, position):
        return [x for x in [1, 2] if position - x >= 0]
    
    def do_move(self, position, move):
        return position - move
    
    def primitive(self, position):
        if position == 0:
            return Value.Win
        else:
            return Value.Undecided