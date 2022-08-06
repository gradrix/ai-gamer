#!python
from ai_client.gameclient import GameClient

client = GameClient('localhost', 8080)
client.start()