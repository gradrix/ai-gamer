import unittest
import subprocess
import time
import os
import re # For regex matching in logs

# Configuration (adjust these as per actual script paths and container names)
GAME_SERVER_DOCKER_IMAGE = "your_game_server_image_name" # Replace with actual image name
AI_AGENT_SCRIPT_PATH = "./run_ai_agent.sh" # Relative to project root
TEST_AGENT_NAME = "TestInitAgent"
MODEL_DIR = "ai_agent/data/models/" # Relative to project root
TEST_AGENT_MODEL_FILE = os.path.join(MODEL_DIR, TEST_AGENT_NAME + ".keras")
LOG_CHECK_TIMEOUT_SECONDS = 60 # How long to wait for log messages
LOG_POLL_INTERVAL_SECONDS = 1

# Expected log message regex (adjust if actual log message differs)
# Example: "Controller TestInitAgent: Network components initialized. Board: 3x3x1, Actions: 9"
EXPECTED_INIT_LOG_REGEX = r"Controller {}: Network components initialized. Board: (\d+)x(\d+)x(\d+), Actions: (\d+)".format(TEST_AGENT_NAME)
EXPECTED_BOARD_DIMS = (3, 3, 1) # H, W, C
EXPECTED_ACTIONS = 9


class TestAgentInitialization(unittest.TestCase):

    game_server_process = None
    ai_agent_process = None

    def _start_game_server(self):
        # Command to start the game server in Docker
        # This is highly dependent on how the server is containerized and run.
        # For example:
        # cmd = ["docker", "run", "--rm", "-p", "50051:50051", GAME_SERVER_DOCKER_IMAGE]
        # This assumes the server image is built and named GAME_SERVER_DOCKER_IMAGE
        # and it exposes port 50051, and that the AI agent connects to localhost:50051
        # **This part needs to be adapted by the user to their specific server run command.**
        # For now, we'll use a placeholder and print a message.
        print(f"Placeholder: Would start game server Docker image {GAME_SERVER_DOCKER_IMAGE}")
        # self.game_server_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # time.sleep(5) # Give server time to start
        return True # Placeholder

    def _stop_game_server(self):
        if self.game_server_process:
            # cmd = ["docker", "stop", self.game_server_process.pid] # This is incorrect for docker run
            # Instead, if 'docker run' was used, one would typically stop by container name/ID.
            # For simplicity with Popen, sending terminate/kill if it was a direct process.
            # If using 'docker run', the teardown needs to manage the container.
            print(f"Placeholder: Would stop game server (if managed by Popen or specific docker stop command)")
            # self.game_server_process.terminate()
            # self.game_server_process.wait(timeout=10)
        return True # Placeholder

    def _start_ai_agent(self):
        env = os.environ.copy()
        env["AGENT_NAME"] = TEST_AGENT_NAME
        # Add other env vars if needed, e.g., AI_SERVER_HOST, AI_SERVER_PORT
        # Assuming run_ai_agent.sh uses these.
        try:
            self.ai_agent_process = subprocess.Popen(
                [AI_AGENT_SCRIPT_PATH],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except FileNotFoundError:
            self.fail(f"AI Agent script not found at {AI_AGENT_SCRIPT_PATH}. Ensure path is correct from project root.")
        time.sleep(5) # Give agent time to start

    def _stop_ai_agent(self):
        if self.ai_agent_process:
            self.ai_agent_process.terminate()
            try:
                self.ai_agent_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.ai_agent_process.kill()
                self.ai_agent_process.wait(timeout=10)

    def setUp(self):
        # Remove old model file if it exists
        # Construct path relative to this script's directory if MODEL_DIR is not absolute
        # For simplicity, assuming MODEL_DIR is relative to project root where test is run
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR, exist_ok=True) # Ensure model directory exists
            
        if os.path.exists(TEST_AGENT_MODEL_FILE):
            os.remove(TEST_AGENT_MODEL_FILE)

        # Start server
        if not self._start_game_server():
            self.fail("Failed to start game server (placeholder - adapt command)")
        
        # Start AI agent
        self._start_ai_agent()

    def tearDown(self):
        self._stop_ai_agent()
        self._stop_game_server()
        # Clean up model file again, just in case
        if os.path.exists(TEST_AGENT_MODEL_FILE):
            #os.remove(TEST_AGENT_MODEL_FILE) # Keep it for inspection for now
            pass


    def test_agent_initializes_and_logs_dimensions(self):
        self.assertIsNotNone(self.ai_agent_process, "AI Agent process should be started.")
        
        start_time = time.time()
        log_found = False
        
        # Give the agent a bit more time to connect and log, especially if server startup is slow
        time.sleep(5) 

        while time.time() - start_time < LOG_CHECK_TIMEOUT_SECONDS:
            line = ""
            try:
                # Non-blocking read (or very short timeout) would be ideal here,
                # but Popen.stdout.readline() can block.
                # If self.ai_agent_process.stdout is a stream, this will read one line.
                # For non-blocking, one might use select or threads, but for a test script,
                # polling like this is often simpler if performance is not critical.
                line = self.ai_agent_process.stdout.readline()
            except Exception as e: # Catch potential errors during readline, e.g. if pipe closes unexpectedly
                print(f"Error reading agent stdout: {e}")

            if not line and self.ai_agent_process.poll() is not None: # Process ended
                print("AI Agent process ended.")
                break 
            
            if line:
                print(f"Agent Log: {line.strip()}") # For debugging the test
                match = re.search(EXPECTED_INIT_LOG_REGEX, line)
                if match:
                    board_h, board_w, channels, actions = map(int, match.groups())
                    self.assertEqual((board_h, board_w, channels), EXPECTED_BOARD_DIMS)
                    self.assertEqual(actions, EXPECTED_ACTIONS)
                    log_found = True
                    break
            else: # No line read, process still running
                time.sleep(LOG_POLL_INTERVAL_SECONDS)


        if not log_found:
            print("Expected log not found. Dumping remaining logs...")
            # Attempt to communicate to get remaining logs, with a timeout
            try:
                stdout, stderr = self.ai_agent_process.communicate(timeout=5)
                print("AI Agent stdout:\n", stdout)
                print("AI Agent stderr:\n", stderr)
            except subprocess.TimeoutExpired:
                print("Timeout expired while trying to get remaining logs from AI agent.")
            except Exception as e:
                print(f"Error during final communicate: {e}")

            self.fail(f"Expected initialization log not found for agent {TEST_AGENT_NAME} within {LOG_CHECK_TIMEOUT_SECONDS}s. Regex: '{EXPECTED_INIT_LOG_REGEX}'")

if __name__ == '__main__':
    # Important: The user needs to provide the actual command to run their game server.
    # For now, this test will run with placeholder server logic.
    print("Reminder: Game server start/stop logic is a placeholder.")
    print(f"Ensure '{GAME_SERVER_DOCKER_IMAGE}' is the correct game server Docker image name.")
    print(f"Ensure '{AI_AGENT_SCRIPT_PATH}' points to the AI agent start script from project root.")
    print(f"Ensure '{MODEL_DIR}' exists or can be created, and is writable.")
    print("The test assumes a 3x3 Tic-Tac-Toe game by default from the server, resulting in these expected values:")
    print(f"  EXPECTED_INIT_LOG_REGEX: r\"{EXPECTED_INIT_LOG_REGEX}\"")
    print(f"  EXPECTED_BOARD_DIMS: {EXPECTED_BOARD_DIMS}")
    print(f"  EXPECTED_ACTIONS: {EXPECTED_ACTIONS}")
    
    unittest.main()
```
