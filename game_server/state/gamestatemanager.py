from .recorderdb import RecorderDb
from common.models.game import Game
from common.models.move import Move
from common.models.player import Player
from common.models.enums import PlayerStatus, GameStatus

class GameStateManager:
    def __init__(self):
        self.db = RecorderDb()
        self.game = Game(None, dict(), None, GameStatus.Created)
        self.moves = []

    def registerPlayer(self, playerName: str):
        player = self.db.getPlayer(playerName)
        if (player == None):
            player = self.db.createPlayer(playerName)
        else:
            print('Loading existing player.')

        player.status = PlayerStatus.Wait
        self.game.players[playerName] = player
        return player

    def registerGame(self):
        players = self.game.players
        game = self.db.createGame()
        game.players = players
        self.game = game
        self.moves = []

    def endGame(self, players: list[Player]):
        if (self.game.status == GameStatus.Ended):
            return
        match self.__isDraw():
            case True:
                self.game.status = GameStatus.EndedDraw
            case False:
                self.game.status = GameStatus.Ended
        self.game = self.db.updateGame(self.game)
        for player in players:
            self.db.updatePlayer(player)
        self.db.addMoves(self.moves)

    def addMove(self, move: Move):
        self.moves.append(move)

    def isGameRunning(self):
        return self.game.status in [GameStatus.Started]

    def hasGameEnded(self):
        endStatuses = [PlayerStatus.Draw, PlayerStatus.Lost, PlayerStatus.Won]
        finishedPlayers = [p for p in self.playersList if p.status in endStatuses]
        return len(finishedPlayers) == len(self.playersList)
    
    def whoWon(self):
        winner: Player = None
        if (self.game.status == GameStatus.Ended):
            winner = [p for p in self.playersList if p.status == PlayerStatus.Won][0]
        if (winner == None):
            return "It was draw!"
        else:
            return str(winner) + " has won!"

    def inactivatePlayer(self, playerName):
        del self.game.players[playerName]

    def doesPlayerExist(self, playerName: str):
        player = self.db.getPlayer(playerName)
        return player != None

    @property
    def players(self):
        return self.game.players

    @property
    def playersList(self):
        return list(self.game.players.values())

    def __isDraw(self):
        drawPlayers = [p for p in self.playersList if p.status in [PlayerStatus.Draw]]
        return len(drawPlayers) == len(self.playersList)
