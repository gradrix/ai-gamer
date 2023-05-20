package main

import (
	"context"
	"log"

	gc "ai_client/game_api"

	"google.golang.org/grpc"
)

func test() {
	// Set up a connection to the Python gRPC server
	conn, err := grpc.Dial("localhost:8080", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("Failed to connect: %v", err)
	}
	defer conn.Close()

	// Create a new instance of the gRPC client
	client := gc.NewGameApiClient(conn)

	// Create a request
	request := &gc.PlayerNameRequest{
		PlayerName: "AI",
	}

	// Call the remote method
	response, err := client.RegisterPlayer(context.Background(), request)
	if err != nil {
		log.Fatalf("RPC failed: %v", err)
	}

	// Handle the response
	log.Println(response.RegistrationStatus)
}
