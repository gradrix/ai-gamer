import time
import threading
import logging
import numpy as np
from common.rpc.rpcclient import GameEngineRpcClient
from common.models.enums import PlayerStatus, MoveStatus, PlayerRegistration
from .network.controller import Controller # Controller will be adapted later
from .network.neuralnetwork import REWARD # For rewards

logger = logging.getLogger(__name__)

# Define constants for agent learning schedule
TARGET_UPDATE_FREQUENCY = 100  # Example: Update target network every 100 steps/games
MODEL_SAVE_FREQUENCY = 500    # Example: Save model every 500 steps/games


class GameRunner:

    def __init__(self, host, port, agentName):
        self.client = GameEngineRpcClient(host, port)
        # Controller will be initialized with actual network components later
        # For now, placeholders for board_height, board_width, num_actions might be needed
        # if the Controller __init__ expects them. Assuming Controller __init__ will be adapted.
        self.controller = Controller(agentName) # This will need to be adapted for new __init__
        self.playerId = agentName
        self.game_initialized = False
        self.steps_since_last_target_update = 0
        self.steps_since_last_model_save = 0
        self.__initKeepAliveRequestor()
        self.__register() # This will call _initialize_agent_and_controller

    def _initialize_agent_and_controller(self):
        logger.info("Initializing agent and controller for the game...")
        try:
            grid_response = self.client.getCurrentBoard()
            board_height = len(grid_response.grid)
            board_width = len(grid_response.grid[0].items) if board_height > 0 else 0

            moves_response = self.client.getPossibleMoves() # Assuming this returns all possible action slots
            num_actions = len(moves_response.moves)

            if board_height == 0 or board_width == 0 or num_actions == 0:
                logger.error("Failed to get valid board dimensions or number of actions. Retrying...")
                time.sleep(5) # Wait before retrying
                # Potentially re-register or signal critical error
                self.__register() # Attempt to re-initialize by re-registering
                return


            logger.info(f"Board dimensions: {board_height}x{board_width}, Num actions: {num_actions}")
            
            # The controller will be responsible for creating nn and agent
            self.controller.initialize_network_components(board_height, board_width, num_actions)
            self.game_initialized = True
            logger.info("Agent and controller initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing agent and controller: {e}. Will retry registration.")
            self.game_initialized = False # Ensure it's false so registration retries initialization
            # Consider a backoff strategy for retries
            time.sleep(5)
            self.__register() # Attempt to re-initialize

    def start(self):
        while True:
            if not self.game_initialized:
                logger.info("Game not initialized. Attempting to initialize...")
                # Registration implicitly calls _initialize_agent_and_controller
                # if game_initialized is False.
                # However, if registration was successful but initialization failed,
                # we might need a direct call.
                self._initialize_agent_and_controller()
                if not self.game_initialized: # If still not initialized after attempt
                    logger.error("Failed to initialize game after explicit attempt. Waiting before retry.")
                    time.sleep(10) # Wait longer before retrying the loop
                    continue

            player_status_response = self.client.canMove(self.playerId)
            logger.info("Player status: " + str(player_status_response.status))
            
            current_board_response = self.client.getCurrentBoard()
            board_array = np.array([[item for item in row.items] for row in current_board_response.grid], dtype=np.int32)

            match player_status_response.status:
                case PlayerStatus.UnregisteredPlayer:
                    logger.warning("Player unregistered. Attempting to re-register.")
                    self.game_initialized = False # Force re-initialization
                    self.__register()
                case PlayerStatus.Won:
                    self.__gameEnded('I\'ve won!')
                    self.controller.won(board_array)
                    self.game_initialized = False # Re-initialize for new game
                case PlayerStatus.Lost:
                    self.__gameEnded('I\'ve lost :-/')
                    self.controller.lost(board_array)
                    self.game_initialized = False # Re-initialize for new game
                case PlayerStatus.Draw:
                    self.__gameEnded('It\'s a draw..')
                    self.controller.draw(board_array)
                    self.game_initialized = False # Re-initialize for new game
                case PlayerStatus.CanMove:
                    self.__makeSomeMove(board_array)
                    self.steps_since_last_target_update += 1
                    self.steps_since_last_model_save += 1

                    if self.steps_since_last_target_update >= TARGET_UPDATE_FREQUENCY:
                        logger.info("Updating target network.")
                        if hasattr(self.controller, 'agent') and self.controller.agent is not None:
                             self.controller.agent.update_target_network()
                        self.steps_since_last_target_update = 0
                    
                    if self.steps_since_last_model_save >= MODEL_SAVE_FREQUENCY:
                        logger.info(f"GameRunner {self.playerId}: Saving model.")
                        if hasattr(self.controller, 'nn') and self.controller.nn is not None:
                            self.controller.nn.save()
                        self.steps_since_last_model_save = 0
            
            time.sleep(0.1) # Small delay to prevent tight loop spamming in edge cases

    def __register(self) -> bool:
        registration_response = self.client.registerPlayer(self.playerId)
        registered = False
        match registration_response.status:
            case PlayerRegistration.NoPlayerSlotsLeft:
                logger.critical("No place in server")
                raise Exception('No free player slots availabe - won\'t be able to participate..')
            case PlayerRegistration.AlreadyRegistered:
                logger.info('Logging in as already registered '+self.playerId)
                registered = True
            case PlayerRegistration.Registered: # Assuming a 'Registered' status for new successful registration
                logger.info('Successfully registered as '+self.playerId)
                registered = True
            case _: # Catch any other unexpected status
                logger.error(f"Unexpected registration status: {registration_response.status}")
                registered = False # Treat as not registered
        
        if registered and not self.game_initialized:
            self._initialize_agent_and_controller()
        
        return registered
            
    def __gameEnded(self, message):
        logger.info(str(message) + '. Waiting for the game to be started again..')
        # game_initialized will be set to False, prompting re-initialization for the next game.
        time.sleep(1) # Slightly longer pause after game end

    def __makeSomeMove(self, board_array): # Receives raw board_array
        # Controller's guess method is responsible for state preprocessing
        predicted_move_index = self.controller.guess(board_array)
        
        move_response = self.client.move(self.playerId, predicted_move_index)
        
        # Get the state after the move, regardless of success or failure,
        # as the board might change (e.g. opponent moves if we are too slow, though not typical for incorrect)
        # or for logging/debugging.
        current_board_response_after_move = self.client.getCurrentBoard()
        board_array_after_move = np.array([[item for item in row.items] for row in current_board_response_after_move.grid], dtype=np.int32)

        if move_response.status == MoveStatus.Success:
            logger.debug(f'Move to index {predicted_move_index} was successful.')
            # Controller's moved method handles remember and replay
            self.controller.moved(board_array_after_move, REWARD['MOVED'])
        elif move_response.status == MoveStatus.Incorrect:
            logger.debug(f'Move to index {predicted_move_index} was incorrect.')
            # Controller's incorrect method handles remember and replay
            self.controller.incorrect(board_array_after_move)
        else: # Other statuses like Error, etc.
            logger.error(f"Unexpected move status: {move_response.status} for move index {predicted_move_index}")
            # Optionally, penalize or handle this specific case in the controller if needed
            # For now, we might not call a controller learning method, or call a generic penalty.

    def __initKeepAliveRequestor(self):
        thread = threading.Thread(target=self.__keepAliveRequestor, args=())
        thread.daemon = True
        thread.start()

    def __keepAliveRequestor(self):
        while True:
            self.client.keepAlive(self.playerId)
            time.sleep(2)