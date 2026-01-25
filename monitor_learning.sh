#!/bin/bash

# AI-Gamer Learning Progress Monitor
# Continuously tracks and displays AI learning progress

echo "📈 AI-Gamer Learning Progress Monitor"
echo "======================================"
echo "Press Ctrl+C to stop monitoring"
echo ""

# Function to get current statistics
get_stats() {
    python3 -c "
import sqlite3
import sys
from datetime import datetime

try:
    conn = sqlite3.connect('data/db/game_records.db')
    cursor = conn.cursor()
    
    # Get AI player ID (handle both old and new database schemas)
    try:
        cursor.execute('SELECT id FROM players WHERE name = ? AND is_ai = TRUE', ('AILearner',))
        ai_player = cursor.fetchone()
        
        if not ai_player:
            # Fallback: try without is_ai filter for old databases
            cursor.execute('SELECT id FROM players WHERE name = ?', ('AILearner',))
            ai_player = cursor.fetchone()
    except sqlite3.OperationalError:
        # Old database schema without is_ai column
        cursor.execute('SELECT id FROM players WHERE name = ?', ('AILearner',))
        ai_player = cursor.fetchone()
    
    if not ai_player:
        print('AI player not found in database')
        print('Make sure the AI agent has registered with the game server.')
        sys.exit(0)
    
    ai_player_id = ai_player[0]
    
    # Get total games played
    cursor.execute('SELECT COUNT(*) FROM game_results WHERE playerid = ?', (ai_player_id,))
    total_games = cursor.fetchone()[0]
    
    # Get wins, losses, draws
    cursor.execute('SELECT result, COUNT(*) FROM game_results WHERE playerid = ? GROUP BY result', (ai_player_id,))
    results = cursor.fetchall()
    
    wins = 0
    losses = 0
    draws = 0
    
    for result, count in results:
        if result == 1:  # Assuming 1 = win
            wins = count
        elif result == 2:  # Assuming 2 = loss
            losses = count
        elif result == 3:  # Assuming 3 = draw
            draws = count
    
    # Calculate rates
    win_rate = (wins / total_games * 100) if total_games > 0 else 0
    loss_rate = (losses / total_games * 100) if total_games > 0 else 0
    draw_rate = (draws / total_games * 100) if total_games > 0 else 0
    
    # Get recent learning metrics
    cursor.execute('''
        SELECT win_rate, loss_rate, draw_rate, timestamp
        FROM learning_metrics
        WHERE playerid = ?
        ORDER BY timestamp DESC
        LIMIT 1
    ''', (ai_player_id,))
    
    recent_metric = cursor.fetchone()
    
    # Get training session info
    cursor.execute('''
        SELECT start_time, end_time, initial_win_rate, final_win_rate, episodes
        FROM training_sessions
        WHERE playerid = ?
        ORDER BY start_time DESC
        LIMIT 1
    ''', (ai_player_id,))
    
    training_session = cursor.fetchone()
    
    print(f'📊 AI Learning Progress - {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}')
    print(f'🎮 Total Games Played: {total_games}')
    print(f'🏆 Wins: {wins} ({win_rate:.1f}%)')
    print(f'💀 Losses: {losses} ({loss_rate:.1f}%)')
    print(f'⚖️  Draws: {draws} ({draw_rate:.1f}%)')
    
    if recent_metric:
        recent_win_rate = recent_metric[0] * 100
        print(f'📈 Recent Win Rate: {recent_win_rate:.1f}%')
    
    if training_session:
        start_time = datetime.fromtimestamp(training_session[0])
        if training_session[1]:
            end_time = datetime.fromtimestamp(training_session[1])
            duration = end_time - start_time
            print(f'🕒 Current Training Session: {start_time} - {end_time} ({duration})')
            print(f'📊 Progress: {training_session[2]*100:.1f}% → {training_session[3]*100:.1f}% win rate')
            print(f'🎯 Episodes: {training_session[4]}')
        else:
            duration = datetime.now() - start_time
            print(f'🕒 Current Training Session: {start_time} - Now ({duration})')
            print(f'📊 Starting Win Rate: {training_session[2]*100:.1f}%')
            print(f'🎯 Episodes: {training_session[4]}')
    
    conn.close()
    
except Exception as e:
    print(f'Error getting statistics: {e}')
"
}

# Main monitoring loop
while true; do
    clear
    echo "📈 AI-Gamer Learning Progress Monitor"
    echo "======================================"
    echo "Monitoring AI learning progress in real-time..."
    echo ""
    
    get_stats
    
    echo ""
    echo "🔄 Next update in 10 seconds..."
    sleep 10
done