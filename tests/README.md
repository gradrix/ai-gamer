# AI Agent Tests

This directory contains tests for the AI agent.

## Unit Tests

(User can fill this section if they have existing unit test documentation)
Existing unit tests can be found in this directory. [User to specify how to run them, e.g., `python -m unittest discover tests`]

## Integration Tests

These tests verify the AI agent's interaction with the game server and its core functionalities like dynamic initialization and learning.

### Dependencies

*   **Docker:** Required to run the game server, AI agent, and random client in containerized environments. Ensure Docker is installed and the user has permissions to run Docker commands.
*   **Python:** Python 3.x with the `unittest` module (standard library).
*   **Project Scripts:**
    *   `run_ai_agent.sh`: Script to run the AI agent (presumably in Docker).
    *   `run_random_client.sh`: Script to run the random client (presumably in Docker).
    *   A script or Docker command to run the game server.

### Configuration

Before running the integration tests, you **must** configure them according to your local environment:

1.  **Open `tests/it_test_agent_initialization.py` and `tests/it_test_agent_learning_signals.py`:**
2.  **Update Docker Image Names and Script Paths:**
    *   Set `GAME_SERVER_DOCKER_IMAGE` to your actual game server Docker image name.
    *   Ensure `AI_AGENT_SCRIPT_PATH` correctly points to your `./run_ai_agent.sh` (relative to the project root).
    *   Ensure `RANDOM_CLIENT_SCRIPT_PATH` (in `it_test_agent_learning_signals.py`) correctly points to your `./run_random_client.sh` (relative to the project root).
3.  **Adapt Server/Client Start/Stop Logic:**
    *   In both test files, the methods `_start_game_server()`, `_stop_game_server()`, `_start_random_client()` (in the learning test), and potentially parts of `_start_ai_agent()` contain placeholder comments like "**User must adapt this command**".
    *   You need to replace these placeholders with the actual Docker commands or script invocations required to start and stop your game server and random client. This includes specifying correct ports, network configurations, container names for stopping, etc.
    *   For example, if your game server is run with `docker run -d --name test_server -p 50051:50051 my/game-server-image`, then `_start_game_server` should execute this, and `_stop_game_server` should execute `docker stop test_server && docker rm test_server`.

4.  **Agent Naming and Model Paths:**
    *   The tests use specific agent names (`TestInitAgent`, `TestLearnAgent`) and expect model files to be at `ai_agent/data/models/<agent_name>.keras`. Ensure these paths are consistent with your project structure. The `MODEL_DIR` variable in the tests can be adjusted if needed.

5.  **Game Configuration:**
    *   The `it_test_agent_initialization.py` test currently expects the game server to provide a 3x3 Tic-Tac-Toe game by default, as it asserts specific board dimensions (`EXPECTED_BOARD_DIMS = (3, 3, 1)`) and action counts (`EXPECTED_ACTIONS = 9`).
    *   If your default game server configuration is different, you must adjust these `EXPECTED_` constants in `it_test_agent_initialization.py` or ensure your server is configured for a 3x3 game when tests are run.

6.  **Shell Script Parameterization (Recommended):**
    *   The test scripts attempt to pass the agent name to `run_ai_agent.sh` using an environment variable (e.g., `AGENT_NAME="TestAgent"`).
    *   It's recommended that your `run_ai_agent.sh` (or the underlying Docker entrypoint it calls) reads the `AGENT_NAME` environment variable to set the agent's name. If your script uses a different mechanism, you may need to adapt the test scripts' `_start_ai_agent` method.
    *   Similarly, for parameters like the game server's host and port, the AI agent and random client should ideally read these from environment variables (e.g., `AI_SERVER_HOST`, `AI_SERVER_PORT`). The test scripts can be easily modified to pass these if needed. If your scripts hardcode these values or use a different configuration method, ensure they align with your test environment setup (e.g., server running on `localhost:50051`).

### Running the Tests

Once configured, run the tests from the project's root directory:

To run a specific test file:
```bash
python -m unittest tests.it_test_agent_initialization
python -m unittest tests.it_test_agent_learning_signals
```

To run all tests in the `tests` directory (if structured for discovery):
```bash
python -m unittest discover tests
```

### Interpreting Results

*   **`it_test_agent_initialization`**: Checks if the AI agent starts, connects to the server, and correctly logs the initialization of its neural network with the expected game dimensions.
*   **`it_test_agent_learning_signals`**: Checks if the AI agent, when playing against a random client, logs events indicating it's processing game outcomes (wins, losses, moves) and, crucially, that its model file is being updated (timestamp changes), which signals that the learning and saving mechanisms are active.

If tests fail, check the console output for error messages and the logs from the AI agent (which are printed by the test scripts during execution). Ensure all Docker containers started correctly and were able to communicate.
```
