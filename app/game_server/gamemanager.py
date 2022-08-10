import threading
import time
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

from models.enums import GameStatus, Mode, PlayerRegistration
from game_server.consolecontroller import ConsoleController

PORT = 8080
HOST = 'localhost'
GAME_END_STATUSES = set([GameStatus.Draw,  GameStatus.Lost,  GameStatus.Won])

##Todo move this outside of project
class GameEngine:

    def __init__(self, mode, game):
        self.game = game
        self.mode = Mode(mode)
        self.server = None
        self.playerStatuses = {}

        print('Initializing engine with '+str(self.mode))
        if (self.mode == Mode.Rpc or self.mode == Mode.Mixed):
            rpc = threading.Thread(target=self.__rpcListener, args=())
            rpc.daemon = True
            rpc.start()

        if (self.mode == Mode.Console or self.mode == Mode.Mixed):
            console = threading.Thread(target=self.__cmdListener, args=())
            console.daemon = True
            console.start()

    def start(self):
        while True:
            statuses = self.game.getPlayerStatuses()
            endStatuses = [s for s in statuses if s in GAME_END_STATUSES]
            if (len(statuses) == len(endStatuses)):
                print('Game ended.. restarting game.')
                self.game.startNewGame()            
            time.sleep(0.25)

    def __rpcListener(self):
        self.server = SimpleJSONRPCServer((HOST, PORT), logRequests=False)
        self.server.register_function(self.__registerPlayer, 'registerPlayer')
        self.server.register_function(self.game.getPossibleMoves)
        self.server.register_function(self.game.getCurrentBoard)
        self.server.register_function(self.game.canMove)
        self.server.register_function(self.game.move)
        print('Starting RPC server on '+str(HOST)+':'+str(PORT))
        self.server.serve_forever()

    def __cmdListener(self):
        cmdController = ConsoleController(self.game, self.mode)
        cmdController.start()

    #Wrapping RPC methods
    def __registerPlayer(self, playerId):
        print('Registering '+str(playerId) + ' ... ', end='')
        result = self.game.registerPlayer(playerId)
        print(str(result))
        return result

    # def __canMove(self, playerId):
    #     return self.game.canMove(playerId)