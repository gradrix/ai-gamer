#!/bin/bash

# AI-Gamer Learning Statistics Viewer
# Shows detailed learning progress and performance metrics

echo "📊 AI-Gamer Learning Statistics"
echo "================================"
echo ""

python3 -c "
import sqlite3
import sys
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

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
        print('❌ AI player not found in database')
        print('Make sure the AI agent has played some games first.')
        sys.exit(0)
    
    ai_player_id = ai_player[0]
    
    # Get overall statistics
    cursor.execute('SELECT COUNT(*) FROM game_results WHERE playerid = ?', (ai_player_id,))
    total_games = cursor.fetchone()[0]
    
    if total_games == 0:
        print('📊 No games played yet. Start the learning system to begin training!')
        sys.exit(0)
    
    # Get wins, losses, draws
    cursor.execute('SELECT result, COUNT(*) FROM game_results WHERE playerid = ? GROUP BY result', (ai_player_id,))
    results = cursor.fetchall()
    
    wins = 0
    losses = 0
    draws = 0
    
    for result, count in results:
        if result == 1:  # Win
            wins = count
        elif result == 2:  # Loss
            losses = count
        elif result == 3:  # Draw
            draws = count
    
    win_rate = (wins / total_games * 100) if total_games > 0 else 0
    loss_rate = (losses / total_games * 100) if total_games > 0 else 0
    draw_rate = (draws / total_games * 100) if total_games > 0 else 0
    
    print('🎯 OVERALL PERFORMANCE')
    print('======================')
    print(f'Total Games Played: {total_games}')
    print(f'Wins: {wins} ({win_rate:.1f}%)')
    print(f'Losses: {losses} ({loss_rate:.1f}%)')
    print(f'Draws: {draws} ({draw_rate:.1f}%)')
    print(f'Win/Loss Ratio: {wins/losses:.2f}' if losses > 0 else 'Win/Loss Ratio: ∞')
    print('')
    
    # Get learning progress over time
    cursor.execute('''
        SELECT win_rate, timestamp
        FROM learning_metrics
        WHERE playerid = ?
        ORDER BY timestamp ASC
    ''', (ai_player_id,))
    
    progress_data = cursor.fetchall()
    
    if progress_data:
        print('📈 LEARNING PROGRESS')
        print('===================')
        
        # Show progress table
        print('Timestamp                   Win Rate')
        print('-' * 45)
        for win_rate, timestamp in progress_data[:10]:  # Show last 10 entries
            date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f'{date_str}  {win_rate*100:.1f}%')
        
        if len(progress_data) > 10:
            print(f'... and {len(progress_data) - 10} more entries')
        
        print('')
        
        # Generate progress chart
        timestamps = [datetime.fromtimestamp(ts) for _, ts in progress_data]
        win_rates = [wr * 100 for wr, _ in progress_data]
        
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, win_rates, marker='o', linestyle='-', color='b')
        plt.title('AI Learning Progress - Win Rate Over Time')
        plt.xlabel('Time')
        plt.ylabel('Win Rate (%)')
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)
        
        # Save the chart
        plt.savefig('data/learning_progress.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print('📊 Progress chart saved to: data/learning_progress.png')
        print('')
    
    # Get training sessions
    cursor.execute('''
        SELECT start_time, end_time, initial_win_rate, final_win_rate, episodes
        FROM training_sessions
        WHERE playerid = ?
        ORDER BY start_time DESC
    ''', (ai_player_id,))
    
    sessions = cursor.fetchall()
    
    if sessions:
        print('🎓 TRAINING SESSIONS')
        print('===================')
        
        for i, session in enumerate(sessions[:5]):  # Show last 5 sessions
            start_time = datetime.fromtimestamp(session[0])
            end_time = datetime.fromtimestamp(session[1]) if session[1] else 'Now'
            duration = end_time - start_time if isinstance(end_time, datetime) else 'Ongoing'
            
            print(f'Session {i+1}:')
            print(f'  Start: {start_time}')
            print(f'  End: {end_time}')
            print(f'  Duration: {duration}')
            print(f'  Initial Win Rate: {session[2]*100:.1f}%')
            print(f'  Final Win Rate: {session[3]*100:.1f}%' if session[3] else '  Final Win Rate: Ongoing')
            print(f'  Episodes: {session[4]}')
            print(f'  Improvement: {((session[3] - session[2])*100):.1f}%' if session[3] and session[2] else '  Improvement: Calculating...')
            print('')
        
        if len(sessions) > 5:
            print(f'... and {len(sessions) - 5} more sessions')
    
    # Get recent game details
    cursor.execute('''
        SELECT g.id, g.date, g.board_size, gr.result
        FROM games g
        JOIN game_results gr ON g.id = gr.gameid
        WHERE gr.playerid = ?
        ORDER BY g.date DESC
        LIMIT 5
    ''', (ai_player_id,))
    
    recent_games = cursor.fetchall()
    
    if recent_games:
        print('🎮 RECENT GAMES')
        print('==============')
        
        result_map = {1: 'Win', 2: 'Loss', 3: 'Draw'}
        
        for game in recent_games:
            game_id, timestamp, board_size, result = game
            date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            result_str = result_map.get(result, 'Unknown')
            
            print(f'Game {game_id}: {date_str}')
            print(f'  Board Size: {board_size}x{board_size}')
            print(f'  Result: {result_str}')
            print('')
    
    # Show recommendations
    print('💡 RECOMMENDATIONS')
    print('=================')
    
    if win_rate < 30:
        print('The AI is still learning the basics. Keep training!')
    elif win_rate < 60:
        print('The AI is making progress but still has room for improvement.')
    elif win_rate < 80:
        print('The AI is performing well! Consider increasing the difficulty.')
    else:
        print('Excellent performance! The AI has mastered this game configuration.')
    
    print('')
    print('📈 To see real-time progress, run: ./monitor_learning.sh')
    print('🎮 To start training, run: ./run_learning_system.sh')
    
    conn.close()
    
except Exception as e:
    print(f'❌ Error getting statistics: {e}')
    import traceback
    traceback.print_exc()
" 