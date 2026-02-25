#!/usr/bin/env python3
"""
Analyze AI Learning Progress Over Time
Checks if AI performance improves as it plays more games
"""

import sqlite3
import time
from datetime import datetime

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect('data/db/game_records.db')

def get_ai_performance_by_time_window(hours_back=None):
    """Get AI performance in time windows to see if it's improving"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all games with timestamps
    if hours_back:
        # Get games from last N hours
        cursor.execute('''
            SELECT g.id, g.date, p.name, gr.result
            FROM games g
            JOIN game_results gr ON g.id = gr.gameid
            JOIN players p ON gr.playerid = p.id
            WHERE g.date > ?  -- Assuming date is in milliseconds
            ORDER BY g.date ASC
        ''', (int((time.time() - hours_back * 3600) * 1000),))
    else:
        # Get all games
        cursor.execute('''
            SELECT g.id, g.date, p.name, gr.result
            FROM games g
            JOIN game_results gr ON g.id = gr.gameid
            JOIN players p ON gr.playerid = p.id
            ORDER BY g.date ASC
        ''')
    
    all_results = cursor.fetchall()
    
    # Separate by player
    ai_results = []
    random_results = []
    
    for game_id, timestamp, player_name, result in all_results:
        if 'AI' in player_name or 'Learner' in player_name:
            ai_results.append((game_id, timestamp, result))
        elif 'Random' in player_name or 'Bot' in player_name:
            random_results.append((game_id, timestamp, result))
    
    conn.close()
    
    return ai_results, random_results

def calculate_win_rate(results, total_games):
    """Calculate win rate from results"""
    if not results or total_games == 0:
        return 0, 0, 0, 0  # wins, losses, draws, win_rate
    
    wins = sum(1 for _, _, result in results if result == 1)
    losses = sum(1 for _, _, result in results if result == 2)
    draws = sum(1 for _, _, result in results if result == 3)
    
    win_rate = (wins / total_games * 100) if total_games > 0 else 0
    return wins, losses, draws, win_rate

def analyze_learning_progress():
    """Analyze if AI is learning over time"""
    print("🔬 AI Learning Progress Analysis")
    print("=" * 60)
    
    # Get all results
    ai_results, random_results = get_ai_performance_by_time_window(None)
    
    if not ai_results:
        print("No AI results found in database")
        return
    
    total_games = len(ai_results)  # Each game has 2 results (one for each player)
    
    print(f"Total games analyzed: {total_games//2}")  # Divide by 2 since each game has 2 entries
    print()
    
    # Split results into early and late games to see if there's improvement
    if len(ai_results) >= 100:  # Need enough games to split meaningfully
        mid_point = len(ai_results) // 2
        
        early_ai = ai_results[:mid_point]
        late_ai = ai_results[mid_point:]
        
        early_total = len(early_ai)
        late_total = len(late_ai)
        
        if early_total > 0 and late_total > 0:
            early_wins, early_losses, early_draws, early_win_rate = calculate_win_rate(early_ai, early_total)
            late_wins, late_losses, late_draws, late_win_rate = calculate_win_rate(late_ai, late_total)
            
            print("📊 EARLY GAMES PERFORMANCE (first half):")
            print(f"   Games: {early_total} ({early_wins} wins, {early_losses} losses, {early_draws} draws)")
            print(f"   Win Rate: {early_win_rate:.1f}%")
            
            print()
            print("📈 LATER GAMES PERFORMANCE (second half):")
            print(f"   Games: {late_total} ({late_wins} wins, {late_losses} losses, {late_draws} draws)")
            print(f"   Win Rate: {late_win_rate:.1f}%")
            
            print()
            improvement = late_win_rate - early_win_rate
            if improvement > 2.0:  # Significant improvement threshold
                print(f"✅ IMPROVEMENT DETECTED: +{improvement:.1f}% win rate improvement!")
            elif improvement < -2.0:  # Significant decline
                print(f"❌ PERFORMANCE DECLINE: {improvement:.1f}% win rate decline")
            else:
                print(f"➡️  NO SIGNIFICANT CHANGE: {improvement:.1f}% change in win rate")
    
    # Overall performance
    total_ai_games = len(ai_results)
    if total_ai_games > 0:
        total_wins, total_losses, total_draws, total_win_rate = calculate_win_rate(ai_results, total_ai_games)
        
        print()
        print("🏆 OVERALL AI PERFORMANCE:")
        print(f"   Total Games: {total_ai_games}")
        print(f"   Wins: {total_wins} ({total_wins/total_ai_games*100:.1f}%)")
        print(f"   Losses: {total_losses} ({total_losses/total_ai_games*100:.1f}%)")
        print(f"   Draws: {total_draws} ({total_draws/total_ai_games*100:.1f}%)")
        print(f"   Overall Win Rate: {total_win_rate:.1f}%")
        
        # Compare with random player
        total_random_games = len(random_results)
        if total_random_games > 0:
            random_wins, random_losses, random_draws, random_win_rate = calculate_win_rate(random_results, total_random_games)
            print()
            print("🤖 VS RANDOM BOT COMPARISON:")
            print(f"   Random Bot Win Rate: {random_win_rate:.1f}%")
            print(f"   AI Learner Win Rate: {total_win_rate:.1f}%")
            
            if total_win_rate > random_win_rate:
                print("   🏆 AI is outperforming Random Bot!")
            elif total_win_rate > 35:  # Above random baseline
                print("   📈 AI is performing above random baseline")
            elif total_win_rate > 25:  # Around random baseline
                print("   🤔 AI is performing around random level")
            else:
                print("   📉 AI is performing below random level - needs improvement")
    
    print()
    print("💡 LEARNING INDICATORS:")
    print("   • Positive trend in win rate over time = Learning happening")
    print("   • Win rate > 30% = Better than random play")
    print("   • Win rate > 50% = Outperforming opponent")
    print("   • Consistent improvement = Effective learning")

if __name__ == "__main__":
    analyze_learning_progress()