# AI-Gamer Learning System

## 🎮 Overview

The AI-Gamer Learning System is a comprehensive platform for training and monitoring AI agents that learn to play board games. The system includes:

- **Game Server** - gRPC-based server for hosting games
- **Random Client** - Baseline opponent for AI training
- **AI Agent** - Deep Q-Network agent that learns through reinforcement learning
- **Monitoring System** - Real-time tracking of learning progress
- **Web Dashboard** - Visualization of performance metrics

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI-Gamer Learning System                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────┐  │
│  │      Game Server    │    │    Random Client    │    │     AI Agent    │  │
│  │  ┌───────────────┐  │    │  ┌───────────────┐  │    │  ┌───────────┐  │  │
│  │  │ gRPC Server   │  │    │  │ Brute Force   │  │    │  │ DQN Agent │  │  │
│  │  └───────────────┘  │    │  │ Move Selection│  │    │  │ Neural    │  │  │
│  │  ┌───────────────┐  │    │  └───────────────┘  │    │  │ Network  │  │  │
│  │  │ Game Logic    │  │    │  ┌───────────────┐  │    │  │ Q-Learning│  │  │
│  │  └───────────────┘  │    │  │ gRPC Client   │  │    │  └───────────┘  │  │
│  └─────────────────────┘    │  └───────────────┘  │    └─────────────────┘  │  │
│          ▲                        ▲                        ▲                  │  │
│          │                        │                        │                  │  │
│  ┌───────┴────────────────────────┴────────────────────────┴──────────────┐  │  │
│  │                          gRPC Communication                              │  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │  │
│                                                                             │  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │  │
│  │                          SQLite Database                               │  │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │  │
│  │  │  Players    │  │   Games     │  │  Moves      │  │ Game Results│  │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │  │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │  │  │
│  │  │Learning     │  │Training     │  │Game Results │                  │  │  │
│  │  │Metrics      │  │Sessions     │  │             │                  │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                  │  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │  │
│                                                                             │  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │  │
│  │                        Monitoring System                               │  │  │
│  │  ┌─────────────────┐  ┌─────────────────────────────────────────────┐  │  │  │
│  │  │ CLI Monitor     │  │ Web Dashboard                        │  │  │  │
│  │  │  ┌─────────────┐ │  │  ┌─────────────────────────────────┐  │  │  │  │
│  │  │  │ Real-time    │ │  │  │ Flask Web Server                │  │  │  │  │
│  │  │  │ Updates      │ │  │  │ Matplotlib Charts               │  │  │  │  │
│  │  │  │ Statistics   │ │  │  │ Interactive UI                 │  │  │  │  │
│  │  │  └─────────────┘ │  │  └─────────────────────────────────┘  │  │  │  │
│  │  └─────────────────┘  └─────────────────────────────────────────────┘  │  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │  │
│                                                                             │  │
└─────────────────────────────────────────────────────────────────────────────┘  │  │
                                                                                 │  │
┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│                            User Interface                                    │  │  │
├─────────────────────────────────────────────────────────────────────────────┤  │  │
│                                                                             │  │  │
│  • Shell Scripts: run_learning_system.sh, monitor_learning.sh, etc.         │  │  │
│  • Web Dashboard: http://localhost:5000                                      │  │  │
│  • Statistics: show_learning_stats.sh                                        │  │  │
│                                                                             │  │  │
└─────────────────────────────────────────────────────────────────────────────┘  │  │
                                                                                 │  │
┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│                            Data Storage                                      │  │  │
├─────────────────────────────────────────────────────────────────────────────┤  │  │
│                                                                             │  │  │
│  • data/db/game_records.db - SQLite database with all game data              │  │  │
│  • data/models/ - Trained neural network models                              │  │  │
│  • data/charts/ - Generated progress charts                                  │  │  │
│                                                                             │  │  │
└─────────────────────────────────────────────────────────────────────────────┘  │  │
                                                                                 │  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Docker installed and running
