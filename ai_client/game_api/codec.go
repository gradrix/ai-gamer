package game_api

import (
	. "ai_client/common"
)

func ConvertPlayerRegistrationResponse(resp *RegisterPlayerResponse) RegistrationStatus {
	switch resp.RegistrationStatus {
	case PlayerRegistration_REGISTRATION_SUCCESS:
		return RegistrationSuccess
	case PlayerRegistration_NO_PLAYER_SLOT_LEFT:
		return NoPlayerSlotLeft
	case PlayerRegistration_ALREADY_REGISTERED:
		return AlreadyRegistered
	default:
		return RegistrationError
	}
}

func ConvertGetPossibleMovesResponse(resp *GetPossibleMovesResponse) []Coordinate {
	moves := resp.Moves
	result := make([]Coordinate, len(moves))
	for i, cord := range moves {
		result[i] = Coordinate{
			X: cord.X,
			Y: cord.Y,
		}
	}
	return result
}

func ConvertGetCurrentBoardResponse(resp *GetCurrentBoardResponse) [][]int32 {
	grid := resp.Grid
	result := make([][]int32, len(grid))
	for i, row := range grid {
		items := row.Items
		result[i] = make([]int32, len(items))
		for j, cell := range items {
			result[i][j] = cell
		}
	}
	return result
}

func ConvertCanMoveResponse(resp *CanMoveResponse) GameStatus {
	switch resp.PlayerStatus {
	case PlayerStatus_WON:
		return Won
	case PlayerStatus_LOST:
		return Lost
	case PlayerStatus_DRAW:
		return Draw
	case PlayerStatus_CAN_MOVE:
		return CanMove
	case PlayerStatus_WAIT:
		return Wait
	case PlayerStatus_UNREGISTERED_PLAYER:
		return UnregisteredPlayer
	default:
		return PlayerError
	}
}

func ConvertMoveResponse(resp *MoveResponse) GameMoveStatus {
	switch resp.Status {
	case MoveStatus_MOVE_SUCCESS:
		return MoveSuccess
	case MoveStatus_INCORRECT:
		return Incorrect
	default:
		return MoveError
	}
}
