#!/bin/bash

# Stop and remove the existing game_server container (if it exists)
docker stop ai_agent >/dev/null 2>&1 && docker rm ai_agent >/dev/null 2>&1

# Build the new game_server image
docker build -t ai_agent -f ./ai_agent/Dockerfile .

# Run the new game_server container
docker run -d -v $(pwd)/data/models:/app/data/models --name ai_agent ai_agent

# Watch for logs
docker logs -f ai_agent