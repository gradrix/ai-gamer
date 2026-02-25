import logging
import time
import threading
import numpy as np
from .modelmanager import ModelManager, REWARD

logger = logging.getLogger(__name__)
INCORRECT_MOVE = -1

class Controller:

    def __init__(self, agentId):
        self.modelManager = ModelManager(agentId)
        self.paddedBoard = []
        self.paddedMoves = []
        self.last_state = None
        self.last_action = None
        self.current_state = None
        # Track moves made during the current game for proper credit assignment
        self.game_moves_history = []  # List of (state, action, next_state) tuples

    def initialize(self):
        self.__initModelSaver()
        self.__initTrainingLoop()

    #Try to guess until NN chooses non padded index
    def guess(self, board, moves):
        import time
        start_time = time.time()

        prediction = INCORRECT_MOVE
        attempts = 0
        while (prediction < 0):
            (padded_board, padded_moves, prediction) = self.modelManager.predict(board, moves)
            self.paddedBoard = padded_board
            self.paddedMoves = padded_moves
            self.current_state = [padded_board, padded_moves]
            if (prediction < 0):
                self.lastPrediction = 0 - prediction
                self._remember_experience(prediction, REWARD['INCORRECT'], True)
            self.lastPrediction = prediction
            attempts += 1
            if attempts > 10:  # Prevent infinite loop
                break

        end_time = time.time()
        if (end_time - start_time) > 0.1:  # Log if it takes more than 100ms
            logger.debug(f"AI move took {(end_time - start_time)*1000:.1f}ms with {attempts} attempts")

        return prediction
    
    def moved(self, moveIndex):
        # Remember the experience for this move
        self._remember_experience(moveIndex, REWARD['MOVED'], False)
        self.last_action = moveIndex

        # Add this move to the game history for proper credit assignment later
        # Store the state that led to this action, the action taken, and the resulting state
        if self.last_state is not None and self.current_state is not None:
            self.game_moves_history.append((self.last_state, moveIndex, self.current_state))
    
    def won(self):
        # Assign positive reward to all moves made in this game
        self._assign_credit_to_game_moves(REWARD['WON'])
        # Trigger immediate training to reinforce winning moves
        self._train()
        # Clear the game history
        self.game_moves_history = []

    def lost(self):
        # Assign negative reward to all moves made in this game
        self._assign_credit_to_game_moves(REWARD['LOST'])
        # Trigger immediate training to learn from losing moves
        self._train()
        # Clear the game history
        self.game_moves_history = []

    def draw(self):
        # Assign neutral reward to all moves made in this game
        self._assign_credit_to_game_moves(REWARD['DRAW'])
        # Trigger immediate training
        self._train()
        # Clear the game history
        self.game_moves_history = []

    def _assign_credit_to_game_moves(self, final_game_result):
        """
        Assign credit to all moves made during the game based on final outcome.
        Implements Monte Carlo learning for the entire game episode.
        """
        # Apply the final game result to all moves made during this game
        # Only the last move in the game should be marked as done (terminal)
        for i, (state, action, next_state) in enumerate(self.game_moves_history):
            # For all moves except the last one, mark as not done (not terminal)
            # Only the final move is terminal
            is_terminal = (i == len(self.game_moves_history) - 1)
            self.modelManager.remember(state, action, final_game_result, next_state, is_terminal)

        # Trigger immediate training on the completed game
        if len(self.game_moves_history) > 0:
            self._train()

    def incorrect(self):
        self._remember_experience(self.lastPrediction, REWARD['INCORRECT'], True)
        # Also add this incorrect move to the game history so it gets proper credit assignment
        if self.last_state is not None and self.current_state is not None:
            self.game_moves_history.append((self.last_state, self.lastPrediction, self.current_state))

    def _remember_experience(self, action, reward, done):
        """Store experience in replay buffer for later training"""
        if self.last_state is not None and self.current_state is not None:
            # Store the transition: (last_state, action, reward, current_state, done)
            self.modelManager.remember(self.last_state, action, reward, self.current_state, done)

        # Update last_state for next transition, but only if not done (terminal state)
        if not done:
            self.last_state = self.current_state
        else:
            # When game ends, clear the last state to start fresh in next game
            self.last_state = None

    def _train(self):
        """Train on a batch from replay buffer"""
        # Only train if there are enough experiences in the buffer
        if hasattr(self.modelManager, 'replay_buffer'):
            if len(self.modelManager.replay_buffer.buffer) >= 64:  # Use proper batch size
                self.modelManager.train()

        # Periodically update target network (less frequent to reduce overhead)
        if np.random.rand() < 0.005:  # 0.5% chance to update target network
            self.modelManager.update_target_network()

    def __initModelSaver(self):
        thread = threading.Thread(target=self.__modelSaver, args=())
        thread.daemon = True
        thread.start()

    def __modelSaver(self):
        while True:
            self.modelManager.save()
            time.sleep(30)
    
    def __initTrainingLoop(self):
        thread = threading.Thread(target=self.__trainingLoop, args=())
        thread.daemon = True
        thread.start()
    
    def __trainingLoop(self):
        """Continuous training loop"""
        while True:
            self._train()
            time.sleep(2)  # Train every 2 seconds - balance between learning and performance