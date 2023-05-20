package common

type RegistrationStatus int

const (
	RegistrationSuccess RegistrationStatus = iota
	NoPlayerSlotLeft
	AlreadyRegistered
	RegistrationError
)

type Player struct {
	ID   string
	Name string
}

type Coordinate struct {
	X int32
	Y int32
}

type GameStatus int

const (
	Won GameStatus = iota
	Lost
	Draw
	CanMove
	Wait
	UnregisteredPlayer
	PlayerError
)

type GameMoveStatus int

const (
	MoveSuccess GameMoveStatus = iota
	Incorrect
	MoveError
)
