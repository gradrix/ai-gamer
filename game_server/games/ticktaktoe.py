from array import array
import random
import time

from common.models.gamebase import GameBase
from common.models.enums import PlayerStatus, MoveStatus
from common.models.player import Player
from common.models.game import MoveResult

E = 0 #Empty
X = 1 #X
O = 2 #O

class TikTakToe(GameBase):
    def __init__(self, xSize, ySize, scoreLineLength):
        self.xSize = xSize
        self.ySize = ySize
        self.scoreLineLength = scoreLineLength
        if (min(xSize, ySize) < scoreLineLength):
            raise Exception('Error: scoreLineLength of '+str(scoreLineLength)+ ' is bigger than width ('+str(xSize)+ ') or '+
            'height ('+str(ySize)+') and therefore it is not possible to reach winning condition')
        self.previousWinner = None
        self.player1: Player = None
        self.player2: Player = None
        self.hasEnded = True
        self.__reset()

    #GameBase implementation
    requiredNumOfPlayers: int = 2

    def startNewGame(self, players: list[Player]):
        self.__reset()
        self.syncPlayers(players)
    
        if (self.player1.id == self.previousWinner):
            self.__assignPlayerFigures(True)
        elif (self.player2.id == self.previousWinner):
            self.__assignPlayerFigures(False)
        else:
            self.__assignPlayerFigures(bool(random.getrandbits(1)))

        self.hasEnded = False
        self.player1.status = PlayerStatus.CanMove
        self.player2.status = PlayerStatus.Wait
        return True

    def getPossibleMoves(self) -> array:
        moves = []
        for y in range(0, self.ySize):
            for x in range(0, self.xSize):
                moves.append([x, y])
        return moves

    def getCurrentBoard(self) -> array:
        return self.grid
    
    def getCurrentBoardString(self) -> str:
        result = ''
        for y in range(0, self.ySize):
            line = ''
            for x in range(0, self.xSize):
                value = self.grid[y][x]
                if (value == X):
                    line += 'x|'
                elif (value == O):
                    line += 'o|'
                else:
                    line += ' |'
            result += line[:-1] + '\n'
        return result

    def canMove(self, playerName) -> PlayerStatus:
        playerFigure = self.__getPlayerFigureByName(playerName)
        playerStatus = self.checkForWinner()
        player = self.__getPlayerByName(playerName)

        if (playerFigure == None):
            if (self.hasEnded == True and player != None):
                return PlayerStatus.Wait
            else:
                return PlayerStatus.UnregisteredPlayer
        elif (playerStatus == False):
            if (self.stillCouldHaveWinner == False):
                return self.__endGame(player, PlayerStatus.Draw)
            elif (self.nextToMove != playerFigure):
                return PlayerStatus.Wait
            else:
                return PlayerStatus.CanMove
        elif (playerStatus == playerFigure):
            return self.__endGame(player, PlayerStatus.Won)
        else:
            return self.__endGame(player, PlayerStatus.Lost)

    def move(self, playerName, index):
        playerFigure = self.__getPlayerFigureByName(playerName)

        if (self.hasEnded or playerFigure == None or self.nextToMove != playerFigure):
            return MoveResult(MoveStatus.Error, None)
        else:
            possibleMoves = self.getPossibleMoves()
            (x, y) = possibleMoves[index]
            if (self.placeFigure(x, y, playerFigure)):
                if (playerFigure == X):
                    symbol = 'X'
                    self.nextToMove = O
                else:
                    symbol = 'O'
                    self.nextToMove = X
                moveStr = symbol + ' -> X:' +str(x)+ ',Y:'+str(y)
                return MoveResult(MoveStatus.Success, moveStr)
            else:
                return MoveResult(MoveStatus.Incorrect, None)
            
    def syncPlayers(self, players: list[Player]):
        def getPlayer(player: Player):
            return  (None, None) if player is None else (player.refid, player.name)

        def syncFigure(oponentsName: str, newName: str):
            figure = self.__getPlayerFigureByName(oponentsName)
            if (figure != None):
                isX = True if figure is X else False
                if (isX): 
                    self.figureMap[O] = newName
                else:
                    self.figureMap[X] = newName

        (pl1Ref, pl1Name) = getPlayer(players[0])
        (pl2Ref, pl2Name) =  getPlayer(players[1])
        (existing1Ref, existing1Name) = getPlayer(self.player1)
        (existing2Ref, existing2Name) = getPlayer(self.player2)

        #swap if needed
        if ((pl1Ref != None and pl1Ref == existing2Ref) or 
                (pl2Ref != None and pl2Ref == existing1Ref)):
            player1 = self.player1
            self.player1 = self.player2
            self.player2 = player1

        if (pl1Ref != None and pl1Ref != existing1Ref):
            self.player1 = players[0]
            syncFigure(existing2Name, pl1Name)

        if (pl2Ref != None and pl2Ref != existing2Ref):
            self.player2 = players[1]
            syncFigure(existing1Name, pl2Name)
    #end

    def getPl(self, players: list[Player], refId: str):
        maybePlayer = [player for player in players if player.refid == refId]
        return maybePlayer[0] if maybePlayer else None

    def placeFigure(self, x, y, figure) -> bool:
        if ((x < 0 or x > self.xSize - 1 or y < 0 or y > self.ySize - 1) or
            (figure != X and figure != O)):
            return False
        
        canPlaceFigure = self.grid[y][x] == E
        if (canPlaceFigure):
            self.grid[y][x] = figure
        return canPlaceFigure

    def checkForWinner(self):
        self.stillCouldHaveWinner = False
        score = { 
            X: 0,
            O: 0,
            E: 0,
            "prev": None
        }

        #check vertically
        for x in range(0, self.xSize):
            self.__clearAllScores(score)  
            for y in range(0, self.ySize):  
                winner = self.__calculateScore(score, self.grid[y][x])
                if (winner != None):
                    return winner

        #check horizontally
        for y in range(0, self.ySize):  
            self.__clearAllScores(score)  
            for x in range(0, self.xSize):
                winner = self.__calculateScore(score, self.grid[y][x])
                if (winner != None):
                    return winner

        #check diagonally (bottom left -> top right)
        xStart = 0
        yStart = self.ySize - 1
        while(xStart < self.xSize):            
            self.__clearAllScores(score)  
            x = xStart
            y = yStart
            while (y < self.ySize and x < self.xSize):             
                winner = self.__calculateScore(score, self.grid[y][x])
                if (winner != None):
                    return winner
                x += 1
                y += 1
            if (yStart > 0):
                yStart -= 1
            elif (yStart == 0):
                xStart += 1

        #check diagonally (bottom left -> top right)
        yStart = 0
        xStart = 0
        while(yStart < self.ySize):       
            self.__clearAllScores(score)  
            x = xStart
            y = yStart
            while (y >= 0 and x < self.xSize):   
                winner = self.__calculateScore(score, self.grid[y][x])
                if (winner != None):
                    return winner
                x += 1
                y -= 1
            if (yStart < self.ySize):
                yStart += 1
            elif (yStart == self.ySize - 1):
                xStart += 1

        return False

    def __reset(self):
        self.figureMap = {
            X: None,
            O: None
        }
        self.grid = []
        for y in range(0, self.ySize):
            self.grid.insert(y, [])
            for x in range(0, self.xSize):
                self.grid[y].insert(x, E)
        self.nextToMove = X

    def __endGame(self, player: Player, endStatus: PlayerStatus):
        self.hasEnded = True        
        player.status = endStatus
        return endStatus

    def __clearAllScores(self, score):
        score[X] = 0
        score[O] = 0
        score[E] = 0

    def __clearOponentScore(self, score, playerFigure):
        if (playerFigure == X and score[O] > 0):
            score[O] = 0
            score[E] = 0
        elif (playerFigure == O and score[X] > 0):
            score[X] = 0
            score[E] = 0

    def __calculateScore(self, score, newFigure):
        prevFigure = score["prev"]
        score[newFigure] += 1

        if (prevFigure != newFigure):
            self.__clearOponentScore(score, newFigure)

        if (newFigure != E and score[newFigure] >= self.scoreLineLength):
            return newFigure
        elif ((prevFigure != None and score[prevFigure] + score[E] >= self.scoreLineLength)
                or (score[newFigure] + score[E] >= self.scoreLineLength)):
            self.stillCouldHaveWinner = True

        score["prev"] = newFigure
        return None

    def __assignPlayerFigures(self, player1IsFirst: bool):
        if (player1IsFirst):
            self.figureMap[X] = self.player1.name
            self.figureMap[O] = self.player2.name
        else:
            self.figureMap[X] = self.player1.name
            self.figureMap[O] = self.player2.name

    #TODO: move outside
    def __getPlayerByName(self, playerName: str):
        if (self.player1 != None and self.player1.name == playerName):
            return self.player1
        elif (self.player2 != None and self.player2.name == playerName):
            return self.player2
        else:
            return None

    def __getPlayerFigureByName(self, playerName: str):
        figures = list(self.figureMap.keys())
        for i, figPlayerName in enumerate(self.figureMap.values()):
            if (figPlayerName == playerName):
                return figures[i]
        return None
