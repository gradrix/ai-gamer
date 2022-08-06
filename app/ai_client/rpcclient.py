from array import array
from jsonrpclib import Server

class GameEngineRpcClient:

    def __init__(self, host, port):
        self.client = Server('http://'+str(host)+':'+str(port))

    def register(self, playerId):
        print('Registering player with '+playerId)
        return self.client.registerPlayer(playerId)

    def getPossibleMoves(self) -> array:
        return self.client.getPossibleMoves()

    def getCurrentBoard(self):
        return self.client.getCurrentBoard()

    def canMove(self, playerId):
        return self.client.canMove(playerId)

    def move(self, playerId, index):
        return self.client.move(playerId, index)
        
    def registerPlayer(self, par):
        return self.client.registerPlayer(par)

    def isAlive(self, playerId):
        return self.client.isAlive(playerId)
