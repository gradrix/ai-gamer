import os
import time
import threading
from common.cordhelpers import parse_coordinate

from common.rpc.rpcclient import GameEngineRpcClient
from common.models.enums import PlayerStatus, MoveStatus, PlayerRegistration

class ConsoleClient:

    def __init__(self, host, port, agentName = 'Console'):
        self.client = GameEngineRpcClient(host, port)
        self.playerId = agentName
        self.__initKeepAliveRequestor()
        self.__register()

    def start(self):
        while True:
            canMove = self.client.canMove(self.playerId)
            match canMove:
                case PlayerStatus.UnregisteredPlayer:
                    self.__register()
                case PlayerStatus.Won:
                    self.__gameEnded('I\'ve won!')
                    time.sleep(3)
                case PlayerStatus.Lost:
                    self.__gameEnded('I\'ve lost :-/')
                    time.sleep(3)
                case PlayerStatus.Draw:
                    self.__gameEnded('It\'s a draw..')
                    time.sleep(3)
                case PlayerStatus.CanMove:
                    self.__makeSomeMove()
                case PlayerStatus.Wait:
                    os.system("clear")
                    self.__printGrid()
                    print("Waiting for oponent's move..")
                    time.sleep(0.5)

    def __makeSomeMove(self):
        possibleMoves = self.client.getPossibleMoves()
        moveResult = None
        while (moveResult != MoveStatus.Error and moveResult != MoveStatus.Success):
            self.__printGrid()
            coordinate = input("Enter your move coordinate: ")
            os.system("clear")
            (x, y) = parse_coordinate(coordinate)
            moveStr = str(coordinate) + " ("+str(x)+","+str(y)+")"
            if (x, y) not in possibleMoves:
                print(moveStr+" is not a valid move!")
            else:
                moveIndex = possibleMoves.index((x, y))
                moveResult = self.client.move(self.playerId, moveIndex).status
                if (moveResult == moveResult.Incorrect):
                    print(moveStr+" is incorrect move!")
                elif (moveResult == moveResult.Error):
                    print("There was an error when moving to " +moveStr)


    def __printGrid(self):
        grid = self.client.getCurrentBoard()
        rows = len(grid)
        cols = len(grid[0])

        # Print column headers (x-axis)
        column_labels = [chr(65 + i) for i in range(cols)]
        column_header = "     " + " ".join(label.ljust(2) for label in column_labels)
        print(column_header+'\n')

        # Print table
        for i in range(rows):
            # Print row number (y-axis)
            print(str(i + 1).rjust(2) + "  ", end="")
            # Print row values
            for j in range(cols):
                print(str(grid[i][j]).rjust(2) + " ", end="")
            # Print row number (y-axis)
            print("  " + str(i + 1).rjust(2), end="")

            print()  # Move to the next line

        print('\n' + column_header)

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

    def __initKeepAliveRequestor(self):
        thread = threading.Thread(target=self.__keepAliveRequestor, args=())
        thread.daemon = True
        thread.start()

    def __keepAliveRequestor(self):
        while True:
            self.client.keepAlive(self.playerId)
            time.sleep(2)

    def __gameEnded(self, message):
        print(str(message) + '. Waiting for the game to be started again..')
        time.sleep(0.1)
