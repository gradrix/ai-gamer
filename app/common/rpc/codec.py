from models.game import MoveResult
from rpc import gameapi_pb2
from models.enums import PlayerRegistration, PlayerStatus, MoveStatus

def decodeRegisterPlayerResponse(response: gameapi_pb2.RegisterPlayerResponse):
    match response.registrationStatus:
        case gameapi_pb2.PlayerRegistration.REGISTRATION_SUCCESS:
            return PlayerRegistration.Success
        case gameapi_pb2.PlayerRegistration.NO_PLAYER_SLOT_LEFT:
            return PlayerRegistration.NoPlayerSlotsLeft
        case gameapi_pb2.PlayerRegistration.ALREADY_REGISTERED:
            return PlayerRegistration.AlreadyRegistered

def encodeRegisterPlayerResponse(registrationResult: PlayerRegistration):
    match registrationResult:
        case PlayerRegistration.Success:
            status = gameapi_pb2.PlayerRegistration.REGISTRATION_SUCCESS
        case PlayerRegistration.NoPlayerSlotsLeft:
            status = gameapi_pb2.PlayerRegistration.NO_PLAYER_SLOT_LEFT
        case PlayerRegistration.AlreadyRegistered:
            status = gameapi_pb2.PlayerRegistration.ALREADY_REGISTERED
    return gameapi_pb2.RegisterPlayerResponse(registrationStatus = status)

def decodeGetPossibleMovesResponse(response: gameapi_pb2.GetPossibleMovesResponse):
    result = []
    for move in response.moves:
        result.append((move.x, move.y))
    return result

def encodeGetPossibleMovesResponse(response):
    result = []
    for move in response:
        (x, y) = move
        result.append(gameapi_pb2.MoveCoordinates(x = x, y = y))
    return gameapi_pb2.GetPossibleMovesResponse(moves = result)

def decodeGetCurrentBoardResponse(response: gameapi_pb2.GetCurrentBoardResponse):
    result = []
    for row in response.grid:
        rows = []
        for item in row:
            rows.append(item)
        result.append(rows)
    return result

def encodeGetCurrentBoardResponse(response):
    result = []
    for row in response:
        result.append(gameapi_pb2.BoardRow(items = row.items))
    return gameapi_pb2.GetCurrentBoardResponse(grid = result)

def decodeCanMoveResponse(response: gameapi_pb2.CanMoveResponse):
    match response.playerStatus:
        case gameapi_pb2.PlayerStatus.WON:
            return PlayerStatus.Won
        case gameapi_pb2.PlayerStatus.LOST:
            return PlayerStatus.Lost
        case gameapi_pb2.PlayerStatus.DRAW:
            return PlayerStatus.Draw
        case gameapi_pb2.PlayerStatus.CAN_MOVE:
            return PlayerStatus.CanMove
        case gameapi_pb2.PlayerStatus.WAIT:
            return PlayerStatus.Wait
        case gameapi_pb2.PlayerStatus.UNREGISTERED_PLAYER:
            return PlayerStatus.UnregisteredPlayer

def encodeCanMoveResponse(response: PlayerStatus):
    match response:
        case PlayerStatus.Won:
            status = gameapi_pb2.PlayerStatus.WON
        case PlayerStatus.Lost:
            status = gameapi_pb2.PlayerStatus.LOST
        case PlayerStatus.Draw:
            status = gameapi_pb2.PlayerStatus.DRAW
        case PlayerStatus.CanMove:
            status = gameapi_pb2.PlayerStatus.CAN_MOVE
        case PlayerStatus.Wait:
            status = gameapi_pb2.PlayerStatus.WAIT
        case PlayerStatus.UnregisteredPlayer:
            status = gameapi_pb2.PlayerStatus.UNREGISTERED_PLAYER
    return gameapi_pb2.CanMoveResponse(playerStatus = status)

def encodePlayerNameRequest(playerName):
    return gameapi_pb2.PlayerNameRequest(playerName=playerName)

def encodeMoveRequest(playerName: str, index: int):
    return gameapi_pb2.MoveRequest(
        playerName=playerName, 
        index=index
    )

def decodeMoveResponse(response: gameapi_pb2.MoveResponse):
    match response.status:
        case gameapi_pb2.MoveStatus.MOVE_SUCCESS:
            status = MoveStatus.Success
        case gameapi_pb2.MoveStatus.INCORRECT:
            status = MoveStatus.Incorrect
        case _:
            status = MoveStatus.Error
    return MoveResult(status, response.move)

def encodeMoveResponse(response: MoveResult):
    match response.status:
        case MoveStatus.Success:
            status = gameapi_pb2.MoveStatus.MOVE_SUCCESS
        case MoveStatus.Incorrect:
            status = gameapi_pb2.MoveStatus.INCORRECT
        case _:
            status = gameapi_pb2.MoveStatus.ERROR
    return gameapi_pb2.MoveResponse(status = status, move = response.move)