import os
import time
import logging
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model, Sequential, load_model, clone_model
from tensorflow.keras.layers import Input, Dense, Concatenate, Flatten
from tensorflow.keras.optimizers import Adam
import random

logger = logging.getLogger(__name__)

# Hyperparameters for DQN
MAX_GRID_SIZE = 10
GRID_AREA = MAX_GRID_SIZE * MAX_GRID_SIZE
MAX_POSSIBLE_MOVES = GRID_AREA * GRID_AREA
MOVE_VECTOR_LENGTH = 10
NO_VALUE = 0

# DQN Hyperparameters
gamma = 0.95  # Discount factor
alpha = 0.001  # Learning rate
epsilon = 1.0  # Exploration-exploitation trade-off
epsilon_min = 0.01
epsilon_decay = 0.995
batch_size = 64

# Reward system (fixed)
REWARD = {
    'INCORRECT': -10.0,  # Very bad - agent should avoid at all costs
    'LOST': -1.0,        # Bad - agent lost the game
    'MOVED': 0.0,        # Neutral - standard move
    'DRAW': 0.5,         # Good - better than losing
    'WON': 1.0           # Very good - agent won the game
}

class ReplayBuffer:
    def __init__(self, max_size=2000):
        self.buffer = []
        self.max_size = max_size
    
    def add(self, experience):
        if len(self.buffer) >= self.max_size:
            self.buffer.pop(0)
        self.buffer.append(experience)
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)

