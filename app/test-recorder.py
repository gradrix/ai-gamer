#!python
from recorder.recorderdb import RecorderDb
from models.game import Game
from models.move import Move

rec = RecorderDb()
c = Game( 1, 5, 123, "aa")
m = Move(44, 35, 0, 'EF->BG', 20220816004326999)
#rec.addGame(c)
rec.addMove(m)