- Python 3.11+ (for local development)
- Basic understanding of command line

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/your-repo/ai-gamer.git
   cd ai-gamer
   ```

2. **Make scripts executable**:
   ```bash
   chmod +x run_*.sh monitor_learning.sh show_learning_stats.sh stop_learning_system.sh
   ```

3. **Install Python dependencies** (for local testing):
   ```bash
   pip install sqlite3 matplotlib flask
   ```

## 🎯 Running the System

### Start the Complete Learning System

```bash
./run_learning_system.sh
```

This script will:
1. Start the Game Server in Docker
2. Start the Random Client in Docker  
3. Start the AI Agent in Docker
4. Launch the monitoring system
5. Show real-time logs

### Access the Web Dashboard

```bash
./run_dashboard.sh
```

Then open your browser to: `http://localhost:5000`

The dashboard shows:
- Real-time win/loss/draw statistics
- Learning progress charts
- Recent game history
- Performance metrics

### Monitor Learning Progress

```bash
./monitor_learning.sh
```

This provides a real-time CLI monitor that updates every 10 seconds showing:
- Total games played
- Current win rate
- Loss and draw rates
- Training session progress

### View Detailed Statistics

```bash
./show_learning_stats.sh
```

This shows comprehensive statistics including:
- Overall performance metrics
- Learning progress over time
- Training session history
- Recent game details
- Performance recommendations

### Stop the System

```bash
./stop_learning_system.sh
```

This gracefully shuts down all components and shows final statistics.

## 📊 Monitoring and Analysis

### Real-time Monitoring

The system provides multiple ways to monitor AI learning progress:

1. **Web Dashboard** (`http://localhost:5000`)
   - Beautiful visual interface
   - Auto-refreshing data
   - Progress charts
   - Game history

2. **CLI Monitor** (`./monitor_learning.sh`)
   - Real-time text updates
   - Quick performance overview
   - Training session tracking

3. **Statistics Viewer** (`./show_learning_stats.sh`)
   - Detailed analysis
   - Historical data
   - Performance trends

### Database Schema

The enhanced database schema tracks:

**Players Table**
- `id`, `name`, `createddate`, `lastonline`, `is_ai`

**Games Table**
- `id`, `date`, `status`, `board_size`, `game_type`, `winner_id`

**Moves Table**
- `id`, `gameid`, `playerid`, `idx`, `move`, `date`, `q_value`

**Game Results Table**
- `id`, `gameid`, `playerid`, `result`, `timestamp`

**Learning Metrics Table**
- `id`, `playerid`, `timestamp`, `win_rate`, `loss_rate`, `draw_rate`, `average_q_value`, `games_played`

**Training Sessions Table**
- `id`, `playerid`, `start_time`, `end_time`, `initial_win_rate`, `final_win_rate`, `episodes`, `epsilon_start`, `epsilon_end`

### Performance Metrics

The system tracks these key metrics:

- **Win Rate**: Percentage of games won
- **Loss Rate**: Percentage of games lost  
- **Draw Rate**: Percentage of games drawn
- **Win/Loss Ratio**: Wins divided by losses
- **Q-Values**: Quality estimates for moves
- **Games Played**: Total number of games
- **Training Episodes**: Number of learning iterations

## 🤖 AI Learning Process

### How the AI Learns

1. **Initialization**: AI starts with random moves (high epsilon)
2. **Exploration**: AI tries different moves to learn the game
3. **Exploitation**: AI uses learned knowledge to make better moves
4. **Experience Replay**: AI learns from past games
5. **Q-Value Updates**: AI improves move quality estimates
6. **Epsilon Decay**: AI gradually relies more on learned knowledge

### Learning Phases

- **Phase 1 (0-100 games)**: Random exploration, learning basics
- **Phase 2 (100-500 games)**: Pattern recognition, strategy development
- **Phase 3 (500+ games)**: Refinement, optimization, mastery

### Expected Progress

- **0-50 games**: ~10-30% win rate (mostly random)
- **50-200 games**: ~30-60% win rate (learning patterns)
- **200-500 games**: ~60-80% win rate (strategy development)
- **500+ games**: ~80-95% win rate (mastery level)

## 🔧 Configuration

### Environment Variables

You can customize the system using environment variables:

