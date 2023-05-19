#!python

import os
import sys

# Set the working directory to the root of the project
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
os.chdir(root_dir)

from gameserver import GameServer
from games.ticktaktoe import TikTakToe

GameServer(TikTakToe(10, 10, 5))
#GameServer(TikTakToe(3, 3, 3))