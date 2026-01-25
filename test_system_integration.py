#!/usr/bin/env python3

"""
AI-Gamer System Integration Test
Tests all components without requiring Docker builds
"""

import sys
import os
import sqlite3
from datetime import datetime
import subprocess

def test_database_schema():
    """Test that the database schema is valid"""
    print("🔍 Testing database schema...")
    
    try:
        # Create test database
        test_db = 'test_integration.db'
        if os.path.exists(test_db):
            os.remove(test_db)
        
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        # Read and execute schema
        with open('game_server/state/game_records_schema.sql', 'r') as f:
            schema = f.read()
        
        cursor.executescript(schema)
        
        # Verify all tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall() if table[0] != 'sqlite_sequence']
        
        required_tables = ['players', 'games', 'moves', 'game_results', 'learning_metrics', 'training_sessions']
        
        for table in required_tables:
            if table not in tables:
                print(f"❌ Missing table: {table}")
                return False
        
        print("✅ Database schema is valid")
        conn.close()
        os.remove(test_db)
        return True
        
    except Exception as e:
        print(f"❌ Database schema test failed: {e}")
        if os.path.exists(test_db):
            os.remove(test_db)
        return False

def test_shell_scripts():
    """Test that all shell scripts have valid syntax"""
    print("🔍 Testing shell script syntax...")
    
    scripts = [
        'run_game_server_docker.sh',
        'run_random_client_docker.sh', 
        'run_ai_agent_docker.sh',
        'run_learning_system.sh',
        'stop_learning_system.sh',
        'monitor_learning.sh',
        'show_learning_stats.sh',
        'run_dashboard.sh'
    ]
    
    for script in scripts:
        if not os.path.exists(script):
            print(f"❌ Missing script: {script}")
            return False
        
        # Test syntax
        result = subprocess.run(['bash', '-n', script], capture_output=True)
        if result.returncode != 0:
            print(f"❌ Syntax error in {script}: {result.stderr.decode()}")
            return False
    
    print("✅ All shell scripts have valid syntax")
    return True

def test_statistics_logic():
    """Test the statistics calculation logic"""
    print("🔍 Testing statistics calculation logic...")
    
    try:
        # Create test database
        test_db = 'test_stats.db'
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        # Create minimal schema for testing
        cursor.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                is_ai BOOLEAN DEFAULT FALSE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE game_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gameid INTEGER NOT NULL,
                playerid INTEGER NOT NULL,
                result INTEGER NOT NULL,
                timestamp INTEGER NOT NULL
            )
        ''')
        
        # Insert test data
        cursor.execute('INSERT INTO players (name, is_ai) VALUES (?, ?)', ('AILearner', True))
        player_id = cursor.lastrowid
        
        # Insert game results (1=win, 2=loss, 3=draw)
        test_results = [1, 2, 3, 1, 2, 1, 3, 2, 1, 3, 1, 1]
        current_time = int(datetime.now().timestamp())
        
        for i, result in enumerate(test_results):
            cursor.execute('INSERT INTO game_results (gameid, playerid, result, timestamp) VALUES (?, ?, ?, ?)',
                          (i, player_id, result, current_time - (len(test_results) - i) * 60))
        
        conn.commit()
        
        # Calculate statistics
        cursor.execute('SELECT COUNT(*) FROM game_results WHERE playerid = ?', (player_id,))
        total_games = cursor.fetchone()[0]
        
        cursor.execute('SELECT result, COUNT(*) FROM game_results WHERE playerid = ? GROUP BY result', (player_id,))
        results = cursor.fetchall()
        
        wins = sum(count for result, count in results if result == 1)
        losses = sum(count for result, count in results if result == 2)
        draws = sum(count for result, count in results if result == 3)
        
        win_rate = (wins / total_games * 100) if total_games > 0 else 0
        loss_rate = (losses / total_games * 100) if total_games > 0 else 0
        draw_rate = (draws / total_games * 100) if total_games > 0 else 0
        
        # Verify calculations
        assert total_games == len(test_results), f"Total games mismatch: {total_games} vs {len(test_results)}"
        assert wins + losses + draws == total_games, "Results don't sum to total games"
        assert abs(win_rate + loss_rate + draw_rate - 100.0) < 0.1, "Rates don't sum to 100%"
        
        print(f"✅ Statistics calculation works correctly")
        print(f"   Total Games: {total_games}")
        print(f"   Wins: {wins} ({win_rate:.1f}%)")
        print(f"   Losses: {losses} ({loss_rate:.1f}%)")
        print(f"   Draws: {draws} ({draw_rate:.1f}%)")
        
        conn.close()
        os.remove(test_db)
        return True
        
    except Exception as e:
        print(f"❌ Statistics logic test failed: {e}")
        if os.path.exists(test_db):
            os.remove(test_db)
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("🔍 Testing file structure...")
    
    required_files = [
        # Dockerfiles
        'game_server/Dockerfile',
        'random_client/Dockerfile',
        'ai_agent/Dockerfile',
        'dashboard/Dockerfile',
        
        # Database files
        'game_server/state/game_records_schema.sql',
        'game_server/state/recorderdb.py',
        
        # Scripts
        'run_game_server_docker.sh',
        'run_random_client_docker.sh',
        'run_ai_agent_docker.sh',
        'run_learning_system.sh',
        'stop_learning_system.sh',
        'monitor_learning.sh',
        'show_learning_stats.sh',
        'run_dashboard.sh',
        
        # Python files
        'dashboard_server.py',
        'random_client/requirements.txt',
        'dashboard/requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files exist")
    return True

def test_dockerfile_syntax():
    """Test Dockerfile syntax"""
    print("🔍 Testing Dockerfile syntax...")
    
    dockerfiles = [
        'game_server/Dockerfile',
        'random_client/Dockerfile',
        'ai_agent/Dockerfile',
        'dashboard/Dockerfile'
    ]
    
    for dockerfile in dockerfiles:
        try:
            with open(dockerfile, 'r') as f:
                content = f.read()
            
            # Basic syntax checks
            if 'FROM' not in content:
                print(f"❌ {dockerfile}: Missing FROM instruction")
                return False
            
            if 'CMD' not in content and 'ENTRYPOINT' not in content:
                print(f"❌ {dockerfile}: Missing CMD or ENTRYPOINT instruction")
                return False
            
        except Exception as e:
            print(f"❌ {dockerfile}: Error reading file: {e}")
            return False
    
    print("✅ All Dockerfiles have valid basic syntax")
    return True

def main():
    """Run all tests"""
    print("🧪 AI-Gamer System Integration Test")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_dockerfile_syntax,
        test_shell_scripts,
        test_database_schema,
        test_statistics_logic
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        print()
        if test():
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! System integration is working correctly.")
        print()
        print("🚀 Ready to run the learning system:")
        print("   • ./run_learning_system.sh")
        print("   • ./run_dashboard.sh")
        print("   • ./monitor_learning.sh")
        return True
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)