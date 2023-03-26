#!python
from game_server.gameserver import GameServer
from game_server.games.ticktaktoe import TikTakToe

server = GameServer(TikTakToe(10, 10, 5))
server.start()