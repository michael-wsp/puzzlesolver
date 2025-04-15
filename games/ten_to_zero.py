from .game import *


class TenToZero(Game[int]):
    def __init__(self):
        self.id = 'ten-to-zero'
        self.n_players = 2

    def start(self):
        return 10
    
    def generate_moves(self, position):
        return [x for x in [1, 2] if position - x >= 0]
    
    def do_move(self, position, move):
        return position - move
    
    def primitive(self, position):
        if position == 0:
            return Value.Loss
        else:
            return None