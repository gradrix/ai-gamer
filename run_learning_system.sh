#!/bin/bash

# AI-Gamer Learning System Master Script
# Starts the complete system: server, random client, and AI agent
# with comprehensive monitoring

echo "🎮 Starting AI-Gamer Learning System..."
echo "========================================"

# Create necessary directories
mkdir -p data/db
mkdir -p data/models
mkdir -p data/logs

# Function to check if a container is running
is_container_running() {
    docker ps --format '{{.Names}}' | grep -q "^$1$"
}

# Start Game Server
echo ""
echo "1️⃣ Starting Game Server..."
if is_container_running "game_server"; then
    echo "⚠️  Game server is already running"
else
    ./run_game_server_docker.sh &
    sleep 5  # Give server time to start
fi

# Start Random Client
echo ""
echo "2️⃣ Starting Random Client..."
if is_container_running "random_client"; then
    echo "⚠️  Random client is already running"
else
    for i in {1..10}; do ./run_random_client_docker.sh "_$i" & sleep 1; done
    sleep 3
fi

# Start AI Agent
echo ""
echo "3️⃣ Starting AI Agent..."
if is_container_running "ai_agent"; then
    echo "⚠️  AI agent is already running"
else
    ./run_ai_agent_docker.sh &
    sleep 5
fi

echo ""
echo "🎉 Learning System is now running!"
echo ""
echo "📊 Monitoring Options:"
echo "  • docker logs -f game_server"
echo "  • docker logs -f random_client"
echo "  • docker logs -f ai_agent"
echo "  • ./monitor_learning.sh"
echo ""
echo "🛑 To stop the system:"
echo "  • docker stop game_server random_client ai_agent"
echo "  • ./stop_learning_system.sh"

# # Start monitoring in background (but wait for AI to register first)
# echo ""
# echo "📈 Starting learning monitoring (will wait for AI registration)..."
# (
#     # Wait for AI player to register in database
#     echo "Waiting for AI player to register..."
#     for i in {1..30}; do
#         if python3 -c "
# import sqlite3
# try:
#     conn = sqlite3.connect('data/db/game_records.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT 1 FROM players WHERE name = ? LIMIT 1', ('AILearner',))
#     if cursor.fetchone():
#         print('✅ AI player registered!')
#         exit(0)
#     conn.close()
# except:
#     pass
# print('⏳ Waiting for AI registration...')
# " 2>/dev/null; then
#             break
#         fi
#         sleep 2
#     done
    
#     # Start monitoring
#     echo "Starting monitoring..."
#     ./monitor_learning.sh
# ) &

# Show system status
echo ""
echo "🔍 System Status:"
docker ps --format "{{.Names}}: {{.Status}}" | grep -E "(game_server|random_client|ai_agent)"