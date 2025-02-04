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
num_actions = 1000  # Number of possible moves
input_shape = (100, 100, 1)

# Reward system
REWARD = {
    'INCORRECT': -1.0,  # Negative reward for incorrect moves
    'LOST': -1.0,       # Negative reward for losing
    'MOVED': 0.0,       # No reward for a regular move
    'DRAW': 0.5,        # Positive reward for a draw
    'WON': 1.0,         # Positive reward for winning
}

class NeuralNetwork:

    def __init__(self, agentName):
        self.model_file = 'data/models/' +agentName + '.keras'
        self.loadModel()

    def loadModel(self):
        if os.path.exists(self.model_file):
            logger.info("Loading existing NN model from the disk.")
            self.model = load_model(self.model_file)
        else:
            self.model = self.build_model()
            self.save()

    def save(self):
        self.model.save(self.model_file)

    def build_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(128, activation='relu'))
        model.add(tf.keras.layers.Dense(num_actions, activation='linear'))  # Outputs Q-values
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=alpha), loss='mse')
        return model

    def predict(self, state):
        return self.model.predict(state)

    def train(self, state, target):
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
        self.target_model = nn.model
        self.replay_buffer = ReplayBuffer(max_size=2000)
        self.epsilon = epsilon
        
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(0, num_actions)  # Random move (exploration)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])  # Best move (exploitation)
    
    def remember(self, state, action, reward, next_state, done):
        self.replay_buffer.add((state, action, reward, next_state, done))

    def replay(self):
        if len(self.replay_buffer.buffer) < batch_size:
            return
        
        minibatch = self.replay_buffer.sample(batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + gamma * np.amax(self.target_model.predict(next_state)[0])
            
            q_values = self.model.predict(state)
            q_values[0][action] = target  # Update the Q-value for the chosen action
            
            self.model.fit(state, q_values, epochs=1, verbose=0)

        # Decay epsilon (less random exploration over time)
        if self.epsilon > epsilon_min:
            self.epsilon *= epsilon_decay

    def update_target_network(self):
        self.target_model.set_weights(self.model.get_weights())
