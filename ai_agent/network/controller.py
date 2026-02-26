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
        self.pending_state = None
        self.pending_action = None

    def initialize(self):
        self.__initModelSaver()
        self.__initTrainingLoop()

    # Try to guess until NN chooses non padded index
    def guess(self, board, moves):
        import time

        start_time = time.time()

        (padded_board, padded_moves, prediction) = self.modelManager.predict(
            board, moves
        )
        self.paddedBoard = padded_board
        self.paddedMoves = padded_moves
        self.lastPrediction = prediction
        self.current_state = [padded_board, padded_moves]

        # Remember previous turn's pending experience (now have next_state)
        if self.pending_state is not None and self.pending_action is not None:
            self.modelManager.remember(
                self.pending_state,
                self.pending_action,
                REWARD["MOVED"],
                self.current_state,
                False,
            )
            logger.debug("Remembered previous turn's experience")

        # Prepare pending for this turn's action
        self.pending_state = [padded_board.copy(), padded_moves.copy()]
        self.pending_action = prediction

        end_time = time.time()
        logger.debug(f"AI move took {(end_time - start_time) * 1000:.1f}ms")

        return prediction

    def moved(self, moveIndex):
        self.last_action = moveIndex
        logger.debug(f"Move confirmed: {moveIndex}")

    def won(self):
        if self.pending_state is not None and self.pending_action is not None:
            final_next_state = (
                self.current_state
                if self.current_state is not None
                else [
                    np.zeros_like(self.pending_state[0]),
                    np.zeros_like(self.pending_state[1]),
                ]
            )
            self.modelManager.remember(
                self.pending_state,
                self.pending_action,
                REWARD["WON"],
                final_next_state,
                True,
            )
        self.pending_state = None
        self.pending_action = None
        self._train()
        logger.info("Game won - terminal experience stored")

    def lost(self):
        if self.pending_state is not None and self.pending_action is not None:
            final_next_state = (
                self.current_state
                if self.current_state is not None
                else [
                    np.zeros_like(self.pending_state[0]),
                    np.zeros_like(self.pending_state[1]),
                ]
            )
            self.modelManager.remember(
                self.pending_state,
                self.pending_action,
                REWARD["LOST"],
                final_next_state,
                True,
            )
        self.pending_state = None
        self.pending_action = None
        self._train()
        logger.info("Game lost - terminal experience stored")

    def draw(self):
        if self.pending_state is not None and self.pending_action is not None:
            final_next_state = (
                self.current_state
                if self.current_state is not None
                else [
                    np.zeros_like(self.pending_state[0]),
                    np.zeros_like(self.pending_state[1]),
                ]
            )
            self.modelManager.remember(
                self.pending_state,
                self.pending_action,
                REWARD["DRAW"],
                final_next_state,
                True,
            )
        self.pending_state = None
        self.pending_action = None
        self._train()
        logger.info("Game draw - terminal experience stored")

    def incorrect(self):
        # Store invalid prediction as terminal experience with negative reward
        if self.current_state is not None:
            dummy_next = [
                np.zeros_like(self.current_state[0]),
                np.zeros_like(self.current_state[1]),
            ]
            self.modelManager.remember(
                self.current_state,
                self.lastPrediction,
                REWARD["INCORRECT"],
                dummy_next,
                True,
            )
        self.pending_action = None  # Reset for retry
        logger.warning(f"Incorrect prediction {self.lastPrediction} penalized")

    def _train(self):
        """Train on a batch from replay buffer"""
        # Only train if there are enough experiences in the buffer
        if hasattr(self.modelManager, "replay_buffer"):
            if (
                len(self.modelManager.replay_buffer.buffer) >= 64
            ):  # Use proper batch size
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
            time.sleep(
                2
            )  # Train every 2 seconds - balance between learning and performance
