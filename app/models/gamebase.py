from abc import ABCMeta, abstractmethod, abstractproperty
from models.game import MoveResult
from models.player import Player

# ------------------------------ #
#     Abstract class of games    #
# ------------------------------ #
class GameBase(metaclass=ABCMeta):

    @abstractproperty
    def requiredNumOfPlayers(self) -> int:
        pass

    @abstractmethod
    def startNewGame(self, players: list[Player]):
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
          
    #Syncs players
    @abstractmethod
    def syncPlayers(self, players: list[Player]):
        pass