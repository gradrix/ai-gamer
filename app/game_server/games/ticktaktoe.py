from array import array
import random

from models.gamebase import GameBase
from models.enums import GameStatus, PlayerRegistration, Move
from models.player import Player

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
        self.reset()

    #GameBase implementation
    def reset(self):
        self.players = {
            X: Player(None, GameStatus.CanMove),
            O: Player(None, GameStatus.Wait)
        }
        self.startNewGame()

    def startNewGame(self):
        self.grid = []
        for y in range(0, self.ySize):
            self.grid.insert(y, [])
            for x in range(0, self.xSize):
                self.grid[y].insert(x, E)

        self.nextToMove = X

        #Randomly change figure for player after each game
        if (bool(random.getrandbits(1))):
            print('Switching figures!')
            xId = self.players[X].id
            self.players[X].id = self.players[O].id
            self.players[O].id = xId

        self.hasEnded = False
        self.players[X].status = GameStatus.CanMove
        self.players[O].status = GameStatus.Wait

    def registerPlayer(self, playerId):
        if (self.players[X].id != None and self.players[O].id != None):
            return PlayerRegistration.NoPlayerSlotsLeft
        elif (self.players[X].id == playerId or self.players[O].id == playerId):
            return PlayerRegistration.AlreadyRegistered
        else:
            if (self.players[X].id == None and self.players[O].id == None):
                randomIdx = random.randint(0, 1)
                if (randomIdx == 0):
                    self.players[O].id = playerId
                else:
                    self.players[X].id = playerId
            elif (self.players[O].id == None):
                self.players[O].id = playerId
            else:
                self.players[X].id = playerId
            return PlayerRegistration.Success

    def getPossibleMoves(self) -> array:
        moves = []
        for y in range(0, self.ySize):
            for x in range(0, self.xSize):
                moves.append((x, y))
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

    def canMove(self, playerId) -> GameStatus:
        playerFigure = self.__getPlayerFigureById(playerId)
        gameStatus = self.checkForWinner()
        if (playerFigure == None):
            return GameStatus.UnregisteredPlayer
        elif (gameStatus == False):
            if (self.stillCouldHaveWinner == False):
                return self.__endGame(playerId, GameStatus.Draw)
            elif (self.nextToMove != playerFigure):
                return GameStatus.Wait
            else:
                return GameStatus.CanMove
        elif (gameStatus == playerFigure):
            return self.__endGame(playerId, GameStatus.Won)
        else:
            return self.__endGame(playerId, GameStatus.Lost)

    def move(self, playerId, index) -> Move:
        playerFigure = self.__getPlayerFigureById(playerId)

        if (self.hasEnded or playerFigure == None or self.nextToMove != playerFigure):
            return Move.Error
        else:
            possibleMoves = self.getPossibleMoves()
            (x, y) = possibleMoves[index]
            if (self.placeFigure(x, y, playerFigure)):
                if (playerFigure == X):
                    self.nextToMove = O
                else:
                    self.nextToMove = X
                return Move.Success
            else:
                return Move.Incorrect

    def getPlayerStatuses(self) -> array:
        result = []
        for player in self.players.values():
            result.append(player.status)
        return result
    #end

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

    def __endGame(self, playerId, endStatus):
        playerFigure = self.__getPlayerFigureById(playerId)
        self.hasEnded = True        
        self.players[playerFigure].status = endStatus
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

    def __getPlayerFigureById(self, playerId):
        figureMap = list(self.players.keys())
        for i, player in enumerate(self.players.values()):
            if (player.id == playerId):
                return figureMap[i]
        return None
