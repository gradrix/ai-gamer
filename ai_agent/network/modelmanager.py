import os
import time
import logging
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model, Sequential, load_model, clone_model
from tensorflow.keras.layers import (
    Input,
    Dense,
    Concatenate,
    Flatten,
    Conv2D,
    MaxPooling2D,
)
from tensorflow.keras.optimizers import Adam
import random

logger = logging.getLogger(__name__)

# Hyperparameters for DQN
MAX_GRID_SIZE = 10
GRID_AREA = MAX_GRID_SIZE * MAX_GRID_SIZE
MAX_POSSIBLE_MOVES = GRID_AREA
MOVE_VECTOR_LENGTH = 1  # Not used for CNN
NO_VALUE = 0

# DQN Hyperparameters
gamma = 0.95  # Discount factor
alpha = 0.001  # Learning rate
epsilon = 1.0  # Exploration-exploitation trade-off
epsilon_min = 0.1  # Higher minimum to maintain some exploration
epsilon_decay = 0.995  # Slower decay for better exploration
batch_size = 64

# Reward system (fixed)
REWARD = {
    "INCORRECT": -10.0,  # Very bad - agent should avoid at all costs
    "LOST": -1.0,  # Bad - agent lost the game
    "MOVED": 0.0,  # Neutral - standard move
    "DRAW": 0.5,  # Good - better than losing
    "WON": 1.0,  # Very good - agent won the game
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
        self.model_file = "data/models/" + agentName + "_model.keras"
        self.replay_buffer = ReplayBuffer(max_size=10000)
        self.epsilon = epsilon
        self.train_steps = 0
        self._loadModel()
        # Create target network
        self.target_model = clone_model(self.model)
        self.target_model.set_weights(self.model.get_weights())

    def save(self):
        self.model.save(self.model_file)

    def predict(self, board, moves):
        # Pad the board and moves to correct sizes
        padded_board_unb = self._padBoard(board)
        padded_moves_unb = self._padMoves(moves)

        # Reshape data for Keras (adding batch dimension)
        padded_board = np.expand_dims(padded_board_unb, axis=0)
        padded_moves = np.expand_dims(padded_moves_unb, axis=0)

        # Use epsilon-greedy policy for exploration
        if np.random.rand() <= self.epsilon:
            # Random move (exploration)
            prediction = np.random.randint(0, len(moves))
        else:
            # Best move (exploitation) - use main model for prediction
            q_values = self.model.predict(
                [padded_board, padded_moves], verbose=0
            )  # Suppress verbose output
            # Only consider Q-values for the actual available moves to avoid invalid indices
            valid_q_values = q_values[0][
                : len(moves)
            ]  # Limit to number of actual moves
            if len(valid_q_values) > 0:
                prediction = np.argmax(valid_q_values)
            else:
                prediction = 0  # Default to first move if no valid moves

        # Decay epsilon
        if self.epsilon > epsilon_min:
            self.epsilon *= epsilon_decay

        return padded_board_unb, padded_moves_unb, prediction

    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay buffer"""
        self.replay_buffer.add((state, action, reward, next_state, done))

    def train(self):
        """Train on a batch from replay buffer using DQN"""
        if len(self.replay_buffer) < batch_size:
            return

        self.train_steps += 1
        if self.train_steps % 1000 == 0:
            self.update_target_network()

        # Sample a batch from replay buffer
        minibatch = self.replay_buffer.sample(batch_size)

        # Prepare batches
        state_boards = []
        state_moves = []
        targets = []

        for state, action, reward, next_state, done in minibatch:
            # Extract board and moves from state (state is [board, moves])
            state_board = state[0]
            state_moves_tensor = state[1]

            state_boards.append(state_board)
            state_moves.append(state_moves_tensor)

            # Get current Q-values from main model
            current_q = self.model.predict(
                [
                    np.expand_dims(state_board, axis=0),
                    np.expand_dims(state_moves_tensor, axis=0),
                ]
            )
            current_q = current_q[0]  # Remove batch dimension

            # Calculate target Q-value
            if done:
                target = reward  # Terminal state: target is just the reward
            else:
                # Use target network to calculate future Q-values
                next_board = next_state[0]
                next_moves = next_state[1]
                future_q_values = self.target_model.predict(
                    [
                        np.expand_dims(next_board, axis=0),
                        np.expand_dims(next_moves, axis=0),
                    ]
                )
                future_q_max = np.amax(future_q_values[0])
                target = reward + gamma * future_q_max  # Q-learning target

            # Update the Q-value for the action taken
            target_q = np.copy(current_q)
            if 0 <= action < len(target_q):
                target_q[action] = target
            else:
                # Action index out of bounds, skip this sample
                continue

            targets.append(target_q)

        if len(targets) == 0:
            return

        # Convert to numpy arrays
        state_boards = np.array(state_boards)
        state_moves = np.array(state_moves)
        targets = np.array(targets)

        # Train the model
        self.model.fit(
            [state_boards, state_moves],
            targets,
            batch_size=min(batch_size, len(targets)),
            epochs=1,
            verbose=0,
        )

    def update_target_network(self):
        """Update target network with weights from main network"""
        self.target_model.set_weights(self.model.get_weights())

    def _newModel(self):
        logger.info("Creating CNN DQN model for spatial learning.")
        board_input = Input(shape=(MAX_GRID_SIZE, MAX_GRID_SIZE, 1))
        x = Conv2D(32, (3, 3), activation="relu", padding="same")(board_input)
        x = MaxPooling2D((2, 2))(x)
        x = Conv2D(64, (3, 3), activation="relu", padding="same")(x)
        x = MaxPooling2D((2, 2))(x)
        x = Flatten()(x)

        moves_input = Input(shape=(GRID_AREA, ))
        x = Concatenate()([x, moves_input])
        x = Dense(128, activation="relu")(x)
        q_values = Dense(GRID_AREA, activation="linear")(x)

        model = Model(inputs=[board_input, moves_input], outputs=q_values)
        model.compile(optimizer=Adam(learning_rate=alpha), loss="mse")
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
        assert pad_height >= 0 and pad_width >= 0, (
            "Board is larger than the max size to pad!"
        )

        # Create padded board with game information
        padded_board = np.pad(
            board,
            ((0, pad_height), (0, pad_width)),
            "constant",
            constant_values=NO_VALUE,
        )

        # Add board size information in the padding
        # Use specific padding values to encode board dimensions
        if pad_height > 0:
            # Encode original height in first padded row
            height_encoding = np.full(
                (1, max_size), board.shape[0] / max_size, dtype=np.float32
            )
            padded_board[-pad_height:, :] = height_encoding

        if pad_width > 0:
            # Encode original width in first padded column
            width_encoding = np.full(
                (max_size, 1), board.shape[1] / max_size, dtype=np.float32
            )
            padded_board[:, -pad_width:] = width_encoding

        padded_board = np.expand_dims(padded_board, axis=2)
        return padded_board

    def _padMoves(
        self,
        moves,
        max_possible_moves=MAX_POSSIBLE_MOVES,
        move_vector_length=MOVE_VECTOR_LENGTH,
    ):
        """
        Pad moves to standard size with additional game information.

        The padded moves will include:
        - Original move coordinates
        - Number of valid moves (encoded in padding)
        - Move validity information
        """
        # Pad each move to have a length of MOVE_VECTOR_LENGTH
        padded_moves = [
            move + [NO_VALUE] * (move_vector_length - len(move)) for move in moves
        ]

        # Now flatten the padded list of moves
        flattened_moves = [item for sublist in padded_moves for item in sublist]

        # Calculate the total length needed after padding the flattened moves
        total_length = max_possible_moves * move_vector_length

        # Further pad the flattened_moves list with NO_VALUE to match the total_length
        padded_flattened_moves = np.pad(
            flattened_moves,
            (0, total_length - len(flattened_moves)),
            "constant",
            constant_values=NO_VALUE,
        )

        # Add game information in the padding
        # Encode number of valid moves in the last few positions
        num_valid_moves = len(moves)
        if total_length - len(flattened_moves) >= 2:
            padded_flattened_moves[-2] = (
                num_valid_moves / max_possible_moves
            )  # Normalized count
            padded_flattened_moves[-1] = 1.0  # Valid moves indicator

        return padded_flattened_moves

    def _loadModel(self):
        if os.path.exists(self.model_file):
            logger.info("Loading existing NN model from the disk.")
            self.model = load_model(self.model_file)
        else:
            self.model = self._newModel()
