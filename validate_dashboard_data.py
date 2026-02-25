#!/usr/bin/env python3
"""
Validation script to verify that dashboard API responses match database data
"""

import requests
import sqlite3
import sys
import json

def validate_dashboard_data():
    print("🔍 Validating dashboard data consistency...")
    print("=" * 50)
    
    # Get data from dashboard API
    try:
        response = requests.get('http://localhost:5000/api/stats', timeout=10)
        if response.status_code != 200:
            print(f"❌ Dashboard API returned status code: {response.status_code}")
            return False
            
        api_data = response.json()
        if 'error' in api_data:
            print(f"❌ Dashboard API returned error: {api_data['error']}")
            return False
            
        print("✅ Dashboard API responded successfully")
    except Exception as e:
        print(f"❌ Error connecting to dashboard API: {e}")
        return False
    
    # Get data from database
    try:
        conn = sqlite3.connect('data/db/game_records.db')
        cursor = conn.cursor()
        
        # Get AILearner player ID
        cursor.execute('SELECT id FROM players WHERE name = ? AND is_ai = TRUE', ('AILearner',))
        ai_player = cursor.fetchone()
        
        if not ai_player:
            print("❌ AILearner not found in database")
            return False
            
        ai_player_id = ai_player[0]
        print(f"✅ Found AILearner with ID: {ai_player_id}")
        
        # Get game results for AILearner from database
        cursor.execute('SELECT COUNT(*) FROM game_results WHERE playerid = ?', (ai_player_id,))
        db_total_games = cursor.fetchone()[0]
        
        cursor.execute('SELECT result, COUNT(*) FROM game_results WHERE playerid = ? GROUP BY result', (ai_player_id,))
        db_results = cursor.fetchall()
        
        db_wins = sum(count for result, count in db_results if result == 1)
        db_losses = sum(count for result, count in db_results if result == 2)
        db_draws = sum(count for result, count in db_results if result == 3)
        
        db_win_rate = (db_wins / db_total_games * 100) if db_total_games > 0 else 0
        db_loss_rate = (db_losses / db_total_games * 100) if db_total_games > 0 else 0
        db_draw_rate = (db_draws / db_total_games * 100) if db_total_games > 0 else 0
        
        conn.close()
        
        print(f"📊 Database stats for AILearner: {db_total_games} games ({db_wins} wins, {db_losses} losses, {db_draws} draws)")
        
    except Exception as e:
        print(f"❌ Error querying database: {e}")
        return False
    
    # Compare API data with database data
    print("\n📋 Comparing API vs Database data...")
    
    validation_passed = True
    
    if api_data['total_games'] != db_total_games:
        print(f"❌ Total games mismatch: API={api_data['total_games']}, DB={db_total_games}")
        validation_passed = False
    else:
        print(f"✅ Total games match: {api_data['total_games']}")
    
    if api_data['wins'] != db_wins:
        print(f"❌ Wins mismatch: API={api_data['wins']}, DB={db_wins}")
        validation_passed = False
    else:
        print(f"✅ Wins match: {api_data['wins']}")
    
    if api_data['losses'] != db_losses:
        print(f"❌ Losses mismatch: API={api_data['losses']}, DB={db_losses}")
        validation_passed = False
    else:
        print(f"✅ Losses match: {api_data['losses']}")
    
    if api_data['draws'] != db_draws:
        print(f"❌ Draws mismatch: API={api_data['draws']}, DB={db_draws}")
        validation_passed = False
    else:
        print(f"✅ Draws match: {api_data['draws']}")
    
    # Compare rates (allow small floating point differences)
    if abs(api_data['win_rate'] - db_win_rate) > 0.1:
        print(f"❌ Win rate mismatch: API={api_data['win_rate']:.1f}, DB={db_win_rate:.1f}")
        validation_passed = False
    else:
        print(f"✅ Win rate match: {api_data['win_rate']:.1f}%")
    
    if abs(api_data['loss_rate'] - db_loss_rate) > 0.1:
        print(f"❌ Loss rate mismatch: API={api_data['loss_rate']:.1f}, DB={db_loss_rate:.1f}")
        validation_passed = False
    else:
        print(f"✅ Loss rate match: {api_data['loss_rate']:.1f}%")
    
    if abs(api_data['draw_rate'] - db_draw_rate) > 0.1:
        print(f"❌ Draw rate mismatch: API={api_data['draw_rate']:.1f}, DB={db_draw_rate:.1f}")
        validation_passed = False
    else:
        print(f"✅ Draw rate match: {api_data['draw_rate']:.1f}%")
    
    print("\n" + "=" * 50)
    if validation_passed:
        print("🎉 All validations passed! Dashboard data matches database data.")
        return True
    else:
        print("💥 Validation failed! Dashboard data does not match database data.")
        return False

if __name__ == '__main__':
    success = validate_dashboard_data()
    sys.exit(0 if success else 1)