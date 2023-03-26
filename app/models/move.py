from dataclasses import dataclass

@dataclass
class Move:
    id: int
    gameid: int
    playerid: int
    idx: int
    move: str
    date: int
