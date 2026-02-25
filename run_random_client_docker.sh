#!/bin/bash

# Random Client Docker Script
# Runs the random client that plays against the AI

echo "🎲 Starting Random Client in Docker..."

# Stop and remove existing container if it exists
docker stop random_client >/dev/null 2>&1
docker rm random_client >/dev/null 2>&1

# Build the random client image
echo "🔨 Building random client image..."
docker build -t random_client -f ./random_client/Dockerfile .

# Run the random client container
# Use host network to connect to game server on localhost
echo "🐳 Starting random client container..."
docker run -d \
  --name random_client \
  --network host \
  -e PLAYER_NAME="RandomBot" \
  -e CLIENT_LOOP_DELAY="0.0" \
  -e PYTHONUNBUFFERED=1 \
  random_client

# Wait a moment for the client to start
sleep 2

# Show logs
echo "📜 Random Client Logs:"
docker logs -f random_client