#!python
from game_server.gamemanager import GameManager
from game_server.games.ticktaktoe import TikTakToe
from models.enums import Mode

engine = GameManager(Mode.Mixed, TikTakToe(3, 3, 3))
engine.start()