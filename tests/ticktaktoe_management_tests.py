import sys, os

sys.path.append(os.path.abspath('./app'))
from game_server.games.ticktaktoe import TikTakToe
from models.enums import GameStatus, PlayerRegistration

def createTickTakToe(x = 10, y = 10, scoreLine = 5):
    return TikTakToe(x, y, scoreLine)

def test_register_player():
    game = createTickTakToe(3, 3, 3)

    registrationResult = game.registerPlayer('Bronny')
    status = game.canMove('Bronny')

    assert registrationResult == PlayerRegistration.Success
    assert status == GameStatus.CanMove or status == GameStatus.Wait

def test_register_player_twice_should_error():
    game = createTickTakToe(3, 3, 3)

    registrationResult = game.registerPlayer('Bronny')
    registrationResult2 = game.registerPlayer('Bronny')

    assert registrationResult == PlayerRegistration.Success
    assert registrationResult2 == PlayerRegistration.AlreadyRegistered

def test_register_third_player_should_error():
    game = createTickTakToe(3, 3, 3)

    assert game.registerPlayer('Bronny') == PlayerRegistration.Success
    assert game.registerPlayer('Bill') == PlayerRegistration.Success
    assert game.registerPlayer('Third') == PlayerRegistration.NoPlayerSlotsLeft

def test_gets_player_statuses():
    game = createTickTakToe(3, 3, 3)

    game.registerPlayer('Bronny')
    game.registerPlayer('Bill')
    statuses = game.getPlayerStatuses()
    assert GameStatus.CanMove in statuses
    assert GameStatus.Wait in statuses
    