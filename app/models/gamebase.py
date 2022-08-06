from abc import ABC, abstractmethod

from models.enums import Move

# ------------------------------ #
#     Abstract class of games    #
# ------------------------------ #
class GameBase(ABC):

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def startNewGame(self):
        pass

    @abstractmethod
    def registerPlayer(self, playerId):
        pass

    #Return array of not correct moves but theoretically possible moves
    @abstractmethod
    def getPossibleMoves(self):
        pass

    @abstractmethod
    def getCurrentBoard(self):
        pass

    @abstractmethod
    def getCurrentBoardString(self):
        pass

    @abstractmethod
    def canMove(self, playerId):
        pass

    #Return False if move is invalid
    @abstractmethod
    def move(self, playerId, index):
        pass
          
    @abstractmethod
    def getPlayerStatuses(self) -> Move:
        pass