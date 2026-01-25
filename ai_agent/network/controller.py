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

    def initialize(self):
        self.__initModelSaver()
        self.__initTrainingLoop()

    #Try to guess until NN chooses non padded index
    def guess(self, board, moves):
        prediction = INCORRECT_MOVE
        while (prediction < 0):
            (padded_board, padded_moves, prediction) = self.modelManager.predict(board, moves)
            self.paddedBoard = padded_board
            self.paddedMoves = padded_moves
            self.current_state = [padded_board, padded_moves]
            if (prediction < 0):
                self.lastPrediction = 0 - prediction
                self._remember_experience(prediction, REWARD['INCORRECT'], True)
            self.lastPrediction = prediction
        return prediction
    
    def moved(self, moveIndex):
        self._remember_experience(moveIndex, REWARD['MOVED'], False)
        self.last_action = moveIndex
    
    def won(self):
        self._remember_experience(self.lastPrediction, REWARD['WON'], True)

    def lost(self):
        self._remember_experience(self.lastPrediction, REWARD['LOST'], True)

    def draw(self):
        self._remember_experience(self.lastPrediction, REWARD['DRAW'], True)

    def incorrect(self):
        self._remember_experience(self.lastPrediction, REWARD['INCORRECT'], True)

    def _remember_experience(self, action, reward, done):
        """Store experience in replay buffer for later training"""
        if self.last_state is not None and self.current_state is not None:
            # Store the transition: (last_state, action, reward, current_state, done)
            self.modelManager.remember(self.last_state, action, reward, self.current_state, done)
        
        # Update last_state for next transition
        self.last_state = self.current_state

    def _train(self):
        """Train on a batch from replay buffer"""
        self.modelManager.train()
        
        # Periodically update target network
        if np.random.rand() < 0.01:  # 1% chance to update target network
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
            time.sleep(1)  # Train every second