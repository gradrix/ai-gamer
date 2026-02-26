#!/bin/bash

# Game Server Docker Script
# Runs the game server with proper volume mounting for database and logs

echo "🚀 Starting Game Server in Docker..."

# Stop and remove existing container if it exists
docker stop game_server >/dev/null 2>&1
docker rm game_server >/dev/null 2>&1

# Build the game server image
echo "🔨 Building game server image..."
docker build -t game_server -f ./game_server/Dockerfile .

# Create necessary directories if they don't exist
mkdir -p data/db
mkdir -p data/logs

# Run the game server container with proper volume mounting
echo "🐳 Starting game server container..."
docker run -d \
  --user $(id -u):$(id -g) \
  --name game_server \
  -p 8080:8080 \
  -v \$(pwd)/data/db:/app/data/db \
  -v $(pwd)/data/logs:/app/data/logs \
  -e PYTHONUNBUFFERED=1 \
  game_server

# Wait a moment for the server to start
sleep 3

# Show logs
echo "📜 Game Server Logs:"
docker logs -f game_server