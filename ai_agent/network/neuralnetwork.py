import os
import logging
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
import random

logger = logging.getLogger(__name__)

# Hyperparameters
gamma = 0.95  # Discount factor
alpha = 0.001  # Learning rate
epsilon = 1.0  # Exploration-exploitation trade-off
epsilon_min = 0.01
epsilon_decay = 0.995
batch_size = 64
# num_actions = 1000  # Number of possible moves # Removed global num_actions
# input_shape = (100, 100, 1) # Removed global input_shape

# Reward system
REWARD = {
    'INCORRECT': -1.0,  # Negative reward for incorrect moves
    'LOST': -1.0,       # Negative reward for losing
    'MOVED': 0.0,       # No reward for a regular move
    'DRAW': 0.5,        # Positive reward for a draw
    'WON': 1.0,         # Positive reward for winning
}

class NeuralNetwork:

    def __init__(self, agentName, board_height, board_width, num_actions, num_channels=1):
        self.model_file = 'data/models/' + agentName + '.keras'
        self.board_height = board_height
        self.board_width = board_width
        self.num_channels = num_channels
        self.input_shape = (self.board_height, self.board_width, self.num_channels)
        self.num_actions = num_actions
        self.loadModel()

    def loadModel(self):
        if os.path.exists(self.model_file):
            logger.info("Loading existing NN model from the disk.")
            # When loading a model, Keras automatically handles the architecture,
            # including input shape. We might need custom objects if we have custom layers/activations.
            # For now, direct loading should work.
            self.model = load_model(self.model_file)
            # Verify input shape compatibility if possible, or ensure saving/loading handles it.
            # Keras model saving includes the architecture, so build_model() isn't typically called here
            # unless the model needs to be recreated with potentially different parameters not stored in the file.
            # However, if the loaded model's input shape is different from the current config,
            # it might indicate an issue or a need to rebuild.
            # For this task, we assume the loaded model is compatible or will be overwritten
            # if incompatible by the logic: if a model exists, load it, else build it.
        else:
            logger.info(f"No model found at {self.model_file}. Building a new model.")
            self.model = self.build_model()
            self.save()

    def save(self):
        self.model.save(self.model_file)

    def build_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        model.add(tf.keras.layers.GlobalAveragePooling2D()) # Added GlobalAveragePooling2D
        # model.add(tf.keras.layers.Flatten()) # Removed Flatten
        model.add(tf.keras.layers.Dense(128, activation='relu'))
        model.add(tf.keras.layers.Dense(self.num_actions, activation='linear'))  # Outputs Q-values
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=alpha), loss='mse')
        return model

    def predict(self, state):
        # Ensure state has a batch dimension for Keras model
        if state.ndim == 3: # Assuming state is (H, W, C)
            state = np.expand_dims(state, axis=0) # Shape becomes (1, H, W, C)
        return self.model.predict(state)

    def train(self, state, target):
        # Ensure state and target have a batch dimension for Keras model
        # state is expected to be (1, H, W, C) and target (1, num_actions) by DQNAgent.replay
        self.model.fit(state, target, epochs=1, verbose=0)

class ReplayBuffer:
    def __init__(self, max_size):
        self.buffer = []
        self.max_size = max_size
    
    def add(self, experience):
        if len(self.buffer) >= self.max_size:
            self.buffer.pop(0)
        self.buffer.append(experience)
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)


class DQNAgent:
    def __init__(self, nn: NeuralNetwork):
        self.model = nn.model
        self.target_model = nn.model # Consider if target_model should also be built with dynamic num_actions
        self.num_actions = nn.num_actions # Derive num_actions from NeuralNetwork instance
        self.replay_buffer = ReplayBuffer(max_size=2000)
        self.epsilon = epsilon
        
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(0, self.num_actions)  # Random move (exploration)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])  # Best move (exploitation)
    
    def remember(self, state, action, reward, next_state, done):
        self.replay_buffer.add((state, action, reward, next_state, done))

    def replay(self):
        if len(self.replay_buffer.buffer) < batch_size:
            return
        
        minibatch = self.replay_buffer.sample(batch_size)
        
        states = []
        next_states = []
        for s, a, r, ns, d in minibatch:
            states.append(s)
            next_states.append(ns)
        
        states_batch = np.array(states) # Shape (batch_size, H, W, C) assuming states are stored correctly
        next_states_batch = np.array(next_states) # Shape (batch_size, H, W, C)

        # If states/next_states in replay buffer are single samples (H,W,C)
        # and model.predict expects (N,H,W,C), we might need to stack them or predict one by one.
        # The current NeuralNetwork.predict handles individual (H,W,C) states by adding a batch dim.
        # However, for replaying, it's more efficient to predict in a batch.
        # Let's assume states and next_states from buffer are individual (H,W,C) for now.
        # Keras predict/fit can typically handle a list of numpy arrays for batching,
        # but it's better to explicitly form a numpy batch.

        # The loop processes one experience at a time, which is less efficient for batch processing with NNs.
        # A more common pattern is to batch states and next_states, get predictions in batches,
        # then update targets and fit in a batch.
        # Given the current structure (looping one by one):
        for i, (state, action, reward, next_state, done) in enumerate(minibatch):
            # Ensure state and next_state have batch dimension for Keras model methods
            if state.ndim == 3: # Assuming state from buffer is (H, W, C)
                state_batch = np.expand_dims(state, axis=0)
            else: # Assuming state is already correctly batched e.g. (1, H, W, C) or (N, H, W, C)
                state_batch = state
            
            if next_state.ndim == 3: # Assuming next_state from buffer is (H, W, C)
                next_state_batch = np.expand_dims(next_state, axis=0)
            else: # Assuming next_state is already correctly batched
                next_state_batch = next_state

            target = reward
            if not done:
                next_q_values = self.target_model.predict(next_state_batch) 
                target = reward + gamma * np.amax(next_q_values[0])
            
            current_q_values = self.model.predict(state_batch) 
            current_q_values[0][action] = target  # Update the Q-value for the chosen action
            
            self.model.fit(state_batch, current_q_values, epochs=1, verbose=0)

        # Decay epsilon (less random exploration over time)
        if self.epsilon > epsilon_min:
            self.epsilon *= epsilon_decay

    def update_target_network(self):
        self.target_model.set_weights(self.model.get_weights())
