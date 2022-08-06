from dataclasses import dataclass

from models.enums import GameStatus

@dataclass
class Player:
    id: str
    status: GameStatus