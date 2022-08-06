
import random
import uuid
import time

from ai_client.rpcclient import GameEngineRpcClient
from models.enums import GameStatus, Move, PlayerRegistration

class GameClient:

    def __init__(self, host, port):
        self.client = GameEngineRpcClient(host, port)
        self.__register()

    def start(self):
        while True:
            canMove = self.client.canMove(self.playerId)
            match canMove:
                case GameStatus.UnregisteredPlayer:
                    self.register()
                case GameStatus.Won:
                    self.__gameEnded('I\'ve won!')
                case GameStatus.Lost:
                    self.__gameEnded('I\'ve lost :-/')
                case GameStatus.Draw:
                    self.__gameEnded('It\'s a draw..')
                case GameStatus.CanMove:
                    self.__makeSomeMove()
            time.sleep(1)

    #TODO make AI move
    def __makeSomeMove(self):
        #currentBoard = self.client.getCurrentBoard()
        possibleMoves = self.client.getPossibleMoves()

        #pick random move
        moveResult = None
        while (moveResult != Move.Error and moveResult != Move.Success):
            move = random.randint(0, len(possibleMoves) - 1)
            moveResult = self.client.move(self.playerId, move)        
    
    def __register(self) -> bool:
        self.__generateNewId()
        registration = self.client.register(self.playerId)
        match registration:
            case PlayerRegistration.NoPlayerSlotsLeft:
                raise Exception('No free player slots availabe - won\'t be able to participate..')
            case PlayerRegistration.AlreadyRegistered:
                print('Already registered.. I shouldn\'t be trying this..')
                return True
            case _:
                return True

    def __generateNewId(self):
        self.playerId = 'ai-' +str(uuid.uuid4())
    
    def __gameEnded(self, message):
        print(str(message) + '. Waiting for the game to be started again..')
        time.sleep(1)

    