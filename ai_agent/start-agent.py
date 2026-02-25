#!python
import sys
import os
import logging

# Disable Tensorflow logging (warnings and info)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Set the working directory to the root of the project
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
os.chdir(root_dir)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s-> %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Check for GPU availability
import tensorflow as tf

# Suppress some warnings
tf.get_logger().setLevel(logging.ERROR)

print("TensorFlow version:", tf.__version__)
print("Built with CUDA:", tf.test.is_built_with_cuda())

try:
    # List physical devices
    gpus = tf.config.list_physical_devices('GPU')
    print("GPU Available:", gpus)

    if gpus:
        print("Using GPU for computation")
        try:
            # Enable memory growth for each GPU
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"Enabled memory growth for {len(gpus)} GPU(s)")

            # Print GPU details
            for gpu in gpus:
                details = tf.config.experimental.get_device_details(gpu)
                print(f"GPU details: {details}")
        except RuntimeError as e:
            print(f"GPU memory growth configuration error: {e}")
    else:
        print("Using CPU for computation")
        cpus = tf.config.list_physical_devices('CPU')
        print(f"Available CPUs: {len(cpus)}")
except Exception as e:
    print(f"Error checking GPU availability: {e}")
    print("Defaulting to CPU computation")

from ai_agent.gamerunner import GameRunner

agentName = None
if (len(sys.argv) > 1 and sys.argv[1]):
    agentName = sys.argv[1]
elif os.environ.get('PLAYER_NAME'):
    agentName = os.environ.get('PLAYER_NAME')
else:
    agentName = 'AI_Agent'

game = GameRunner('localhost', 8080, agentName)
game.start()