**AI Agent**:
- `PLAYER_NAME`: Name of the AI player (default: "AILearner")
- `LEARNING_MODE`: Enable/disable learning (default: "true")
- `BOARD_SIZE`: Game board size (default: 3)

**Random Client**:
- `PLAYER_NAME`: Name of the random player (default: "RandomBot")

**Dashboard**:
- `DASHBOARD_PORT`: Port for web dashboard (default: 5000)

### Customizing Game Parameters

Edit these files to customize game behavior:

- `ai_agent/network/modelmanager.py`: Learning parameters
- `game_server/games/ticktaktoe.py`: Game rules
- `common/models/enums.py`: Game constants

## 📈 Advanced Features

### TensorBoard Integration (Future)

For advanced neural network visualization:
```bash
# tensorboard --logdir=data/models
```

### Multi-Game Support (Future)

The system is designed to support multiple games:
- Tic-Tac-Toe (current)
- Chess (planned)
- Connect Four (planned)
- Gomoku (planned)

### Performance Optimization

For better performance:
- Increase `batch_size` in modelmanager.py
- Adjust `learning_rate` for faster/smoother learning
- Modify `epsilon_decay` for exploration/exploitation balance

## 🛠️ Troubleshooting

### Common Issues

**Database connection errors**:
- Make sure `data/db` directory exists
- Check file permissions
- Verify Docker volume mounting

**Docker build failures**:
- Check Docker is running
- Ensure enough disk space
- Clean Docker cache: `docker system prune`

**Monitoring script errors**:
- Run with Python 3.11+
- Install required dependencies
- Check database schema version

### Debugging Tips

1. **Check logs**:
   ```bash
   docker logs game_server
   docker logs ai_agent
   docker logs random_client
   ```

2. **Test database connection**:
   ```bash
   sqlite3 data/db/game_records.db "SELECT * FROM players;"
   ```

3. **Verify network connectivity**:
   ```bash
   docker network inspect bridge
   ```

## 📚 Technical Details

### Reinforcement Learning

- **Algorithm**: Deep Q-Network (DQN)
- **Exploration**: Epsilon-greedy policy
- **Experience Replay**: Memory buffer for stable learning
- **Target Network**: Separate network for stable Q-value estimation

### Neural Network Architecture

- **Input**: Board state + possible moves
- **Hidden Layers**: 2 dense layers (128, 64 units)
- **Output**: Q-values for each possible move
- **Activation**: ReLU for hidden layers, Linear for output
- **Optimizer**: Adam
- **Loss Function**: Mean Squared Error

### Reward System

- **Win**: +1.0 reward
- **Draw**: +0.5 reward
- **Loss**: -1.0 reward
- **Invalid Move**: -10.0 reward
- **Regular Move**: 0.0 reward

## 🎓 Learning Resources

### Reinforcement Learning
- [Deep Q-Network (DQN) Paper](https://www.nature.com/articles/nature14236)
- [OpenAI Spinning Up](https://spinningup.openai.com/)

### Game AI
- [AlphaGo Paper](https://www.nature.com/articles/nature16961)
- [Chess Programming Wiki](https://www.chessprogramming.org/)

### Python & AI
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Keras Documentation](https://keras.io/)

## 📋 Roadmap

### Completed ✅
- [x] Fix reward system (was completely inverted)
- [x] Implement proper DQN with experience replay
- [x] Add target network for stable learning
- [x] Enhance database schema for learning metrics
- [x] Create comprehensive monitoring system
- [x] Build web dashboard with visualization
- [x] Implement Docker containerization
- [x] Add real-time progress tracking

### In Progress 🚧
- [ ] Multi-game support (chess, connect four)
- [ ] TensorBoard integration
- [ ] Advanced opponent strategies
- [ ] Hyperparameter optimization


## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Commit changes**: `git commit -m 'Add some feature'`
4. **Push to branch**: `git push origin feature/your-feature`
5. **Open a pull request**

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_learning.py
```

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgments

- Thanks to all contributors
- Inspired by reinforcement learning research
- Built with Python, TensorFlow, and Docker
