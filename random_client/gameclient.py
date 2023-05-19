
import random
import time
import threading

from random_client.rpcclient import GameEngineRpcClient
from common.models.enums import PlayerStatus, MoveStatus, PlayerRegistration

class GameClient:

    def __init__(self, host, port, agentName):
        self.client = GameEngineRpcClient(host, port)
        self.playerId = agentName
        self.__initKeepAliveRequestor()
        self.__register()

    def start(self):
        while True:
            canMove = self.client.canMove(self.playerId)
            match canMove:
                case PlayerStatus.UnregisteredPlayer:
                    self.__register()
                case PlayerStatus.Won:
                    self.__gameEnded('I\'ve won!')
                case PlayerStatus.Lost:
                    self.__gameEnded('I\'ve lost :-/')
                case PlayerStatus.Draw:
                    self.__gameEnded('It\'s a draw..')
                case PlayerStatus.CanMove:
                    self.__makeSomeMove()

    #TODO make AI move
    def __makeSomeMove(self):
        #currentBoard = self.client.getCurrentBoard()
        possibleMoves = self.client.getPossibleMoves()

        #pick random move
        moveResult = None
        while (moveResult != MoveStatus.Error and moveResult != MoveStatus.Success):
            move = random.randint(0, len(possibleMoves) - 1)
            moveResult = self.client.move(self.playerId, move).status
            if (moveResult == MoveStatus.Success):
                mv = possibleMoves[move]
                print('I\'m moving to: '+str(mv[0])+':'+str(mv[1]))
    
    def __register(self) -> bool:
        registration = self.client.registerPlayer(self.playerId)
        match registration:
            case PlayerRegistration.NoPlayerSlotsLeft:
                raise Exception('No free player slots availabe - won\'t be able to participate..')
            case PlayerRegistration.AlreadyRegistered:
                print('Logging in as already registered '+self.playerId)
                return True
            case _:
                return True
    
    def __gameEnded(self, message):
        print(str(message) + '. Waiting for the game to be started again..')
        time.sleep(0.1)

    def __initKeepAliveRequestor(self):
        thread = threading.Thread(target=self.__keepAliveRequestor, args=())
        thread.daemon = True
        thread.start()

    def __keepAliveRequestor(self):
        while True:
            self.client.keepAlive(self.playerId)
            time.sleep(2)
