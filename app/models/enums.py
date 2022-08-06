from enum import IntEnum

class Mode(IntEnum):
    Console = 1 #Both players control game via console
    Mixed = 2 #Console player vs RPC player
    Rpc = 3 # Both players control game via rpc

class PlayerRegistration(IntEnum):
    Success = 1
    NoPlayerSlotsLeft = 2
    AlreadyRegistered = 3

class Move(IntEnum):
    Success = 1
    Incorrect = 2
    Error = 3

class GameStatus(IntEnum):
    Won = 1
    Lost = 2
    Draw = 3
    CanMove = 4
    Wait = 5
    UnregisteredPlayer = 6