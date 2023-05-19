#!/bin/bash

# Stop and remove the existing game_server container (if it exists)
docker stop game_server >/dev/null 2>&1 && docker rm game_server >/dev/null 2>&1

# Build the new game_server image
docker build -t game_server -f ./app/game_server/Dockerfile .

# Run the new game_server container
docker run -d -v $(pwd)/db:/db  -p 8080:8080 --name game_server game_server

# Watch for logs
docker logs -f game_server