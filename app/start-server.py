#!python
from game_server.gameengine import GameEngine
from game_server.games.ticktaktoe import TikTakToe
from models.enums import Mode

engine = GameEngine(Mode.Rpc, TikTakToe(3, 3, 3))
engine.start()