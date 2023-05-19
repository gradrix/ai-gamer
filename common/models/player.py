import uuid
from dataclasses import dataclass

from .enums import PlayerStatus

@dataclass
class Player:
    id: int
    name: str
    createddate: int
    lastonline: int
    status: PlayerStatus = PlayerStatus.Wait

    def __post_init__(self):
        self.refid = str(uuid.uuid4())

    def __str__(self):
        return str(self.name)+'->'+str(self.id)
    