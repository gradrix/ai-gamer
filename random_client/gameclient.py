
import random
import time
import threading
import os

from common.rpc.rpcclient import GameEngineRpcClient
from common.models.enums import PlayerStatus, MoveStatus, PlayerRegistration

class GameClient:

    def __init__(self, host, port, agentName):
        self.client = GameEngineRpcClient(host, port)
        self.playerId = agentName
        print('Starting game client as: '+self.playerId)
        self.__initKeepAliveRequestor()
        self.__register()

    def start(self):
        # Get delay from environment variable, default to 0.2 seconds for stability
        delay = float(os.getenv('CLIENT_LOOP_DELAY', '0.0'))

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

            # Add configurable delay to prevent excessive polling and reduce CPU usage
            if delay > 0:
                time.sleep(delay)

    def __makeSomeMove(self):
        import time
        start_time = time.time()

        possibleMoves = self.client.getPossibleMoves()
        #pick random move
        moveResult = None
        attempts = 0
        while (moveResult != MoveStatus.Error and moveResult != MoveStatus.Success):
            move = random.randint(0, len(possibleMoves) - 1)
            moveResult = self.client.move(self.playerId, move).status
            attempts += 1
            if (moveResult == MoveStatus.Success):
                mv = possibleMoves[move]
                print('I\'m moving to: '+str(mv[0])+':'+str(mv[1]))
            if attempts > 50:  # Prevent infinite loop
                break

        end_time = time.time()
        if (end_time - start_time) > 0.1:  # Log if it takes more than 100ms
            print(f'Random move took {(end_time - start_time)*1000:.1f}ms with {attempts} attempts')
    
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
        time.sleep(0.01)

    def __initKeepAliveRequestor(self):
        thread = threading.Thread(target=self.__keepAliveRequestor, args=())
        thread.daemon = True
        thread.start()

    def __keepAliveRequestor(self):
        while True:
            self.client.keepAlive(self.playerId)
            time.sleep(2)
