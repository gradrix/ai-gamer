#!/usr/bin/env python3
"""
Track AI Learner Progress Over Time
Monitors learning progress by periodically checking game statistics
"""

import sqlite3
import time
import os
from datetime import datetime

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect('data/db/game_records.db')

def get_player_stats():
    """Get current player statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get player stats
    cursor.execute('''
        SELECT p.name, 
               COUNT(*) as total_games,
               SUM(CASE WHEN gr.result = 1 THEN 1 ELSE 0 END) as wins,
               SUM(CASE WHEN gr.result = 2 THEN 1 ELSE 0 END) as losses,
               SUM(CASE WHEN gr.result = 3 THEN 1 ELSE 0 END) as draws
        FROM game_results gr
        JOIN players p ON gr.playerid = p.id
        GROUP BY p.name
    ''')
    
    stats = {}
    for name, total, wins, losses, draws in cursor.fetchall():
        win_rate = (wins / total * 100) if total > 0 else 0
        stats[name] = {
            'total_games': total,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': win_rate
        }
    
    conn.close()
    return stats

def main():
    print("🤖 AI-Learner Progress Tracker")
    print("=" * 50)
    print(f"{'Time':<12} {'Games':<8} {'Wins':<6} {'Losses':<7} {'Draws':<6} {'Win%':<6} {'AILearn Win%':<12}")
    print("-" * 85)
    
    start_time = time.time()
    last_ai_wins = 0
    last_total_games = 0
    
    while True:
        try:
            stats = get_player_stats()
            
            # Find AI Learner stats
            ai_stats = None
            random_stats = None
            
            for name, stat in stats.items():
                if 'AILearner' in name or 'AI' in name:
                    ai_stats = stat
                elif 'Random' in name or 'Bot' in name:
                    random_stats = stat
            
            if ai_stats and random_stats:
                total_games = ai_stats['total_games']  # Both should have same number
                
                # Calculate improvement since last check
                games_since_last = total_games - last_total_games
                ai_wins_since_last = ai_stats['wins'] - last_ai_wins
                
                print(f"{datetime.now().strftime('%H:%M:%S'):<12} {total_games:<8} {ai_stats['wins']:<6} "
                      f"{ai_stats['losses']:<7} {ai_stats['draws']:<6} {ai_stats['win_rate']:<6.1f} "
                      f"{ai_stats['win_rate']:<12.1f}")
                
                # Track improvement
                if games_since_last > 0:
                    print(f"             (+{games_since_last} games, +{ai_wins_since_last} wins since last check)")
                
                last_ai_wins = ai_stats['wins']
                last_total_games = total_games
                
                # Check if AI has reached 1000 games
                if total_games >= 1000:
                    print(f"\n🎯 TARGET REACHED: AI Learner has played {total_games} games!")
                    
                    # Final analysis
                    print(f"\n📊 FINAL ANALYSIS:")
                    print(f"   AI Learner: {ai_stats['wins']} wins, {ai_stats['losses']} losses, {ai_stats['draws']} draws")
                    print(f"   Win Rate: {ai_stats['win_rate']:.1f}%")
                    print(f"   Random Bot: {random_stats['wins']} wins, {random_stats['losses']} losses, {random_stats['draws']} draws")
                    print(f"   Win Rate: {(random_stats['wins']/total_games*100):.1f}%")
                    
                    if ai_stats['win_rate'] > 25:  # If AI improved beyond random chance
                        improvement = ai_stats['win_rate'] - 25  # Baseline for random play
                        print(f"   📈 IMPROVEMENT: AI gained {improvement:.1f}% above random baseline!")
                    else:
                        print(f"   📉 CONCERN: AI win rate is below random baseline")
                    
                    break
            
            # Check every 30 seconds
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"Error getting stats: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()