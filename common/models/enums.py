from enum import IntEnum

class PlayerRegistration(IntEnum):
    Success = 0
    NoPlayerSlotsLeft = 1
    AlreadyRegistered = 2

class MoveStatus(IntEnum):
    Success = 0
    Incorrect = 1
    Error = 2

class PlayerStatus(IntEnum):
    Won = 0
    Lost = 1
    Draw = 2
    CanMove = 3
    Wait = 4
    UnregisteredPlayer = 5

class GameStatus(IntEnum):
    Created = 0
    Started = 1
    Ended = 2
    EndedDraw = 3
    Aborted = 4
