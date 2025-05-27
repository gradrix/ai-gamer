import unittest
import subprocess
import time
import os
import re

# Configuration (adjust as per actual script paths and container names)
GAME_SERVER_DOCKER_IMAGE = "your_game_server_image_name" # Replace
AI_AGENT_SCRIPT_PATH = "./run_ai_agent.sh" # Relative to project root
RANDOM_CLIENT_SCRIPT_PATH = "./run_random_client.sh" # Relative to project root
TEST_AGENT_NAME = "TestLearnAgent"
MODEL_DIR = "ai_agent/data/models/" # Relative to project root
TEST_AGENT_MODEL_FILE = os.path.join(MODEL_DIR, TEST_AGENT_NAME + ".keras")

LOG_CHECK_TIMEOUT_SECONDS = 90 # How long to run the scenario
LOG_POLL_INTERVAL_SECONDS = 1
MIN_GAMES_FOR_LOG_CHECK = 1 # Minimum game outcome logs to expect

# Expected log message regexes for learning events (adapt if actual messages differ)
# Example: "Controller TestLearnAgent: Learning from winning game."
EXPECTED_LEARNING_EVENT_REGEXES = [
    r"Controller {}: Learning from winning game".format(TEST_AGENT_NAME),
    r"Controller {}: Learning from losing game".format(TEST_AGENT_NAME),
    r"Controller {}: Learning from draw game".format(TEST_AGENT_NAME),
    r"Controller {}: Learning from successful move".format(TEST_AGENT_NAME),
    r"Controller {}: Learning from incorrect move".format(TEST_AGENT_NAME)
]
# Example: "GameRunner TestLearnAgent: Saving model."
EXPECTED_MODEL_SAVE_LOG_REGEX = r"GameRunner {}: Saving model".format(TEST_AGENT_NAME)


