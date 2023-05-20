package main

import (
	. "ai_client/game_api"
	"log"
	"time"
)

const (
	agentName      = "AI"
	address        = "localhost:8080" // Replace with your gRPC server address
	keepAliveDelay = 2 * time.Second  // Delay between keep-alive calls
)

func keepAlive(client *GameClient) {
	for {
		err := client.KeepAlive(agentName)
		if err != nil {
			log.Printf("Failed to send keep-alive: %v", err)
		}
		time.Sleep(keepAliveDelay)
	}
}

func main() {
	// Create the GameClient instance and establish the gRPC connection
	client, err := NewGameClient(address)
	if err != nil {
		log.Fatalf("Failed to create GameClient: %v", err)
	}
	defer client.Close()

	go keepAlive(client)

	// Keep the main goroutine alive
	select {}
}
