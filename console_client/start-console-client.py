#!python
import sys
import os

# Set the working directory to the root of the project
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
os.chdir(root_dir)

from console_client.consoleclient import ConsoleClient

agentName = None
if len(sys.argv) > 1:
    agentName = sys.argv[1]

client = ConsoleClient('localhost', 8080, agentName)
client.start()