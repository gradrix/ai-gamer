import logging
from .recorderdb import RecorderDb
from common.models.game import Game
from common.models.move import Move
from common.models.player import Player
from common.models.enums import PlayerStatus, GameStatus
from common.timehelpers import currentTimestamp

logger = logging.getLogger(__name__)

class GameStateManager:
    def __init__(self):
        self.db = RecorderDb()
        self.game = Game(None, dict(), None, GameStatus.Created)
        self.moves = []

    def registerPlayer(self, playerName: str, is_ai: bool = False):
        player = self.db.getPlayer(playerName)
        if (player == None):
            player = self.db.createPlayer(playerName, is_ai)
        else:
            player.lastonline = currentTimestamp()
            logger.info('Loading existing player.')

        player.status = PlayerStatus.Wait
        self.game.players[playerName] = player
        return player

    def registerGame(self):
        players = self.game.players
        # Ensure we have unique players for this game
        unique_players = {}
        for name, player in players.items():
            if player.id not in [p.id for p in unique_players.values()]:
                unique_players[name] = player

        # Log if we filtered out duplicate players
        if len(unique_players) != len(players):
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Filtered duplicate players from game. Had {len(players)}, now {len(unique_players)}")

        game = self.db.createGame()
        game.players = unique_players
        self.game = game
        self.moves = []

    def endGame(self, players: list[Player]):
        # Only process if game hasn't been ended yet
        if (self.game.status == GameStatus.Ended or self.game.status == GameStatus.EndedDraw):
            return

        try:
            # Log the game ending process
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Ending game {self.game.id} with {len(players)} players: {[f'{p.name}(ID:{p.id})' for p in players]}")

            # Determine game status and record results for all players
            if self.__isDraw():
                self.game.status = GameStatus.EndedDraw
                logger.info(f"Game {self.game.id} ended in draw")
                # For a draw, all players get result 3 (draw)
                for player in players:
                    # Ensure each player gets a result recorded
                    logger.info(f"Recording draw result for player {player.name} (ID: {player.id}) in game {self.game.id}")
                    self.db.recordGameResult(self.game.id, player.id, 3)  # 3 = Draw
            else:
                self.game.status = GameStatus.Ended
                logger.info(f"Game {self.game.id} ended normally")
                # Record individual results based on player status
                for player in players:
                    # Default to draw if status is unclear
                    result = 3  # Default to draw
                    if player.status == PlayerStatus.Won:
                        result = 1  # Win
                    elif player.status == PlayerStatus.Lost:
                        result = 2  # Loss
                    elif player.status == PlayerStatus.Draw:
                        result = 3  # Draw

                    result_text = {1: 'Win', 2: 'Loss', 3: 'Draw'}.get(result, f'Unknown({result})')
                    logger.info(f"Recording {result_text} result for player {player.name} (ID: {player.id}, Status: {player.status}) in game {self.game.id}")
                    self.db.recordGameResult(self.game.id, player.id, result)

            # Update game status in database
            updated_game = self.db.updateGame(self.game)
            if updated_game == -1:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to update game {self.game.id} status to {self.game.status}")
            else:
                self.game = updated_game
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f"Successfully updated game {self.game.id} status to {self.game.status}")

            # Update player records
            for player in players:
                self.db.updatePlayer(player)

            # Add moves to database
            self.db.addMoves(self.moves)

            logger.info(f"Game {self.game.id} ended successfully")

        except Exception as e:
            # Log error but don't crash the game server
            logger = logging.getLogger(__name__)
            logger.error(f"Error ending game {self.game.id}: {e}")

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
            winners = [p for p in self.playersList if p.status == PlayerStatus.Won]
            if winners:
                winner = winners[0]
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
