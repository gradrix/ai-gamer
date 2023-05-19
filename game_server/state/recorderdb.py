import sqlite3
from sqlite3 import Error
import pathlib
import threading

from common.models.game import Game
from common.models.move import Move
from common.models.player import Player
from common.models.enums import GameStatus
from common.timehelpers import currentTimestamp

RECORDER_DB = 'db/game_records.db'

class RecorderDb:

    conn = None

    def __init__(self):
        try:
            self.conn = sqlite3.connect(RECORDER_DB, check_same_thread=False)
            self.lock = threading.Lock()
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
        try:
            db = self.conn.cursor()
            db.execute(sql, (playerName,))
            result = db.fetchone()
            if (result == None):
                return None
            return Player(int(result[0]), str(result[1]), int(result[2]), int(result[3]))
        except Error as e:
            print("RecorderDb: Unable to get User: "+str(e))
            return -1
        

    def createPlayer(self, playerName):
        timestamp = currentTimestamp()
        sql = ''' INSERT INTO players(name,createddate,lastonline)
                VALUES(?,?,?) '''
        try:
            with self.lock:
                db = self.conn.cursor()
                db.execute(sql, (playerName, timestamp, timestamp))
                self.conn.commit()
                return Player(int(db.lastrowid), playerName, timestamp, timestamp)
        except Error as e:
            print("RecorderDb: Unable to add User: "+str(e))
            return -1

    def updatePlayer(self, player):
        sql = ''' UPDATE players
                SET lastonline = (?)
                WHERE id = ?'''
        try:
            with self.lock:
                db = self.conn.cursor()
                db.execute(sql, (currentTimestamp(), player.id))
                self.conn.commit()
                return player
        except Error as e:
            print("RecorderDb: Unable to update Player: "+str(e))
            return -1

    def createGame(self, retries = 10):
        timestamp = currentTimestamp()
        sql = ''' INSERT INTO games(date,status)
                VALUES(?,?) '''
        for attempt in range(retries):
            try:
                with self.lock:
                    db = self.conn.cursor()
                    db.execute(sql, (timestamp, int(GameStatus.Started)))
                    self.conn.commit()
                    return Game(db.lastrowid, {}, timestamp, GameStatus.Started)
            except Error as e:
                if "transaction" in str(e) and attempt < retries - 1:
                    # Transaction error: rollback and retry
                    self.conn.rollback()
                    continue
                else:
                    # Other error or out of retries: give up
                    print("RecorderDb: Unable to add Game: "+str(e))
                    return -1

    def updateGame(self, game: Game):
        sql = ''' UPDATE games
                SET  (status)
                        = (?) 
                WHERE id = ? '''
        try:
            with self.lock:
                db = self.conn.cursor()
                db.execute(sql, (game.status, game.id))
                self.conn.commit()
                return game
        except Error as e:
            print("RecorderDb: Unable to update Game: "+str(e))
            return -1

    def addMoves(self, moves: list[Move]):
        data = []
        for idx, move in enumerate(moves):
            data.append((move.gameid, move.playerid, idx, move.move, move.date))
        sql = ''' INSERT INTO moves(gameid,playerid,idx,move,date)
                VALUES(?,?,?,?,?) '''
        try:
            with self.lock:
                db = self.conn.cursor()
                db.executemany(sql, data)
                self.conn.commit()
                return True
        except Error as e:
            print("RecorderDb: Unable to add Moves: "+str(e))
            return -1

    def addMove(self, move: Move):
        sql = ''' INSERT INTO moves(gameid,playerid,idx,move,date)
                VALUES(?,?,?,?,?) '''
        try:
            with self.lock:
                db = self.conn.cursor()
                db.execute(sql, (move.gameid, move.playerid, move.idx, move.move, self.__currentTime()))
                self.conn.commit()
                return db.lastrowid
        except Error as e:
            print("RecorderDb: Unable to add Move: "+str(e))
            return -1

    def __create_tables(self):
        sqlFile = open(str(pathlib.Path().resolve())+'/game_server/state/game_records_schema.sql')
        try:
            sql = sqlFile.read()
            db = self.conn.cursor()
            db.executescript(sql)
        except Error as e:
            print(e)
            raise e
        finally:
            sqlFile.close()
            