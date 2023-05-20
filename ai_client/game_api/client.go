package game_api

import (
	"context"
	"fmt"

	. "ai_client/common"

	"google.golang.org/grpc"
)

// GameClient provides a wrapper around the gRPC client for the GameApi service.
type GameClient struct {
	client GameApiClient
	conn   *grpc.ClientConn
}

// NewGameClient creates a new instance of GameClient.
func NewGameClient(address string) (*GameClient, error) {
	// Create a gRPC connection.
	conn, err := grpc.Dial(address, grpc.WithInsecure())
	if err != nil {
		return nil, fmt.Errorf("failed to dial server: %v", err)
	}

	// Create a GameApiClient instance.
	client := NewGameApiClient(conn)

	return &GameClient{
		client: client,
		conn:   conn,
	}, nil
}

// Close closes the gRPC connection.
func (c *GameClient) Close() {
	if c.conn != nil {
		c.conn.Close()
	}
}

// RegisterPlayer registers a player with the game.
func (c *GameClient) RegisterPlayer(playerName string) (RegistrationStatus, error) {
	req := &PlayerNameRequest{
		PlayerName: playerName,
	}

	resp, err := c.client.RegisterPlayer(context.Background(), req)
	if err != nil {
		return RegistrationError, fmt.Errorf("failed to register player: %v", err)
	}
	response := ConvertPlayerRegistrationResponse(resp)
	return response, nil
}

// GetPossibleMoves retrieves the possible moves
func (c *GameClient) GetPossibleMoves() ([]Coordinate, error) {
	req := &GetPossibleMovesRequest{}

	resp, err := c.client.GetPossibleMoves(context.Background(), req)
	if err != nil {
		return nil, fmt.Errorf("failed to get possible moves: %v", err)
	}
	response := ConvertGetPossibleMovesResponse(resp)
	return response, nil
}

// GetCurrentBoard retrieves the current board state.
func (c *GameClient) GetCurrentBoard() ([][]int32, error) {
	req := &GetCurrentBoardRequest{}

	resp, err := c.client.GetCurrentBoard(context.Background(), req)
	if err != nil {
		return nil, fmt.Errorf("failed to get current board: %v", err)
	}
	response := ConvertGetCurrentBoardResponse(resp)
	return response, nil
}

// CanMove checks if a player can make a move.
func (c *GameClient) CanMove(playerName string) (GameStatus, error) {
	req := &PlayerNameRequest{
		PlayerName: playerName,
	}

	resp, err := c.client.CanMove(context.Background(), req)
	if err != nil {
		return PlayerError, fmt.Errorf("failed to check if player can move: %v", err)
	}
	response := ConvertCanMoveResponse(resp)
	return response, nil
}

// Move makes a move for a player.
func (c *GameClient) Move(playerName string, index int32) (GameMoveStatus, error) {
	req := &MoveRequest{
		PlayerName: playerName,
		Index:      index,
	}

	resp, err := c.client.Move(context.Background(), req)
	if err != nil {
		return MoveError, fmt.Errorf("failed to make a move: %v", err)
	}
	response := ConvertMoveResponse(resp)
	return response, nil
}

// KeepAlive sends a keep-alive request for a player.
func (c *GameClient) KeepAlive(playerName string) error {
	req := &PlayerNameRequest{
		PlayerName: playerName,
	}

	_, err := c.client.KeepAlive(context.Background(), req)
	if err != nil {
		return fmt.Errorf("failed to send keep-alive: %v", err)
	}
	return nil
}
