#!/bin/bash

# Complete System Test
# Tests all components to ensure they work together

echo "🧪 Testing Complete AI-Gamer System"
echo "===================================="

# Test 1: Database Schema
echo ""
echo "1️⃣ Testing database schema..."
python3 -c "
import sqlite3
conn = sqlite3.connect('data/db/game_records.db')
cursor = conn.cursor()

# Check players table
cursor.execute('PRAGMA table_info(players)')
columns = [col[1] for col in cursor.fetchall()]

if 'is_ai' in columns:
    print('✅ Database has correct schema with is_ai column')
else:
    print('❌ Database missing is_ai column')
    exit(1)

conn.close()
"

# Test 2: AI Agent Registration Simulation
echo ""
echo "2️⃣ Testing AI registration simulation..."
python3 -c "
import sqlite3
from datetime import datetime

conn = sqlite3.connect('data/db/game_records.db')
cursor = conn.cursor()

# Insert test AI player
cursor.execute('INSERT INTO players (name, createddate, lastonline, is_ai) VALUES (?, ?, ?, ?)',
              ('AILearner', int(datetime.now().timestamp()), int(datetime.now().timestamp()), True))

# Insert test game results
ai_player_id = cursor.lastrowid
for i in range(5):
    result = 1 if i % 2 == 0 else 2  # Alternate wins and losses
    cursor.execute('INSERT INTO game_results (gameid, playerid, result, timestamp) VALUES (?, ?, ?, ?)',
                  (i, ai_player_id, result, int(datetime.now().timestamp()) - (5 - i) * 60))

conn.commit()

# Test statistics
cursor.execute('SELECT COUNT(*) FROM game_results WHERE playerid = ?', (ai_player_id,))
total_games = cursor.fetchone()[0]

cursor.execute('SELECT result, COUNT(*) FROM game_results WHERE playerid = ? GROUP BY result', (ai_player_id,))
results = cursor.fetchall()

wins = sum(count for result, count in results if result == 1)
losses = sum(count for result, count in results if result == 2)

print(f'✅ Test data inserted: {total_games} games ({wins} wins, {losses} losses)')

conn.close()
"

# Test 3: Statistics Viewer
echo ""
echo "3️⃣ Testing statistics viewer..."
./show_learning_stats.sh

# Test 4: Dashboard API
echo ""
echo "4️⃣ Testing dashboard API..."
python3 -c "
import requests
import json

try:
    response = requests.get('http://localhost:5000/api/stats')
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Dashboard API works!')
        print(f'   Total Games: {data.get(\"total_games\", 0)}')
        print(f'   Win Rate: {data.get(\"win_rate\", 0):.1f}%')
    else:
        print(f'❌ Dashboard API error: {response.status_code}')
        print(f'   Response: {response.text}')
except Exception as e:
    print(f'❌ Dashboard not running or error: {e}')
    print('   Try: ./run_dashboard.sh')
"

# Test 5: Cleanup
echo ""
echo "5️⃣ Cleaning up test data..."
python3 -c "
import sqlite3
conn = sqlite3.connect('data/db/game_records.db')
cursor = conn.cursor()

# Remove test data
cursor.execute('DELETE FROM game_results WHERE playerid IN (SELECT id FROM players WHERE name = ?)', ('AILearner',))
cursor.execute('DELETE FROM players WHERE name = ?', ('AILearner',))

conn.commit()
print('✅ Test data cleaned up')

conn.close()
"

echo ""
echo "🎉 All tests completed!"
echo ""
echo "🚀 Ready to run the real system:"
echo "   ./run_learning_system.sh"
