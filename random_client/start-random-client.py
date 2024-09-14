#!python
import sys
import os

# Set the working directory to the root of the project
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
os.chdir(root_dir)

from random_client.gameclient import GameClient

agentName = None
if (len(sys.argv) > 1 and sys.argv[1]):
    agentName = sys.argv[1]
else:
    agentName = 'RandomClient'

client = GameClient('localhost', 8080, agentName)
client.start()