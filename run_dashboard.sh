#!/bin/bash

# AI-Gamer Dashboard Script
# Runs the learning progress dashboard

echo "📊 Starting AI-Gamer Dashboard..."

# Stop and remove existing container if it exists
docker stop ai_dashboard >/dev/null 2>&1
docker rm ai_dashboard >/dev/null 2>&1

# Build the dashboard image
echo "🔨 Building dashboard image..."
docker build -t ai_dashboard -f ./dashboard/Dockerfile .

# Create necessary directories if they don't exist
mkdir -p data/db
mkdir -p data/charts

# Run the dashboard container
# Use host network and mount the data directory
echo "🐳 Starting dashboard container..."
docker run -d \
  --name ai_dashboard \
  --network host \
  -v $(pwd)/data:/app/data \
  -e PYTHONUNBUFFERED=1 \
  ai_dashboard

# Wait a moment for the dashboard to start
sleep 3

# Show dashboard info
echo ""
echo "🎉 Dashboard is now running!"
echo "🌐 Open your browser and go to: http://localhost:5000"
echo "📊 The dashboard shows real-time AI learning progress"
echo "🔄 Data updates automatically every 30 seconds"
echo ""
echo "📜 Dashboard Logs:"
docker logs -f ai_dashboard