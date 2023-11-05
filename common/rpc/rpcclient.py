from array import array
import grpc

from common.rpc import gameapi_pb2_grpc, gameapi_pb2
from common.models.enums import PlayerStatus
import common.rpc.codec as codec

class GameEngineRpcClient:

    def __init__(self, host, port):
        self.host = host
        self.server_port = int(port)

        # instantiate a channel
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = gameapi_pb2_grpc.GameApiStub(self.channel)

    def registerPlayer(self, playerName: str):
        request = codec.encodePlayerNameRequest(playerName)
        print('Registering player with '+playerName)
        result = self.stub.registerPlayer(request)
        return codec.decodeRegisterPlayerResponse(result)

    def getPossibleMoves(self) -> array:
        result = self.stub.getPossibleMoves(gameapi_pb2.GetPossibleMovesRequest())
        return codec.decodeGetPossibleMovesResponse(result)

    def getCurrentBoard(self):
        result = self.stub.getCurrentBoard(gameapi_pb2.GetCurrentBoardRequest())
        return codec.decodeGetCurrentBoardResponse(result)

    def canMove(self, playerName):
        request = codec.encodePlayerNameRequest(playerName)
        try:
            result = self.stub.canMove(request)
        except:
            result = PlayerStatus.Wait
        finally:
            return codec.decodeCanMoveResponse(result)

    def move(self, playerName, index):
        request = codec.encodeMoveRequest(playerName, index)
        result = self.stub.move(request)
        return codec.decodeMoveResponse(result)

    def keepAlive(self, playerName):
        request = codec.encodePlayerNameRequest(playerName)
        self.stub.keepAlive(request)
        return
 