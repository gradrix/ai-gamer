#!python
import sys
from random_client.gameclient import GameClient

if len(sys.argv) < 2:
    print("Usage: python start-random-client.py [Agent Name]")
    sys.exit(1)

agentName = sys.argv[1]
client = GameClient('localhost', 8080, agentName)
client.start()