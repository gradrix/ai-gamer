# AGENTS.md - AI-Gamer Agents Guide

Inspired by workspace AGENTS.md, this is a continuity file for the ai-gamer project. Read it on startup for context.

## Project Essence
Train AI agents to master Tic-Tac-Toe (and potentially more) using reinforcement learning (DQN). Focus: Self-improvement via games against random opponents, logging progress, visualizing learning.

## Intended Use
- **Training:** Run loops of games to build experience replay, update Q-network.
- **Evaluation:** Stats on win rates, epsilon decay, convergence.
- **Extension:** Add games, better RL algos, multi-agent play.

## Setup & Dependencies
- Python 3.11 + TF 2.20, gRPC, Flask, etc. (install_reqs.sh)
- Docker for isolated runs (volumes for data/db).
- Env vars: PLAYER_NAME, LEARNING_MODE, *_LOOP_DELAY.

## Key Scripts
- Runners: run_learning_system.sh (train), run_dashboard.sh (viz), run_tests.sh.
- Monitors: show_learning_stats.sh, track_ai_progress.py.
- Stoppers: stop_learning_system.sh.

## Agents Breakdown
- **AI Agent (ai_agent/):** DQN core—gamerunner.py polls server, controller.py handles TD learning, modelmanager.py manages buffer/target/epsilon.
- **Random Client:** Simple random-move bot for training fodder.
- **Console Client:** Human interface.

## Database & Data
- SQLite: Tracks players, games, moves, results, metrics.
- Models saved in data/models/.

## Known Fixes/Improvements
- DQN: TD targets, unbatched states, 10k buffer, 0.995 epsilon start.
- DB: WAL mode, DELETE PRAGMA for perf.
- Potential: Fix 'ticktaktoe' typos, boost win rates (aim >90% optimal), add convergence tests.

## Dev Workflow
1. ./run_learning_system.sh
2. Monitor with show_learning_stats.sh
3. Viz at localhost:5000 (run_dashboard.sh)
4. Test: ./run_tests.sh
5. Analyze: track_ai_progress.py

Update this as the project evolves—it's your project's 'soul'.