class ModelManager:
    def __init__(self, agentName):
        self.model_file = 'data/models/' + agentName + '_model.keras'
        self.replay_buffer = ReplayBuffer(max_size=2000)
        self.epsilon = epsilon
        self._loadModel()
        # Create target network
        self.target_model = clone_model(self.model)
        self.target_model.set_weights(self.model.get_weights())

    def save(self):
        self.model.save(self.model_file)

    def predict(self, board, moves):
        # Pad the board and moves to correct sizes
        padded_board = self._padBoard(board)
        padded_moves = self._padMoves(moves)

        # Reshape data for Keras (adding batch dimension)
        padded_board = np.expand_dims(padded_board, axis=0)
        padded_moves = np.expand_dims(padded_moves, axis=0)

        # Use epsilon-greedy policy for exploration
        if np.random.rand() <= self.epsilon:
            # Random move (exploration)
            prediction = np.random.randint(0, len(moves))
        else:
            # Best move (exploitation) - use main model for prediction
            q_values = self.model.predict([padded_board, padded_moves])
            prediction = np.argmax(q_values[0])
            
            # Convert from Q-value index to actual move index
            predicted_move_index = int(prediction) // MOVE_VECTOR_LENGTH
            if predicted_move_index < len(moves):
                prediction = predicted_move_index
            else:
                prediction = 0 - predicted_move_index

        # Decay epsilon
        if self.epsilon > epsilon_min:
            self.epsilon *= epsilon_decay

        return padded_board, padded_moves, prediction
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay buffer"""
        self.replay_buffer.add((state, action, reward, next_state, done))
    
    def train(self):
        """Train on a batch from replay buffer using DQN"""
        if len(self.replay_buffer) < batch_size:
            return
        
        # Sample a batch from replay buffer
        minibatch = self.replay_buffer.sample(batch_size)
        
        # Prepare batches
        states = []
        next_states = []
        targets = []
        
        for state, action, reward, next_state, done in minibatch:
            states.append(state)
            next_states.append(next_state)
            
            # Get current Q-values from main model
            current_q = self.model.predict(state)
            
            # Calculate target Q-value
            if done:
                target_q = reward
            else:
                # Use target network to calculate future Q-values
                future_q = self.target_model.predict(next_state)
                target_q = reward + gamma * np.amax(future_q[0])
            
            # Update the Q-value for the action taken
            current_q[0][action] = target_q
            targets.append(current_q[0])
        
        # Convert to numpy arrays
        states = np.array(states)
        targets = np.array(targets)
        
        # Train the model
        self.model.fit([states[:, 0], states[:, 1]], targets, batch_size=batch_size, epochs=1, verbose=0)
    
    def update_target_network(self):
        """Update target network with weights from main network"""
        self.target_model.set_weights(self.model.get_weights())

    def _newModel(self):
        logger.info("Creating a new DQN model.")
        # Define two separate inputs
        boardInput = Input(shape=(MAX_GRID_SIZE, MAX_GRID_SIZE), name='state_input')
        movesInput = Input(shape=(MAX_POSSIBLE_MOVES * MOVE_VECTOR_LENGTH,), name='possible_moves_input')

        # Flatten the inputs
        flattenerBoard = Flatten()(boardInput)
        flattenedMoves = Flatten()(movesInput)

        # Concatenate the flattened inputs
        concatenatedInputs = Concatenate()([flattenerBoard, flattenedMoves])

        # Add dense layers on top
        x = Dense(128, activation='relu')(concatenatedInputs)
        x = Dense(64, activation='relu')(x)

        # Output Q-values for each possible action (no softmax for DQN)
        output = Dense(MAX_POSSIBLE_MOVES, activation='linear')(x)

        # Create the model
        model = Model(inputs=[boardInput, movesInput], outputs=output)

        # Compile the model with mean squared error loss (standard for DQN)
        model.compile(optimizer=Adam(learning_rate=alpha), loss='mse')
        return model
    
    def _padBoard(self, board, max_size=MAX_GRID_SIZE):
        """
        Pad board to standard size with additional game information.
        
        The padded board will include:
        - Original board data
        - Board size information (encoded in padding)
        - Game type information (for future multi-game support)
        """
        # Convert board to a NumPy array if it's not already one
        if isinstance(board, list):
            board = np.array(board)

        # Calculate the padding sizes
        pad_height = max_size - board.shape[0]
        pad_width = max_size - board.shape[1]
        
        # Ensure non-negative padding sizes
        assert pad_height >= 0 and pad_width >= 0, "Board is larger than the max size to pad!"
        
        # Create padded board with game information
        padded_board = np.pad(board, 
                            ((0, pad_height), (0, pad_width)), 
                            'constant', 
                            constant_values=NO_VALUE)
        
        # Add board size information in the padding
        # Use specific padding values to encode board dimensions
        if pad_height > 0:
            # Encode original height in first padded row
            height_encoding = np.full((1, max_size), board.shape[0] / max_size, dtype=np.float32)
            padded_board[-pad_height:, :] = height_encoding
        
        if pad_width > 0:
            # Encode original width in first padded column
            width_encoding = np.full((max_size, 1), board.shape[1] / max_size, dtype=np.float32)
            padded_board[:, -pad_width:] = width_encoding
        
        return padded_board

    def _padMoves(self, moves, max_possible_moves=MAX_POSSIBLE_MOVES, move_vector_length=MOVE_VECTOR_LENGTH):
        """
        Pad moves to standard size with additional game information.
        
        The padded moves will include:
        - Original move coordinates
        - Number of valid moves (encoded in padding)
        - Move validity information
        """
        # Pad each move to have a length of MOVE_VECTOR_LENGTH
        padded_moves = [move + [NO_VALUE]*(move_vector_length - len(move)) for move in moves]

        # Now flatten the padded list of moves
        flattened_moves = [item for sublist in padded_moves for item in sublist]

        # Calculate the total length needed after padding the flattened moves
        total_length = max_possible_moves * move_vector_length

        # Further pad the flattened_moves list with NO_VALUE to match the total_length
        padded_flattened_moves = np.pad(flattened_moves, (0, total_length - len(flattened_moves)), 'constant', constant_values=NO_VALUE)
        
        # Add game information in the padding
        # Encode number of valid moves in the last few positions
        num_valid_moves = len(moves)
        if total_length - len(flattened_moves) >= 2:
            padded_flattened_moves[-2] = num_valid_moves / max_possible_moves  # Normalized count
            padded_flattened_moves[-1] = 1.0  # Valid moves indicator
        
        return padded_flattened_moves

    
    def _loadModel(self):
        if os.path.exists(self.model_file):
            logger.info("Loading existing NN model from the disk.")
            self.model = load_model(self.model_file)
        else:
            self.model = self._newModel()