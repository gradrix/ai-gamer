#!/bin/bash

# AI Agent Docker Script
# Runs the AI agent that learns to play the game

echo "🤖 Starting AI Agent in Docker..."

# Stop and remove existing container if it exists
docker stop ai_agent >/dev/null 2>&1
docker rm ai_agent >/dev/null 2>&1

# Build the AI agent image
echo "🔨 Building AI agent image..."
docker build -t ai_agent -f ./ai_agent/Dockerfile .

# Create necessary directories if they don't exist
mkdir -p data/models

# Run the AI agent container with GPU support
# Use host network to connect to game server on localhost
echo "🐳 Starting AI agent container..."
docker run -d \
  --name ai_agent \
  --network host \
  --gpus all \
  -v $(pwd)/data/models:/app/data/models \
  -e PLAYER_NAME="AILearner" \
  -e LEARNING_MODE="true" \
  -e PYTHONUNBUFFERED=1 \
  ai_agent

# Wait a moment for the agent to start
sleep 3

# Show logs
echo "📜 AI Agent Logs:"
docker logs -f ai_agent