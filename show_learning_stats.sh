#!/bin/bash

# Simple Learning Statistics Viewer
# Shows AI learning progress without requiring matplotlib

echo "📊 AI-Gamer Learning Statistics (Simple)"
echo "========================================"
echo ""

python3 -c "
import sqlite3
import sys
from datetime import datetime

try:
    conn = sqlite3.connect('data/db/game_records.db')
    cursor = conn.cursor()
    
    # Get AI player ID using new schema
    cursor.execute('SELECT id FROM players WHERE name = ? AND is_ai = TRUE', ('AILearner',))
    ai_player = cursor.fetchone()
    
    if not ai_player:
        print('❌ AI player not found in database')
        print('Make sure the AI agent has played some games first.')
        print('Run: ./run_learning_system.sh')
        sys.exit(0)
    
    ai_player_id = ai_player[0]
    
    # Get overall statistics
    cursor.execute('SELECT COUNT(*) FROM game_results WHERE playerid = ?', (ai_player_id,))
    total_games = cursor.fetchone()[0]
    
    if total_games == 0:
        print('📊 No games played yet. Start the learning system to begin training!')
        print('Run: ./run_learning_system.sh')
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
    
    if losses > 0:
        win_loss_ratio = wins / losses
        print(f'Win/Loss Ratio: {win_loss_ratio:.2f}')
    else:
        print('Win/Loss Ratio: ∞ (no losses yet!)')
    
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
        for win_rate, timestamp in progress_data[-10:]:  # Show last 10 entries
            date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f'{date_str}  {win_rate*100:.1f}%')
        
        if len(progress_data) > 10:
            print(f'... and {len(progress_data) - 10} more entries')
        
        # Calculate improvement
        initial_win_rate = progress_data[0][0] * 100
        current_win_rate = progress_data[-1][0] * 100
        improvement = current_win_rate - initial_win_rate
        
        print('')
        print(f'Initial Win Rate: {initial_win_rate:.1f}%')
        print(f'Current Win Rate: {current_win_rate:.1f}%')
        print(f'Improvement: {improvement:+.1f}%')
        print('')
    
    # Get training sessions
    cursor.execute('''
        SELECT start_time, end_time, initial_win_rate, final_win_rate, episodes
        FROM training_sessions
        WHERE playerid = ?
        ORDER BY start_time DESC
        LIMIT 3
    ''', (ai_player_id,))
    
    sessions = cursor.fetchall()
    
    if sessions:
        print('🎓 RECENT TRAINING SESSIONS')
        print('==========================')
        
        for i, session in enumerate(sessions):
            start_time = datetime.fromtimestamp(session[0])
            end_time = datetime.fromtimestamp(session[1]) if session[1] else 'Now'
            
            if session[1]:
                duration = end_time - start_time if isinstance(end_time, datetime) else 'Ongoing'
                improvement = ((session[3] - session[2]) * 100) if session[3] and session[2] else 0
                print(f'Session {i+1}: {start_time} to {end_time}')
                print(f'  Duration: {duration}')
                print(f'  Initial Win Rate: {session[2]*100:.1f}%')
                print(f'  Final Win Rate: {session[3]*100:.1f}%')
                print(f'  Improvement: {improvement:+.1f}%')
                print(f'  Episodes: {session[4]}')
            else:
                duration = datetime.now() - start_time
                print(f'Session {i+1}: {start_time} to Now ({duration})')
                print(f'  Initial Win Rate: {session[2]*100:.1f}%')
                print(f'  Current Win Rate: Calculating...')
                print(f'  Episodes: {session[4]}')
            print('')
        
        if len(sessions) > 3:
            print(f'... and {len(sessions) - 3} older sessions')
    
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
    print('💡 PERFORMANCE ANALYSIS')
    print('======================')
    
    if win_rate >= 80:
        print('🎉 Excellent performance! The AI has mastered this game configuration.')
        print('   Consider increasing board size or trying a different game.')
    elif win_rate >= 60:
        print('📈 Great progress! The AI is performing very well.')
        print('   Continue training to reach mastery level.')
    elif win_rate >= 40:
        print('🎓 Good progress! The AI is learning effectively.')
        print('   Keep training to improve strategy.')
    elif win_rate >= 20:
        print('🤖 Making progress! The AI is starting to understand the game.')
        print('   Continue training for better results.')
    else:
        print('🤖 Still learning! The AI is in the early exploration phase.')
        print('   Let it play more games to learn basic patterns.')
    
    print('')
    print('📊 To see real-time progress, run: ./monitor_learning.sh')
    print('🎮 To start training, run: ./run_learning_system.sh')
    print('🌐 For visual dashboard, run: ./run_dashboard.sh')
    
    conn.close()
    
except Exception as e:
    print(f'❌ Error getting statistics: {e}')
    print('This might be normal if no training has occurred yet.')
    import traceback
    traceback.print_exc()
" 