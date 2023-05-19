#!python
import sys
import os

# Set the working directory to the root of the project
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
os.chdir(root_dir)

from random_client.gameclient import GameClient

if len(sys.argv) < 2:
    print("Usage: python start-random-client.py [Agent Name]")
    sys.exit(1)

agentName = sys.argv[1]
client = GameClient('localhost', 8080, agentName)
client.start()