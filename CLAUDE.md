# CLAUDE.md

## Project Layout
```
ai-gamer/
├── ai_agent/
│   ├── gamerunner.py
│   ├── network/
│   │   ├── controller.py (DQN TD fixes)
│   │   ├── modelmanager.py (buffer/target/ε fixes)
│   │   └── neuralnetwork.py (legacy CNN)
├── common/
│   ├── models/
│   ├── rpc/
│   └── timehelpers.py
├── console_client/
├── dashboard_server.py (Flask viz)
├── game_server/
│   ├── games/ticktaktoe.py
│   ├── gameserver.py
│   └── state/
│       ├── gamestatemanager.py
│       ├── recorderdb.py (DB logger/PRAGMA)
│       └── game_records_schema.sql
├── random_client/
├── run_*.sh (dockers --user volume)
├── tests/
│   └── test_dqn_fixes.py (padding/state)
├── data/
│   ├── db/ (ai-gamer-db volume)
│   ├── models/
│   └── charts/
├── show_player_stats.sh
├── show_learning_stats.sh
└── track_ai_progress.py
```

## tests/ layout
- test_dqn_fixes.py (model/predict/state shape)
- test_system_integration.py (dockers)
- test_ai_convergence.py (pending)

## Dev Workflow
```
./run_learning_system.sh  # server/random/AI train
./stop_learning_system.sh
./show_learning_stats.sh  # win%
./run_dashboard.sh  # viz
./run_tests.sh  # pytest docker
```

## Environment Variables
| Name | Description | Default |
|------|-------------|---------|
| PLAYER_NAME | AI/Random name | AILearner/RandomBot |
| LEARNING_MODE | Train? | true |
| AGENT_LOOP_DELAY | Poll s | 0.0 |
| CLIENT_LOOP_DELAY | Poll s | 0.0 |

## Stack
- Python 3.11
- TensorFlow 2.20 GPU Keras
- gRPC protobuf
- SQLite WAL/PRAGMA
- Flask dashboard
- Docker --user volume ai-gamer-db
- pytest

## Database Schema
Tables: players (id, name, createddate, lastonline, is_ai, UNIQUE name)
games (id, date, status, board_size, winner_id)
moves (gameid, playerid, idx, move, date, q_value)
game_results (gameid, playerid, result 1win/2loss/3draw, timestamp)
learning_metrics (playerid, timestamp, win_rate...)
training_sessions (playerid, start/end_time, episodes, ε...)

## Fixes
- DQN: TD pending s,a,r,s' (no smear/duplicates)
- State unbatched (10,10)
- Buffer 10k, ε0.995 decay, target%1000
- DB volume chown uid1000, PRAGMA DELETE checkpoint
- Dockers --user timing

**Win rate AILearner 45-60% vs random post-train.**
