#!/bin/bash

# Random Client Docker Script
# Runs the random client that plays against the AI

SUFFIX=$1
if [ -z "$SUFFIX" ]; then
  SUFFIX=""
fi

CONTAINER_NAME="random_client${SUFFIX}"
PLAYER_NAME="RandomBot${SUFFIX}"

echo "🎲 Starting Random Client ${CONTAINER_NAME} in Docker..."

# Stop and remove existing container if it exists
docker stop ${CONTAINER_NAME} >/dev/null 2>&1
docker rm ${CONTAINER_NAME} >/dev/null 2>&1

# Build the random client image (only once effectively due to cache)
echo "🔨 Building random client image..."
docker build -t random_client -f ./random_client/Dockerfile .

# Run the random client container
# Use host network to connect to game server on localhost
echo "🐳 Starting ${CONTAINER_NAME}..."
docker run -d \
  --user $(id -u):$(id -g) \
  --name ${CONTAINER_NAME} \
  --network host \
  -v $(pwd)/data/db:/app/data/db \
  -e PLAYER_NAME="${PLAYER_NAME}" \
  -e CLIENT_LOOP_DELAY="0.0" \
  -e PYTHONUNBUFFERED=1 \
  random_client

# Wait a moment for the client to start
sleep 1

# Show logs
# echo "📜 ${CONTAINER_NAME} Logs:"
# docker logs -f ${CONTAINER_NAME} &
