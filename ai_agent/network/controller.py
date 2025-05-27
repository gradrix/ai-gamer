import logging
import numpy as np
from .neuralnetwork import NeuralNetwork, DQNAgent, REWARD

logger = logging.getLogger(__name__)

class Controller:

    def __init__(self, agentId):
        self.agentId = agentId
        self.nn = None
        self.agent = None
        self.board_height = None
        self.board_width = None
        self.num_channels = 1  # Default number of channels
        self.last_state_processed = None
        self.last_action = None
        # REWARD is already imported and available

    def initialize_network_components(self, board_height, board_width, num_actions):
        """
        Initializes the NeuralNetwork and DQNAgent based on game dimensions.
        Called by GameRunner.
        """
        self.board_height = board_height
        self.board_width = board_width
        # Assuming num_channels is fixed for now, or can be passed if dynamic
        
        # NeuralNetwork constructor: agentName, board_height, board_width, num_actions, num_channels=1
        self.nn = NeuralNetwork(self.agentId, self.board_height, self.board_width, num_actions, self.num_channels)
        self.agent = DQNAgent(self.nn) # DQNAgent uses nn.model and nn.num_actions
        
        logger.info(f"Controller {self.agentId}: Network components initialized. "
                    f"Board: {board_height}x{board_width}x{self.num_channels}, Actions: {num_actions}")

    def guess(self, board_array):
        """
        Preprocesses the board state and gets an action from the DQNAgent.
        Input board_array is a 2D NumPy array.
        """
        if self.agent is None or self.board_height is None:
            logger.error("Agent or board dimensions not initialized. Cannot make a guess.")
            # Return a default/random action or raise an error, depending on desired behavior
            # For now, let's assume GameRunner ensures initialization. If not, this could be an issue.
            # However, num_actions isn't known here to pick a random valid action.
            # This path should ideally not be hit if GameRunner logic is correct.
            raise Exception("Controller not properly initialized before guess.")

        # Preprocess the state: reshape to (1, H, W, C)
        processed_state = board_array.reshape(1, self.board_height, self.board_width, self.num_channels)
        
        self.last_state_processed = processed_state
        action = self.agent.act(processed_state) # DQNAgent.act expects a batched state
        self.last_action = action
        
        return action
    
    def _learn_from_experience(self, event_type: str, reward: float, next_board_array: np.ndarray, done: bool):
        """Helper function to process and learn from an experience."""
        logger.info(f"Controller {self.agentId}: Learning from {event_type}. Reward: {reward}, Done: {done}")
        
        if self.last_state_processed is None or self.last_action is None:
            logger.warning(f"Controller {self.agentId}: Attempted to learn from {event_type} without a stored last state or action. Skipping.")
            return

        if self.agent is None or self.board_height is None:
            logger.error("Agent or board dimensions not initialized. Cannot learn.")
            return
            
        processed_next_state = next_board_array.reshape(1, self.board_height, self.board_width, self.num_channels)
        
        self.agent.remember(self.last_state_processed, self.last_action, reward, processed_next_state, done)
        self.agent.replay() # Perform experience replay

        # Clear last state and action after learning from them
        self.last_state_processed = None
        self.last_action = None

    def moved(self, current_board_array, reward):
        """
        Called by GameRunner after a successful move.
        Learns from the (last_state, last_action, reward, current_state, done=False) tuple.
        """
        # logger.debug(f"Controller {self.agentId}: Move recorded. Reward: {reward}") # Replaced by log in _learn_from_experience
        self._learn_from_experience("successful move", reward, current_board_array, False)

    def incorrect(self, current_board_array):
        """
        Called by GameRunner after an incorrect move.
        Learns from the (last_state, last_action, REWARD['INCORRECT'], current_state, done=True) tuple.
        An incorrect move is treated as a terminal state for that specific action attempt.
        """
        # logger.debug(f"Controller {self.agentId}: Incorrect move recorded.") # Replaced by log in _learn_from_experience
        self._learn_from_experience("incorrect move", REWARD['INCORRECT'], current_board_array, True)
        # Note: 'done' is True here because this particular action sequence terminated due to incorrectness.
        # The game itself might not be over.

    def won(self, final_board_array):
        # logger.debug(f"Controller {self.agentId}: Game won.") # Replaced by log in _learn_from_experience
        self._learn_from_experience("winning game", REWARD['WON'], final_board_array, True)

    def lost(self, final_board_array):
        # logger.debug(f"Controller {self.agentId}: Game lost.") # Replaced by log in _learn_from_experience
        self._learn_from_experience("losing game", REWARD['LOST'], final_board_array, True)

    def draw(self, final_board_array):
        # logger.debug(f"Controller {self.agentId}: Game ended in a draw.") # Replaced by log in _learn_from_experience
        self._learn_from_experience("draw game", REWARD['DRAW'], final_board_array, True)

    # Old methods like _train, initialize, and direct interaction with ModelManager are removed.
    # The class no longer holds paddedBoard or paddedMoves.