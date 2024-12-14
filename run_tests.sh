#!/bin/bash

# Stop and remove the existing game_tests container (if it exists)
docker stop game_tests >/dev/null 2>&1 && docker rm game_tests >/dev/null 2>&1

# Build the new ai_agent image
docker build -t game_tests -f ./ai_agent/Dockerfile.test .

# Run the new ai_agent container
docker run -it --network host --gpus all -d -v $(pwd)/data/models:/app/data/models --name game_tests game_tests
