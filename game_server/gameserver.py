import threading
import time
import grpc
import logging
from google.protobuf import empty_pb2 as EmptyRequest
from concurrent import futures

from common.rpc import gameapi_pb2
from common.rpc import gameapi_pb2_grpc
from common.models.enums import MoveStatus, PlayerStatus, PlayerRegistration, GameStatus
from common.models.move import Move
from common.models.gamebase import GameBase
from .state.gamestatemanager import GameStateManager
from common.timehelpers import currentTimestamp
import common.rpc.codec as codec

PORT = 8080
HOST = 'localhost'

logger = logging.getLogger(__name__)

class GameRpcServer(gameapi_pb2_grpc.GameApiServicer):

    def __init__(self, gameProgram):
        self.lock = threading.Lock()
        self.state = GameStateManager()
        self.gameProgram: GameBase = gameProgram
        self.restarting = False
        self.startNewGame()
        self.__checkForGameStatus()
        self.__initPlayerConnectionChecker()

    #gRPC methods
    def registerPlayer(self, request: gameapi_pb2.PlayerNameRequest, context):
        playerName = request.playerName
        logger.info('Registering player '+str(playerName) + ' ... ')
        result = self.__validatePlayer(playerName)
        match result:
            case PlayerRegistration.Success:
                player = self.state.registerPlayer(playerName)
                self.__syncPlayers()
                logger.info('Newly registered with '+str(player.id)+'.')
            case PlayerRegistration.AlreadyRegistered:
                player = self.state.registerPlayer(playerName)
                self.__syncPlayers()
                logger.info('Already registered with id '+str(player.id)+'.')
            case PlayerRegistration.NoPlayerSlotsLeft:
                players = self.state.playersList
                playersStr = ''
                for player in players:
                    playersStr += str(player)+' '
                logger.warning('No player slots available for ' +str(player.name)+ 'as we already have: '+playersStr)
        return codec.encodeRegisterPlayerResponse(result)

    def getPossibleMoves(self, request: EmptyRequest, context):
        result = self.gameProgram.getPossibleMoves()
        return codec.encodeGetPossibleMovesResponse(result)

    def getCurrentBoard(self, request: EmptyRequest, context):
        result = self.gameProgram.getCurrentBoard()
        return codec.encodeGetCurrentBoardResponse(result)

    def canMove(self, request: gameapi_pb2.PlayerNameRequest, context):
        self.__checkForGameStatus()
        playerName = request.playerName
        
        if (self.state.hasGameEnded()):
            self.state.endGame(self.state.playersList)

        if (self.state.game.status != GameStatus.Started or self.areEnoughPlayers() == False):
            result = PlayerStatus.Wait
        else:
            result = self.gameProgram.canMove(playerName)
        return codec.encodeCanMoveResponse(result)

    def move(self, request: gameapi_pb2.MoveRequest, context):
        result = self.gameProgram.move(request.playerName, request.index)
        moveResult = codec.encodeMoveResponse(result)
        if (result.status == MoveStatus.Success):
            move = Move(None, self.state.game.id, self.state.players[request.playerName].id, request.index, moveResult.move, currentTimestamp())
            self.state.addMove(move)
        return moveResult

    def keepAlive(self, request: gameapi_pb2.PlayerNameRequest, context):
        playerName = request.playerName
        if (playerName in self.state.players):
            self.state.players[playerName].lastonline = currentTimestamp()
        return gameapi_pb2.KeepAliveResponse()
    #End of gRPC methods
    
    def startNewGame(self):
        if (len(self.state.playersList) < self.gameProgram.requiredNumOfPlayers):
            return False
        with self.lock:
            started = self.gameProgram.startNewGame(self.state.playersList)
            if (started and not(self.state.isGameRunning())):
                self.state.registerGame()
            return started
    
    def areEnoughPlayers(self):
        return (len(self.state.playersList) >= self.gameProgram.requiredNumOfPlayers)
    
    def __checkForGameStatus(self):
        if (self.state.isGameRunning() == False):
            if (self.restarting == False):
                if (self.areEnoughPlayers()):
                    logger.info(self.state.whoWon()+' Restarting game..')
                else:
                    logger.info('Starting game..')
                self.restarting = True
            self.started = self.startNewGame()
            if (self.started):
                self.restarting = False

    def __validatePlayer(self, playerName):
        if (self.state.doesPlayerExist(playerName)):
            return PlayerRegistration.AlreadyRegistered
        elif (self.areEnoughPlayers()):
            return PlayerRegistration.NoPlayerSlotsLeft
        else:
            return PlayerRegistration.Success
	  
    def __initPlayerConnectionChecker(self):
        thread = threading.Thread(target=self.__removeInactivePlayers, args=())
        thread.daemon = True
        thread.start()

    def __removeInactivePlayers(self):
        while True:
            if (self.state.isGameRunning()):
                currentTime = currentTimestamp()
                for player in self.state.playersList:
                    msElapsed = currentTime - player.lastonline
                    if (msElapsed > 3000):
                        logger.warning('Removing player \''+str(player.name)+'\' who has been inactive for '+str(msElapsed)+'ms ..')
                        self.state.inactivatePlayer(player.name)
            time.sleep(1)

    def __syncPlayers(self):
        if (self.areEnoughPlayers() == True):
            self.gameProgram.syncPlayers(self.state.playersList)

class GameServer:

    def __init__(self, gameProgram):
        self.gameServer = GameRpcServer(gameProgram)
        self.started = False

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        gameapi_pb2_grpc.add_GameApiServicer_to_server(self.gameServer, server)
        server.add_insecure_port('[::]:'+str(PORT))
        logger.info("gRPC starting")
        server.start()
        server.wait_for_termination()
