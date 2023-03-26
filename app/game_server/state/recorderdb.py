import sqlite3
from sqlite3 import Error
import pathlib

from models.game import Game
from models.move import Move
from models.player import Player
from models.enums import GameStatus
from common.timehelpers import currentTimestamp

RECORDER_DB = 'game_records.db'

class RecorderDb:

    conn = None

    def __init__(self):
        try:
            self.conn = sqlite3.connect(RECORDER_DB, check_same_thread=False)
            self.__create_tables()
        except Error as e:
            print(e)
            raise e

    def __del__(self):
        if (self.conn):
            self.conn.close()

    def getPlayer(self, playerName):
        sql = ''' SELECT * FROM players
                WHERE name = ? '''
        db = self.conn.cursor()
        try:
            db.execute(sql, (playerName,))
            result = db.fetchone()
            if (result == None):
                return None
            return Player(int(result[0]), str(result[1]), int(result[2]), int(result[3]))
        except Error as e:
            print("RecorderDb: Unable to get User: "+str(e))
            return -1
        finally:
            db.close()
        

    def createPlayer(self, playerName):
        sql = ''' INSERT INTO players(name,createddate,lastonline)
                VALUES(?,?,?) '''
        db = self.conn.cursor()
        try:
            time = currentTimestamp()
            db.execute(sql, (playerName, time, time))
            self.conn.commit()
            return Player(int(db.lastrowid), playerName, time, time)
        except Error as e:
            print("RecorderDb: Unable to add User: "+str(e))
            return -1
        finally:
            db.close()

    def updatePlayer(self, player):
        sql = ''' UPDATE players
                SET lastonline = (?)
                WHERE id = ?'''
        db = self.conn.cursor()
        try:
            db.execute(sql, (currentTimestamp(), player.id))
            self.conn.commit()
            return player
        except Error as e:
            print("RecorderDb: Unable to update Player: "+str(e))
            return -1
        finally:
            db.close()      


    def createGame(self, retries = 10):
        sql = ''' INSERT INTO games(date,status)
                VALUES(?,?) '''
        db = self.conn.cursor()
        for attempt in range(retries):
            try:
                time = currentTimestamp()
                db.execute(sql, (time,int(GameStatus.Started)))
                self.conn.commit()
                return Game(db.lastrowid, {}, time, GameStatus.Started)
            except Error as e:
                if "transaction" in str(e) and attempt < retries - 1:
                    # Transaction error: rollback and retry
                    self.conn.rollback()
                    time.sleep(0.1)
                    continue
                else:
                    # Other error or out of retries: give up
                    print("RecorderDb: Unable to add Game: "+str(e))
                    return -1
            finally:
                db.close()

    def updateGame(self, game: Game):
        sql = ''' UPDATE games
                SET  (status)
                        = (?) 
                WHERE id = ? '''
        db = self.conn.cursor()
        try:
            db.execute(sql, (game.status, game.id))
            self.conn.commit()
            return game
        except Error as e:
            print("RecorderDb: Unable to update Game: "+str(e))
            return -1
        finally:
            db.close()

    def addMoves(self, moves: list[Move]):
        data = []
        for idx, move in enumerate(moves):
            data.append((move.gameid, move.playerid, idx, move.move, move.date))
        sql = ''' INSERT INTO moves(gameid,playerid,idx,move,date)
                VALUES(?,?,?,?,?) '''
        db = self.conn.cursor()
        try:
            db.executemany(sql, data)
            self.conn.commit()
            return True
        except Error as e:
            print("RecorderDb: Unable to add Moves: "+str(e))
            return -1
        finally:
            db.close()

    def addMove(self, move: Move):
        sql = ''' INSERT INTO moves(gameid,playerid,idx,move,date)
                VALUES(?,?,?,?,?) '''
        db = self.conn.cursor()
        try:
            db.execute(sql, (move.gameid, move.playerid, move.idx, move.move, self.__currentTime()))
            self.conn.commit()
            return db.lastrowid
        except Error as e:
            print("RecorderDb: Unable to add Move: "+str(e))
            return -1
        finally:
            db.close()

    def __create_tables(self):
        sqlFile = open(str(pathlib.Path().resolve())+'/game_server/state/game_records_schema.sql')
        db = self.conn.cursor()
        try:
            sql = sqlFile.read()
            db.executescript(sql)
        except Error as e:
            print(e)
            raise e
        finally:
            sqlFile.close()
            db.close()
            