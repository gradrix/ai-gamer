#!/usr/bin/env python3

"""
AI-Gamer Learning Dashboard
Simple web interface to visualize AI learning progress
"""

import sqlite3
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from flask import Flask, render_template_string, jsonify, send_from_directory
import os
import threading
import time

app = Flask(__name__)

# HTML Template for the dashboard
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Gamer Learning Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-card h3 {
            font-size: 1.2em;
            margin-bottom: 10px;
            color: #e0e0e0;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .chart-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .chart-container h2 {
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        
        .chart-container img {
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        .recent-games {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .recent-games h2 {
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        
        .game-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            border-left: 4px solid;
        }
        
        .game-item.win {
            border-left-color: #4CAF50;
        }
        
        .game-item.loss {
            border-left-color: #F44336;
        }
        
        .game-item.draw {
            border-left-color: #2196F3;
        }
        
        .game-item:last-child {
            margin-bottom: 0;
        }
        
        .game-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }
        
        .game-id {
            font-weight: bold;
            color: #e0e0e0;
        }
        
        .game-time {
            font-size: 0.8em;
            opacity: 0.7;
        }
        
        .game-result {
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .game-result.win {
            color: #4CAF50;
        }
        
        .game-result.loss {
            color: #F44336;
        }
        
        .game-result.draw {
            color: #2196F3;
        }
        
        .game-details {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .refresh-btn {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
            margin: 20px auto;
            display: block;
        }
        
        .refresh-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            font-size: 1.2em;
        }
        
        .error {
            background: #F44336;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 AI-Gamer Learning Dashboard</h1>

        <div id="content">
            <div class="loading">Loading AI learning data...</div>
        </div>
    </div>

    <script>
        function refreshData() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('content').innerHTML =
                            '<div class="error">🚨 ' + data.error + '</div>';
                    } else {
                        renderDashboard(data);
                    }
                })
                .catch(error => {
                    document.getElementById('content').innerHTML =
                        '<div class="error">🚨 Error loading data: ' + error.message + '</div>';
                });
        }

        function renderDashboard(data) {
            const contentDiv = document.getElementById('content');

            // Create a temporary div to build the new content
            const tempDiv = document.createElement('div');
            tempDiv.style.opacity = '0';
            tempDiv.style.transition = 'opacity 0.3s ease-in-out';

            let html = '';

            // Stats Cards
            html += '<div class="stats-grid">';
            html += '<div class="stat-card">';
            html += '<h3>Total Games</h3>';
            html += '<div class="stat-value">' + data.total_games + '</div>';
            html += '<div class="stat-label">Played</div>';
            html += '</div>';

            html += '<div class="stat-card">';
            html += '<h3>Win Rate</h3>';
            html += '<div class="stat-value">' + data.win_rate.toFixed(1) + '%</div>';
            html += '<div class="stat-label">' + data.wins + ' wins</div>';
            html += '</div>';

            html += '<div class="stat-card">';
            html += '<h3>Loss Rate</h3>';
            html += '<div class="stat-value">' + data.loss_rate.toFixed(1) + '%</div>';
            html += '<div class="stat-label">' + data.losses + ' losses</div>';
            html += '</div>';

            html += '<div class="stat-card">';
            html += '<h3>Draw Rate</h3>';
            html += '<div class="stat-value">' + data.draw_rate.toFixed(1) + '%</div>';
            html += '<div class="stat-label">' + data.draws + ' draws</div>';
            html += '</div>';
            html += '</div>';

            // Progress Chart
            if (data.has_progress_data) {
                html += '<div class="chart-container">';
                html += '<h2>📈 Learning Progress Over Time</h2>';
                html += '<div class="chart-placeholder" style="width:100%; height:400px; position:relative; background-color: #f8f9fa;">';
                html += '<img src="/chart?cache=' + Date.now() + '" alt="Learning Progress Chart" style="width:100%; height:100%; object-fit:contain; display:block;" onload="this.style.display=\'block\'; this.parentNode.querySelector(\'.chart-loading\').style.display=\'none\';" onerror="this.style.display=\'none\'; this.parentNode.querySelector(\'.chart-loading\').textContent=\'Chart failed to load\';">';
                html += '<div class="chart-loading" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);">Loading chart...</div>';
                html += '</div>';
                html += '</div>';
            }

            // Win/Loss Ratio Chart
            if (data.has_win_loss_data) {
                html += '<div class="chart-container">';
                html += '<h2>📊 Win/Loss Ratio Over Time</h2>';
                html += '<div class="chart-placeholder" style="width:100%; height:400px; position:relative; background-color: #f8f9fa;">';
                html += '<img src="/win-loss-chart?cache=' + Date.now() + '" alt="Win/Loss Ratio Chart" style="width:100%; height:100%; object-fit:contain; display:block;" onload="this.style.display=\'block\'; this.parentNode.querySelector(\'.chart-loading\').style.display=\'none\';" onerror="this.style.display=\'none\'; this.parentNode.querySelector(\'.chart-loading\').textContent=\'Chart failed to load\';">';
                html += '<div class="chart-loading" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);">Loading chart...</div>';
                html += '</div>';
                html += '</div>';
            }

            // Recent Games
            if (data.recent_games && data.recent_games.length > 0) {
                html += '<div class="recent-games">';
                html += '<h2>🎮 Recent Games</h2>';

                data.recent_games.forEach(game => {
                    let resultClass = game.result.toLowerCase();
                    html += '<div class="game-item ' + resultClass + '">';
                    html += '<div class="game-header">';
                    html += '<span class="game-id">Game #' + game.id + '</span>';
                    html += '<span class="game-time">' + game.time + '</span>';
                    html += '</div>';
                    html += '<div class="game-result ' + resultClass + '">' + game.result + '</div>';
                    html += '<div class="game-details">' + game.board_size + 'x' + game.board_size + ' board</div>';
                    html += '</div>';
                });

                html += '</div>';
            }

            tempDiv.innerHTML = html;
            contentDiv.parentNode.replaceChild(tempDiv, contentDiv);
            tempDiv.id = 'content';

            // Fade in the new content
            setTimeout(() => {
                tempDiv.style.opacity = '1';
            }, 10);
        }

        // Auto-refresh every 3 seconds
        setInterval(refreshData, 3000);

        // Initial load
        refreshData();
    </script>
