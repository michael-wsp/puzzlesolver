from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from collections.abc import Hashable
from enum import Enum

State = TypeVar('state', bound=Hashable)

class Value(Enum):
    Undecided = 0
    Win = 1
    Loss = 2


class Puzzle(ABC, Generic[State]):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def start(self) -> State:
        """
        Returns the starting position of the puzzle.
        """
        pass
    
    @abstractmethod
    def generate_moves(self, position: State) -> list[State]:
        """
        Returns a list of positions given the input position.
        """
        pass
    
    @abstractmethod
    def do_move(self, position: State, move: State) -> State:
        """
        Returns the resulting position of applying move to position.
        """
        pass

    @abstractmethod
    def primitive(self, position: State) -> Value:
        """
        Returns a Value enum which defines whether the current position is a win, loss, or non-terminal. 
        """
        pass

    