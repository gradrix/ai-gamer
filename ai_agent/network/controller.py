import logging
import time
import threading
from .modelmanager import ModelManager, LABEL

logger = logging.getLogger(__name__)
INCORRECT_MOVE = -1

class Controller:

    def __init__(self, agentId):
        self.modelManager = ModelManager(agentId)
        self.paddedBoard = []
        self.paddedMoves = []

    def initialize(self):
        self.__initModelSaver()        

    #Try to guess until NN chooses non padded index
    def guess(self, board, moves):
        prediction = INCORRECT_MOVE
        while (prediction < 0):
            (padded_board, padded_moves, prediction) = self.modelManager.predict(board, moves)
            self.paddedBoard = padded_board
            self.paddedMoves = padded_moves
            if (prediction < 0):
                self.lastPrediction = 0 - prediction
                self.incorrect()
            self.lastPrediction = prediction
        return prediction
    
    def moved(self, moveIndex):
        self._train(moveIndex)
    
    def won(self):
        self._train(LABEL['WON'])

    def lost(self):
        self._train(LABEL['LOST'])

    def draw(self):
        self._train(LABEL['DRAW'])

    def incorrect(self):
        self._train(LABEL['INCORRECT'])

    def _train(self, label):
        if (len(self.paddedBoard) == 0 or len(self.paddedMoves) == 0):
            return
        self.modelManager.train(self.paddedBoard, self.paddedMoves, label, self.lastPrediction)

    def __initModelSaver(self):
        thread = threading.Thread(target=self.__modelSaver, args=())
        thread.daemon = True
        thread.start()

    def __modelSaver(self):
        while True:
            self.modelManager.save()
            time.sleep(30)