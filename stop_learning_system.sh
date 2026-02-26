#!/bin/bash

# Stop AI-Gamer Learning System
# Gracefully shuts down all components

echo "🛑 Stopping AI-Gamer Learning System..."

# Stop all containers
echo "Stopping containers..."
docker stop game_server ai_agent >/dev/null 2>&1
docker stop $(docker ps -q --filter name=random_client) >/dev/null 2>&1

# Remove containers
echo "Removing containers..."
docker rm game_server ai_agent >/dev/null 2>&1
docker rm $(docker ps -aq --filter name=random_client) >/dev/null 2>&1

# Stop monitoring
echo "Stopping monitoring..."
pkill -f "monitor_learning.sh" >/dev/null 2>&1

echo "✅ Learning system stopped successfully!"
echo ""
echo "📊 Final Statistics:"
echo "(Note: Detailed statistics require matplotlib for charts)"
echo ""

# Show basic statistics without matplotlib
python3 -c "
import sqlite3
from datetime import datetime

try:
    conn = sqlite3.connect('data/db/game_records.db')
    cursor = conn.cursor()
    
    # Get AI player ID (handle both old and new schemas)
    try:
        cursor.execute('SELECT id FROM players WHERE name = ? AND is_ai = TRUE', ('AILearner',))
        ai_player = cursor.fetchone()
        if not ai_player:
            cursor.execute('SELECT id FROM players WHERE name = ?', ('AILearner',))
            ai_player = cursor.fetchone()
    except:
        cursor.execute('SELECT id FROM players WHERE name = ?', ('AILearner',))
        ai_player = cursor.fetchone()
    
    if ai_player:
        ai_player_id = ai_player[0]
        
        # Get statistics
        cursor.execute('SELECT COUNT(*) FROM game_results WHERE playerid = ?', (ai_player_id,))
        total_games = cursor.fetchone()[0]
        
        if total_games > 0:
            cursor.execute('SELECT result, COUNT(*) FROM game_results WHERE playerid = ? GROUP BY result', (ai_player_id,))
            results = cursor.fetchall()
            
            wins = sum(count for result, count in results if result == 1)
            losses = sum(count for result, count in results if result == 2)
            draws = sum(count for result, count in results if result == 3)
            
            win_rate = (wins / total_games * 100) if total_games > 0 else 0
            loss_rate = (losses / total_games * 100) if total_games > 0 else 0
            draw_rate = (draws / total_games * 100) if total_games > 0 else 0
            
            print(f'🎯 Final Learning Statistics:')
            print(f'   Total Games: {total_games}')
            print(f'   Wins: {wins} ({win_rate:.1f}%)')
            print(f'   Losses: {losses} ({loss_rate:.1f}%)')
            print(f'   Draws: {draws} ({draw_rate:.1f}%)')
            
            if win_rate >= 80:
                print('🎉 Excellent performance! The AI has mastered the game!')
            elif win_rate >= 50:
                print('📈 Good progress! The AI is learning effectively.')
            elif win_rate >= 30:
                print('🎓 Making progress! Keep training for better results.')
            else:
                print('🤖 Still learning! The AI needs more training.')
        else:
            print('📊 No games played yet. Start training to see statistics.')
    else:
        print('🤖 AI player not found. No training data available.')
    
    conn.close()
    
except Exception as e:
    print(f'📊 Could not retrieve statistics: {e}')
    print('This is normal if no training has occurred yet.')
"