class TestAgentLearningSignals(unittest.TestCase):

    game_server_process = None
    ai_agent_process = None
    random_client_process = None
    initial_model_file_mtime = None

    def _start_game_server(self):
        # **User must adapt this command**
        # Example:
        # cmd = ["docker", "run", "--rm", "-p", "50051:50051", GAME_SERVER_DOCKER_IMAGE]
        # self.game_server_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # time.sleep(5) # Give server time to start
        print(f"Placeholder: Would start game server Docker image {GAME_SERVER_DOCKER_IMAGE}")
        return True # Placeholder

    def _stop_game_server(self):
        # **User must adapt this command**
        # Example:
        # if self.game_server_process:
        #    self.game_server_process.terminate() # Or specific docker stop command
        #    self.game_server_process.wait(timeout=10)
        print(f"Placeholder: Would stop game server")
        return True # Placeholder

    def _start_ai_agent(self):
        env = os.environ.copy()
        env["AGENT_NAME"] = TEST_AGENT_NAME
        # Ensure MODEL_DIR exists for the agent to write to
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR, exist_ok=True)
        try:
            self.ai_agent_process = subprocess.Popen(
                [AI_AGENT_SCRIPT_PATH], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
        except FileNotFoundError:
            self.fail(f"AI Agent script not found at {AI_AGENT_SCRIPT_PATH}.")
        time.sleep(5) # Give agent time to start and initialize

    def _stop_ai_agent(self):
        if self.ai_agent_process:
            self.ai_agent_process.terminate()
            try: self.ai_agent_process.wait(timeout=10)
            except subprocess.TimeoutExpired: self.ai_agent_process.kill()

    def _start_random_client(self):
        # Add environment variables if run_random_client.sh needs them (e.g., server address)
        env = os.environ.copy()
        # Example if random client needs agent name to play against (though typically it plays any)
        # env["OPPONENT_AGENT_NAME"] = TEST_AGENT_NAME 
        try:
            self.random_client_process = subprocess.Popen(
                [RANDOM_CLIENT_SCRIPT_PATH], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
        except FileNotFoundError:
            self.fail(f"Random client script not found at {RANDOM_CLIENT_SCRIPT_PATH}.")
        time.sleep(2) # Give client time to start

    def _stop_random_client(self):
        if self.random_client_process:
            self.random_client_process.terminate()
            try: self.random_client_process.wait(timeout=10)
            except subprocess.TimeoutExpired: self.random_client_process.kill()

    def setUp(self):
        # Ensure model directory exists before attempting to remove file or get mtime
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR, exist_ok=True)

        if os.path.exists(TEST_AGENT_MODEL_FILE):
            os.remove(TEST_AGENT_MODEL_FILE)
        
        # Store mtime of non-existent file or 0 if it truly doesn't exist after attempt to remove
        try:
            self.initial_model_file_mtime = os.path.getmtime(TEST_AGENT_MODEL_FILE)
        except OSError: # Handles FileNotFoundError
            self.initial_model_file_mtime = 0

        if not self._start_game_server():
            self.fail("Failed to start game server (placeholder - adapt command)")
        self._start_ai_agent()
        self._start_random_client()

    def tearDown(self):
        self._stop_random_client()
        self._stop_ai_agent()
        self._stop_game_server()
        # Keep model file for inspection:
        # if os.path.exists(TEST_AGENT_MODEL_FILE):
        #     os.remove(TEST_AGENT_MODEL_FILE)

    def test_agent_learns_and_saves_model(self):
        self.assertIsNotNone(self.ai_agent_process, "AI Agent process should be started.")
        self.assertIsNotNone(self.random_client_process, "Random client process should be started.")

        start_time = time.time()
        learning_event_logs_found = 0
        model_save_log_found = False
        
        # Let processes run and capture logs
        while time.time() - start_time < LOG_CHECK_TIMEOUT_SECONDS:
            if self.ai_agent_process.poll() is not None: # AI agent terminated prematurely
                print("AI Agent process ended prematurely.")
                break
            if self.random_client_process.poll() is not None: # Random client terminated
                print("Random client process ended.")
                # This might be okay if it just played a few games and exited.
                # Continue checking AI agent logs for a bit more.
                pass

            line = ""
            try:
                # Reading stdout. AI agent logs are expected here.
                line = self.ai_agent_process.stdout.readline()
            except Exception as e:
                print(f"Error reading AI agent stdout: {e}")


            if line:
                print(f"Agent Log: {line.strip()}") # For debugging
                for regex_pattern in EXPECTED_LEARNING_EVENT_REGEXES:
                    if re.search(regex_pattern, line):
                        learning_event_logs_found += 1
                if re.search(EXPECTED_MODEL_SAVE_LOG_REGEX, line):
                    model_save_log_found = True
            
            # Don't break early based on logs found, let it run for the duration
            # to allow model saving to occur based on its own frequency.
            time.sleep(LOG_POLL_INTERVAL_SECONDS)
        
        print(f"Finished log collection phase. Found {learning_event_logs_found} learning events. Model save log found: {model_save_log_found}")

        # Check for learning event logs
        self.assertGreaterEqual(learning_event_logs_found, MIN_GAMES_FOR_LOG_CHECK,
                                f"Expected at least {MIN_GAMES_FOR_LOG_CHECK} learning event logs, found {learning_event_logs_found}.")

        # Check for model save log (if periodic saving is frequent enough for timeout)
        # Or, directly check model file mtime as a more reliable indicator of save.
        
        final_model_file_mtime = 0
        model_exists = os.path.exists(TEST_AGENT_MODEL_FILE)
        if model_exists:
            final_model_file_mtime = os.path.getmtime(TEST_AGENT_MODEL_FILE)
        else:
            # Dump logs if model file not found, as this is a primary assertion failure.
            print("Model file not found. Dumping AI agent logs:")
            # Attempt to communicate to get remaining logs, with a timeout
            try:
                stdout, stderr = self.ai_agent_process.communicate(timeout=5)
                print("AI Agent stdout:\n", stdout)
                print("AI Agent stderr:\n", stderr)
            except subprocess.TimeoutExpired:
                print("Timeout expired while trying to get remaining logs from AI agent.")
            except Exception as e:
                print(f"Error during final communicate: {e}")
            self.fail(f"Model file {TEST_AGENT_MODEL_FILE} was not created.")


        self.assertGreater(final_model_file_mtime, self.initial_model_file_mtime,
                           "Model file modification timestamp did not change, indicating model was not saved or overwritten.")
        
        # Optionally, also assert if model_save_log_found is True if save frequency is high.
        # For lower save frequencies, mtime check is more robust for this test duration.
        if not model_save_log_found:
            print("Note: Model save log message was not found in stdout during test duration. "
                  "Relying on file modification time. This might be okay if save frequency is low.")


if __name__ == '__main__':
    print("Reminder: Game server and random client start/stop logic are placeholders.")
    print(f"Ensure '{GAME_SERVER_DOCKER_IMAGE}', '{AI_AGENT_SCRIPT_PATH}', '{RANDOM_CLIENT_SCRIPT_PATH}' are correct.")
    print(f"This test will run for {LOG_CHECK_TIMEOUT_SECONDS} seconds to observe learning and model saving.")
    print(f"Expected learning log patterns (any of these for each event type):")
    for r in EXPECTED_LEARNING_EVENT_REGEXES:
        print(f"  - r\"{r}\"")
    print(f"Expected model save log pattern: r\"{EXPECTED_MODEL_SAVE_LOG_REGEX}\"")
    print(f"Ensure the AI agent's MODEL_SAVE_FREQUENCY is set to a value that allows saving within {LOG_CHECK_TIMEOUT_SECONDS}s for the model save to be reliably tested by mtime and log.")
    unittest.main()
```
