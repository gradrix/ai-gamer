import time

from models.enums import PlayerStatus, MoveStatus

class ConsoleController:

    def __init__(self, game, mode):        
        self.game = game
        if (mode == Mode.Mixed):
            self.cmdPlayers = 1
        else:
            self.cmdPlayers = 2
        self.players = []

    def start(self):
        self.__registerAll()
        alreadyEnded = []
        for i in range (0, self.cmdPlayers):
            alreadyEnded.append(False)

        while True:
            for i in range(0, self.cmdPlayers):
                player = self.players[i]
                match self.game.canMove(player):
                    case PlayerStatus.UnregisteredPlayer:
                        alreadyEnded[i] = False
                        self.__register(i)
                    case PlayerStatus.Draw if alreadyEnded[i] == False:
                        print('Game has ended because it is Draw!')
                        alreadyEnded[i] = True
                    case PlayerStatus.Lost if alreadyEnded[i] == False:
                        print('Game has ended. Player #'+str(i + 1)+' ('+str(player)+') lost.. :-/')
                        alreadyEnded[i] = True
                    case PlayerStatus.Won if alreadyEnded[i] == False:
                        print('Game has ended. Player #'+str(i + 1)+' ('+str(player)+') won! :-)')
                        alreadyEnded[i] = True
                    case PlayerStatus.CanMove:
                        alreadyEnded[1] = False
                        board = self.game.getCurrentBoardString()
                        possibleMoves = self.game.getPossibleMoves()
                        maxX = 0
                        maxY = 0
                        for mov in possibleMoves:
                            maxX = max(maxX, mov[0])
                            maxY = max(maxY, mov[1])

                        print('Current situation:')
                        print(board)
                        print(str(self.players[i]) + ', perform your move!')
                        x = None
                        y = None
                        while True:
                            xEntered = False
                            while (xEntered == False):
                                inputStr = input('Enter X, possible values: 0 - '+str(maxX)+ ' : ')
                                x = self.__tryGetCoordinate(inputStr)
                                if (x != None):
                                    xEntered = True
                            yEntered = False
                            while (yEntered == False):
                                inputStr = input('Enter Y, possible values: 0 - '+str(maxY)+ ' : ') 
                                yEntered = True
                                y = self.__tryGetCoordinate(inputStr)
                                if (y != None):
                                    yEntered = True
                            moveResult = self.game.move(player, (x, y))
                            if (moveResult == Move.Incorrect):
                                print('Incorrect move, please retry!')
                            else:
                                break
                    case _:
                        time.sleep(0.5)


    def __registerAll(self):
        for i in range(0, self.cmdPlayers):
            self.__register(i)

    def __register(self, index):
        print('Registering player #'+str(index + 1)+'.')
        name = input("Enter player #"+str(index + 1)+ ' name: ')
        if (index in self.players):
            self.players.pop(index)

        self.players.append(name)
        self.game.registerPlayer(name)

    def __tryGetCoordinate(self, value):
        try:
            result = int(value)
            return result
        except:
            print('Incorrect integer value!')
            return None