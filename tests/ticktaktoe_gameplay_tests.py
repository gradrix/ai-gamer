import pytest
import sys, os

sys.path.append(os.path.abspath('./app'))
from game_server.games.ticktaktoe import TikTakToe, E, X, O
from models.enums import GameStatus, PlayerRegistration

def createTickTakToe(x = 10, y = 10, scoreLine = 5):
    return TikTakToe(x, y, scoreLine)

def test_that_grid_is_initialized():
    game = TikTakToe(10, 10, 5)

    assert len(game.grid) == 10
    for row in game.grid:
        assert len(row) == 10
        for item in row:
            assert item == E

def test_initialize_game_with_impossible_score_length():
    #should raise exceptions
    with pytest.raises(Exception):
        TikTakToe(10, 10, 11)
    with pytest.raises(Exception):
        TikTakToe(10, 10, 15)
    with pytest.raises(Exception):
        TikTakToe(3, 3, 5)

    #should not raise exceptions
    TikTakToe(10, 10, 5)
    TikTakToe(10, 10, 10)
    TikTakToe(3, 3, 3)

def test_allowed_to_place_figure():
    game = createTickTakToe()

    assert [E, E, E, X, E, E, E, E, E, E] not in game.grid
    assert game.placeFigure(3, 3, X) == True
    assert [E, E, E, X, E, E, E, E, E, E] in game.grid
    assert game.placeFigure(5, 3, X) == True
    assert game.placeFigure(8, 3, X) == True
    assert [E, E, E, X, E, X, E, E, X, E] in game.grid

def test_forbidden_to_place_figure():
    game = createTickTakToe()
    assert game.placeFigure(3, 3, X) == True

    assert game.placeFigure(3, 3, O) == False
    assert game.placeFigure(3, 1, E) == False
    assert game.placeFigure(10, 3, X) == False
    assert game.placeFigure(5, 13, X) == False
    assert game.placeFigure(-5, 5, X) == False
    assert game.placeFigure(5, -5, X) == False

def test_check_for_winner_3_x_3_no_winner():
    game = createTickTakToe(3, 3, 3)

    game.grid = [
    [X, X, O],
    [O, O, X],
    [X, O, X]]
    assert game.checkForWinner() == False

    game.grid = [
    [E, E, E],
    [E, E, E],
    [E, E, E]]
    assert game.checkForWinner() == False

def test_check_for_winner_3_x_3_diagonally_left():
    game = createTickTakToe(3, 3, 3)

    game.grid = [
    [O, X, X],
    [X, O, O],
    [X, O, O]]
    assert game.checkForWinner() == O

    game = createTickTakToe(3, 3, 2)

    game.grid = [
    [O, E, O],
    [E, E, X],
    [O, E, O]]
    assert game.checkForWinner() == O

def test_check_for_winner_3_x_3_diagonally_right():
    game = createTickTakToe(3, 3, 3)

    game.grid = [
    [X, X, O],
    [O, O, X],
    [O, O, X]]
    assert game.checkForWinner() == O

def test_check_for_winner_3_x_3_vertically():
    game = createTickTakToe(3, 3, 3)

    game.grid = [
    [O, O, X],
    [X, O, X],
    [O, X, X]]
    assert game.checkForWinner() == X

    game.grid = [
    [X, O, O],
    [X, O, X],
    [X, X, O]]
    assert game.checkForWinner() == X

    game.grid = [
    [O, X, O],
    [O, X, X],
    [X, X, O]]
    assert game.checkForWinner() == X

def test_check_for_winner_3_x_3_horizontally():
    game = createTickTakToe(3, 3, 3)

    game.grid = [
    [X, X, X],
    [X, O, O],
    [O, X, O]]
    assert game.checkForWinner() == X

    game.grid = [
    [X, O, O],
    [X, X, X],
    [O, X, O]]
    assert game.checkForWinner() == X

    game.grid = [
    [X, O, O],
    [O, X, O],
    [X, X, X]]
    assert game.checkForWinner() == X
