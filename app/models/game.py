from dataclasses import dataclass

from models.player import Player
from models.enums import GameStatus, MoveStatus

@dataclass
class Game:
    id: int
    players: dict[Player]
    date: int
    status: GameStatus

class MoveResult:
    status: MoveStatus = None
    move: str = None

    def __init__(self, status, move):  
        self.status = status
        self.move = move