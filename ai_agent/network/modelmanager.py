import os
import time
import logging
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.layers import Input, Dense, Concatenate, Flatten
from tensorflow.keras.losses import sparse_categorical_crossentropy
from tensorflow.keras.utils import register_keras_serializable

logger = logging.getLogger(__name__)

MAX_GRID_SIZE = 10
GRID_AREA = MAX_GRID_SIZE * MAX_GRID_SIZE
MAX_POSSIBLE_MOVES = GRID_AREA * GRID_AREA
MOVE_VECTOR_LENGTH = 10
NO_VALUE = 0

LABEL = {
    'INCORRECT': 9999,
    'LOST' : 10000,
    'DRAW' : 10001,
    'WON' : 10002,
}
REWARD = {
    'INCORRECT': 1.0,   # Positive value as a penalty
    'LOST' : 0.2,       # Less bad than INCORRECT
    'MOVED' : 0.0,      # No reward or penalty
    'DRAW' : -0.2,      # Less than WIN_REWARD (but decent progress towards winning)
    'WON' : -1.0,       # Negative value as a reward
}

#@keras.saving.register_keras_serializable()
def custom_loss(y_true, y_pred):
    # Create a loss multiplier, setting it high for incorrect moves
    loss_multiplier = tf.where(tf.equal(y_true, LABEL['INCORRECT']), 10.0, 1.0)
    
    # Calculate the standard sparse categorical crossentropy loss
    scce = tf.keras.losses.sparse_categorical_crossentropy(y_true, y_pred)
    
    # Apply the multiplier to penalize incorrect moves more
    custom_loss = scce * loss_multiplier
    return custom_loss

class ModelManager:
    def __init__(self, agentName):
        self.model_file = 'data/models/' +agentName + '_model.keras'
        self._loadModel()

    def save(self):
        self.model.save(self.model_file)

    def predict(self, board, moves):
        # Pad the board and moves to correct sizes
        padded_board = self._padBoard(board)
        padded_moves = self._padMoves(moves)

        # Reshape data for Keras (adding batch dimension)
        padded_board = np.expand_dims(padded_board, axis=0)
        padded_moves = np.expand_dims(padded_moves, axis=0)

        # Predict the move
        move_probabilities = self.model.predict([padded_board, padded_moves])
        prediction = np.argmax(move_probabilities, axis=1)[0]
        predicted_move_index = int(prediction) // MOVE_VECTOR_LENGTH

        avg = np.average(move_probabilities)
        logger.debug("Predicted move index: " + str(predicted_move_index))
        logger.debug("Min: " + str(np.min(move_probabilities))+ " Max: " + str(np.max(move_probabilities)) + " Avg: " + str(avg))

        if predicted_move_index < len(moves):
            original_move = predicted_move_index
        else:
            original_move = 0 - predicted_move_index
        return padded_board, padded_moves, original_move
    
    def train(self, boards, moves, label, index):
        # Convert label to the correct shape for Keras: (batch_size, )
        labels = np.array([label])
        start_time = time.time()

        self.model.fit([boards, moves], labels, batch_size=1, epochs=1, verbose=0)

        end_time = time.time()
        duration = (end_time - start_time) * 1000

        logger.debug(f"Training took {duration:.2f} ms.")

    def _newModel(self):
        logger.info("Creating a new NN model.")
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

        # Output a fixed-size softmax layer plus LABELed special outcomes
        output = Dense(MAX_POSSIBLE_MOVES + len(LABEL), activation='softmax')(x)

        # Create the model
        model = Model(inputs=[boardInput, movesInput], outputs=output)

        # Compile the model
        model.compile(optimizer='adam',
            loss=custom_loss,
            metrics=['accuracy'])
        return model
    
    def _padBoard(self, board, max_size=MAX_GRID_SIZE):
        # Convert board to a NumPy array if it's not already one
        if isinstance(board, list):
            board = np.array(board)

        # Calculate the padding sizes
        pad_height = max_size - board.shape[0]
        pad_width = max_size - board.shape[1]
        
        # Ensure non-negative padding sizes
        assert pad_height >= 0 and pad_width >= 0, "Board is larger than the max size to pad!"
        
        # Pad the board array with the pad_value
        padded_board = np.pad(board, 
                            ((0, pad_height), (0, pad_width)), 
                            'constant', 
                            constant_values=NO_VALUE)
        return padded_board

    def _padMoves(self, moves, max_possible_moves=MAX_POSSIBLE_MOVES, move_vector_length=MOVE_VECTOR_LENGTH):
        # Pad each move to have a length of MOVE_VECTOR_LENGTH
        padded_moves = [move + [NO_VALUE]*(move_vector_length - len(move)) for move in moves]

        # Now flatten the padded list of moves
        flattened_moves = [item for sublist in padded_moves for item in sublist]

        # Calculate the total length needed after padding the flattened moves
        total_length = max_possible_moves * move_vector_length

        # Further pad the flattened_moves list with NO_VALUE to match the total_length
        padded_flattened_moves = np.pad(flattened_moves, (0, total_length - len(flattened_moves)), 'constant', constant_values=NO_VALUE)
        
        return padded_flattened_moves

    
    def _loadModel(self):
        if os.path.exists(self.model_file):
            logger.info("Loading existing NN model from the disk.")
            self.model = load_model(self.model_file)
        else:
            self.model = self._newModel()