</body>
</html>
'''

def get_db_connection():
    """Get database connection"""
    try:
        conn = sqlite3.connect('data/db/game_records.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def generate_progress_chart():
    """Generate and save the progress chart"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        # Get AI player ID
        cursor.execute('SELECT id FROM players WHERE name = ? AND is_ai = TRUE', ('AILearner',))
        ai_player = cursor.fetchone()
        
        if not ai_player:
            return False
        
        ai_player_id = ai_player['id']
        
        # Get progress data
        cursor.execute('''
            SELECT win_rate, timestamp
            FROM learning_metrics
            WHERE playerid = ?
            ORDER BY timestamp ASC
        ''', (ai_player_id,))
        
        progress_data = cursor.fetchall()
        
        if not progress_data:
            return False
        
        # Generate chart
        converted_timestamps = []
        for row in progress_data:
            timestamp = row['timestamp']
            if timestamp > 1e10:  # If timestamp is in milliseconds
                timestamp /= 1000
            try:
                converted_timestamps.append(datetime.fromtimestamp(timestamp))
            except ValueError:
                converted_timestamps.append(datetime.fromtimestamp(0))  # fallback to epoch if invalid

        win_rates = [row['win_rate'] * 100 for row in progress_data]

        plt.figure(figsize=(12, 6))
        plt.plot(converted_timestamps, win_rates, marker='o', linestyle='-', color='#667eea', linewidth=3, markersize=8)

        # Fill area under the curve
        plt.fill_between(converted_timestamps, win_rates, color='#667eea', alpha=0.2)
        
        # Customize the chart
        plt.title('AI Learning Progress - Win Rate Over Time', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Win Rate (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)
        
        # Add data labels for key points
        for i, (timestamp, win_rate) in enumerate(zip(timestamps, win_rates)):
            if i == 0 or i == len(timestamps) - 1 or i % max(1, len(timestamps)//5) == 0:
                plt.text(timestamp, win_rate + 2, f'{win_rate:.1f}%', 
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Style improvements
        ax = plt.gca()
        ax.set_facecolor('#f8f9fa')  # Use set_facecolor instead of set_face_color
        plt.tight_layout()

        # Save the chart
        os.makedirs('data/charts', exist_ok=True)
        chart_path = 'data/charts/learning_progress.png'
        plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
        plt.close()

        return True

    except Exception as e:
        print(f"Error generating chart: {e}")
        return False

def generate_win_loss_chart():
    """Generate and save the win/loss ratio chart"""
    try:
        conn = get_db_connection()
        if not conn:
            return False

        cursor = conn.cursor()

        # Get AI player ID
        cursor.execute('SELECT id FROM players WHERE name = ? AND is_ai = TRUE', ('AILearner',))
        ai_player = cursor.fetchone()

        if not ai_player:
            print("AILearner player not found in database")
            return False

        ai_player_id = ai_player['id']

        # Get game results ordered by time - use game_results timestamp if game date is not available
        cursor.execute('''
            SELECT gr.timestamp as result_timestamp, gr.result, g.date as game_date
            FROM game_results gr
            JOIN games g ON gr.gameid = g.id
            WHERE gr.playerid = ?
            ORDER BY g.date ASC
        ''', (ai_player_id,))

        game_results = cursor.fetchall()

        if not game_results:
            print(f"No game results found for player ID {ai_player_id}")
            # Try alternative query to see if we have data
            cursor.execute('SELECT COUNT(*) FROM game_results WHERE playerid = ?', (ai_player_id,))
            count = cursor.fetchone()[0]
            print(f"Total game_results for AILearner: {count}")
            return False

        # Process data to calculate cumulative win/loss ratios over time
        timestamps = []
        cumulative_wins = []
        cumulative_losses = []
        cumulative_draws = []
        cumulative_win_ratios = []
        cumulative_loss_ratios = []
        cumulative_draw_ratios = []

        wins = 0
        losses = 0
        draws = 0

        for result_row in game_results:
            # Use game date if available, otherwise fall back to result timestamp
            timestamp = result_row['game_date'] if result_row['game_date'] else result_row['result_timestamp']
            if timestamp > 1e10:  # If timestamp is in milliseconds
                timestamp /= 1000

            if result_row['result'] == 1:  # Win
                wins += 1
            elif result_row['result'] == 2:  # Loss
                losses += 1
            elif result_row['result'] == 3:  # Draw
                draws += 1

            total_games = wins + losses + draws

            if total_games > 0:
                try:
                    timestamps.append(datetime.fromtimestamp(timestamp))
                    cumulative_wins.append(wins)
                    cumulative_losses.append(losses)
                    cumulative_draws.append(draws)
                    cumulative_win_ratios.append((wins / total_games) * 100)
                    cumulative_loss_ratios.append((losses / total_games) * 100)
                    cumulative_draw_ratios.append((draws / total_games) * 100)
                except ValueError as ve:
                    print(f"Error converting timestamp {timestamp}: {ve}")
                    continue

        if not timestamps:
            print("No valid timestamps found for chart")
            return False

        # Create the chart
        plt.figure(figsize=(12, 6))

        # Plot win/loss/draw ratios over time
        plt.plot(timestamps, cumulative_win_ratios, label='Win Rate', marker='o', color='#4CAF50', linewidth=2)
        plt.plot(timestamps, cumulative_loss_ratios, label='Loss Rate', marker='s', color='#F44336', linewidth=2)
        plt.plot(timestamps, cumulative_draw_ratios, label='Draw Rate', marker='^', color='#2196F3', linewidth=2)

        # Customize the chart
        plt.title('AI Learning Progress - Win/Loss/Draw Ratios Over Time', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Rate (%)', fontsize=12)
        plt.legend(loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)

        # Style improvements
        ax = plt.gca()
        ax.set_facecolor('#f8f9fa')  # Use set_facecolor instead of set_face_color
        plt.tight_layout()

        # Save the chart
        os.makedirs('data/charts', exist_ok=True)
        chart_path = 'data/charts/win_loss_ratio.png'
        plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
        plt.close()

        print(f"Successfully generated win/loss chart with {len(timestamps)} data points")
        return True

    except Exception as e:
        print(f"Error generating win/loss chart: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    """API endpoint to get learning statistics"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get AI player ID (using new schema with is_ai column)
        cursor.execute('SELECT id FROM players WHERE name = ? AND is_ai = TRUE', ('AILearner',))
        ai_player = cursor.fetchone()
        
        if not ai_player:
            # If no AI player found, check if any player exists (might need to initialize)
            cursor.execute('SELECT COUNT(*) FROM players')
            player_count = cursor.fetchone()[0]
            
            if player_count == 0:
                return jsonify({'error': 'No games played yet. Start the learning system to begin training!'}), 404
            else:
                return jsonify({'error': 'AI player not found. Start training first.'}), 404
        
        ai_player_id = ai_player['id']
        
        # Get overall statistics
        cursor.execute('SELECT COUNT(*) FROM game_results WHERE playerid = ?', (ai_player_id,))
        total_games = cursor.fetchone()[0]
        
        if total_games == 0:
            return jsonify({'error': 'No games played yet. Start training to see statistics.'}), 404
        
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
        
        # Check if progress data exists
        cursor.execute('SELECT COUNT(*) FROM learning_metrics WHERE playerid = ?', (ai_player_id,))
        has_progress_data = cursor.fetchone()[0] > 0

        # Check if win/loss data exists
        cursor.execute('SELECT COUNT(*) FROM game_results WHERE playerid = ?', (ai_player_id,))
        has_win_loss_data = cursor.fetchone()[0] > 0

        # Get recent games
        cursor.execute('''
            SELECT g.id, g.date, g.board_size, gr.result
            FROM games g
            JOIN game_results gr ON g.id = gr.gameid
            WHERE gr.playerid = ?
            ORDER BY g.date DESC
            LIMIT 10
        ''', (ai_player_id,))

        recent_games = []
        result_map = {1: 'Win', 2: 'Loss', 3: 'Draw'}

        for game in cursor.fetchall():
            # Handle timestamp conversion - it might be in milliseconds
            timestamp = game['date']
            if timestamp > 1e10:  # If timestamp is in milliseconds
                timestamp /= 1000
            try:
                time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
            except ValueError:
                time_str = 'Invalid timestamp'

            recent_games.append({
                'id': game['id'],
                'time': time_str,
                'result': result_map.get(game['result'], 'Unknown'),
                'board_size': game['board_size']
            })

        conn.close()

        return jsonify({
            'total_games': total_games,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': win_rate,
            'loss_rate': loss_rate,
            'draw_rate': draw_rate,
            'has_progress_data': has_progress_data,
            'has_win_loss_data': has_win_loss_data,
            'recent_games': recent_games
        })
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to retrieve statistics'}), 500

@app.route('/chart')
def get_chart():
    """API endpoint to get the progress chart"""
    try:
        # Generate fresh chart
        if generate_progress_chart():
            return send_from_directory('data/charts', 'learning_progress.png', mimetype='image/png')
        else:
            # Return a placeholder if no data
            return send_from_directory('data/charts', 'learning_progress.png', mimetype='image/png')
    except Exception as e:
        print(f"Error serving chart: {e}")
        return "Chart not available", 404

@app.route('/win-loss-chart')
def get_win_loss_chart():
    """API endpoint to get the win/loss ratio chart"""
    try:
        # Generate fresh chart
        success = generate_win_loss_chart()
        if success:
            # Check if file exists before sending
            chart_path = os.path.join('data/charts', 'win_loss_ratio.png')
            if os.path.exists(chart_path):
                return send_from_directory('data/charts', 'win_loss_ratio.png', mimetype='image/png')
            else:
                # Create a simple placeholder chart if file doesn't exist
                create_placeholder_chart('data/charts/win_loss_ratio.png', 'No data available for win/loss chart')
                return send_from_directory('data/charts', 'win_loss_ratio.png', mimetype='image/png')
        else:
            # Create a simple placeholder chart if no data
            create_placeholder_chart('data/charts/win_loss_ratio.png', 'No data available for win/loss chart')
            return send_from_directory('data/charts', 'win_loss_ratio.png', mimetype='image/png')
    except Exception as e:
        print(f"Error serving win/loss chart: {e}")
        # Create a simple placeholder chart for errors
        create_placeholder_chart('data/charts/win_loss_ratio.png', 'Error generating win/loss chart')
        return send_from_directory('data/charts', 'win_loss_ratio.png', mimetype='image/png')

def create_placeholder_chart(filepath, message):
    """Create a simple placeholder chart image"""
    try:
        import matplotlib.pyplot as plt
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np

        # Create a simple image with the message
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, message, horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=14)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    except:
        # If matplotlib fails, create a basic file
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write('placeholder')

def start_dashboard():
    """Start the dashboard server"""
    print("📊 Starting AI-Gamer Learning Dashboard...")
    print("🌐 Dashboard will be available at: http://localhost:5000")
    print("📈 Press Ctrl+C to stop the dashboard")
    print("=" * 50)
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Make sure data directories exist
    os.makedirs('data/db', exist_ok=True)
    os.makedirs('data/charts', exist_ok=True)
    
    # Start the dashboard
    start_dashboard()