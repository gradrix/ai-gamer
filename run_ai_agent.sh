#!/bin/bash

# Retrieve the last argument
last_arg="${!#}"
debug=false
docker_file="Dockerfile"
debug_container_escape=""

# Check if the last argument is '--debug'
if [ "$last_arg" == "--debug" ]; then
    debug=true  
    docker_file="Dockerfile.debug"
    debug_container_escape="-it"
    echo "Running in debug mode"
fi

# Stop and remove the existing ai_agent container (if it exists)
docker stop ai_agent >/dev/null 2>&1 && docker rm ai_agent >/dev/null 2>&1

# Build the new ai_agent image
docker build -t ai_agent -f ./ai_agent/$docker_file .

# Run the new ai_agent container
docker run $debug_container_escape --network host --gpus all -d -v $(pwd)/data/models:/app/data/models --name ai_agent ai_agent

if [ "$debug" = false ]; then
    # Watch for logs
    docker logs -f ai_agent
fi