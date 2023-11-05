#!python
import sys
import os
import logging

# Set the working directory to the root of the project
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
os.chdir(root_dir)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s-> %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

from ai_agent.gamerunner import GameRunner

if len(sys.argv) < 2:
    logger.error("Usage: python agent.py [Agent Name]")
    sys.exit(1)

agentName = sys.argv[1]
game = GameRunner('localhost', 8080, agentName)
game.start()