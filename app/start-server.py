#!python
from game_server.gameserver import GameServer
from game_server.games.ticktaktoe import TikTakToe

GameServer(TikTakToe(10, 10, 5))
#GameServer(TikTakToe(3, 3, 3))