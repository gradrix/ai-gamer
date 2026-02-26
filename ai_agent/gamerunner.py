import time
import threading
import logging
import os
from common.rpc.rpcclient import GameEngineRpcClient
from common.models.enums import PlayerStatus, MoveStatus, PlayerRegistration
from .network.controller import Controller

logger = logging.getLogger(__name__)

class GameRunner:

    def __init__(self, host, port, agentName):
        self.client = GameEngineRpcClient(host, port)
        self.nnController = Controller(agentName)
        self.playerId = agentName
        self.__initKeepAliveRequestor()
        self.__register()

    def start(self):
        self.nnController.initialize()

        # Get delay from environment variable, default to 0.1 seconds
        delay = float(os.getenv('AGENT_LOOP_DELAY', '0.1'))

        while True:
            canMove = self.client.canMove(self.playerId)
            logger.info("Can move: " + str(canMove))
            match canMove:
                case PlayerStatus.UnregisteredPlayer:
                    self.__register()
                case PlayerStatus.Won:
                    self.__gameEnded('I\'ve won!')
                    self.nnController.won()
                case PlayerStatus.Lost:
                    self.__gameEnded('I\'ve lost :-/')
                    self.nnController.lost()
                case PlayerStatus.Draw:
                    self.__gameEnded('It\'s a draw..')
                    self.nnController.draw()
                case PlayerStatus.CanMove:
                    self.__makeSomeMove()

            # Add configurable delay to prevent excessive polling and reduce CPU usage
            if delay > 0:
                time.sleep(delay)

    def __register(self) -> bool:
        registration = self.client.registerPlayer(self.playerId)
        match registration:
            case PlayerRegistration.NoPlayerSlotsLeft:
                logger.critical("No place in server")
                raise Exception('No free player slots availabe - won\'t be able to participate..')
            case PlayerRegistration.AlreadyRegistered:
                logger.info('Logging in as already registered '+self.playerId)
                return True
            case _:
                return True
            
    def __gameEnded(self, message):
        logger.debug(str(message) + '. Waiting for the game to be started again..')
        time.sleep(0.01)

    def __makeSomeMove(self):
        grid = self.client.getCurrentBoard()
        possibleMoves = self.client.getPossibleMoves()

        moveResult = None
        while (moveResult != MoveStatus.Error and moveResult != MoveStatus.Success):
            predicted = self.nnController.guess(grid, possibleMoves)
            moveResult = self.client.move(self.playerId, predicted).status
            if (moveResult == MoveStatus.Success):
                mv = possibleMoves[predicted]
                logger.debug('I\'m moving to: '+str(mv[0])+':'+str(mv[1]))
                self.nnController.moved(predicted)
            elif (moveResult == MoveStatus.Incorrect):
                self.nnController.incorrect()
            # Remove the delay to allow fast gameplay
            # time.sleep(3)

    def __initKeepAliveRequestor(self):
        thread = threading.Thread(target=self.__keepAliveRequestor, args=())
        thread.daemon = True
        thread.start()

    def __keepAliveRequestor(self):
        while True:
            self.client.keepAlive(self.playerId)
            time.sleep(2)