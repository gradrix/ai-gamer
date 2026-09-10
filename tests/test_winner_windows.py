"""Regression coverage for contiguous winning windows and draw potential."""

from copy import deepcopy

import pytest

from game_server.games.ticktaktoe import E, O, X, TikTakToe


def make_game(width, height, length, cells=(), figure=X):
    game = TikTakToe(width, height, length)
    for x, y in cells:
        assert game.placeFigure(x, y, figure)
    return game


@pytest.mark.parametrize("cells", [
    [(0, 0), (2, 0), (4, 0)],
    [(0, 0), (0, 2), (0, 4)],
    [(0, 0), (2, 2), (4, 4)],
    [(0, 4), (2, 2), (4, 0)],
])
def test_separated_pieces_do_not_form_a_winning_line(cells):
    game = make_game(5, 5, 3, cells)
    assert game.checkForWinner() is False
    assert game.stillCouldHaveWinner is True


@pytest.mark.parametrize("figure", [X, O])
def test_anti_diagonal_starting_away_from_left_edge(figure):
    game = make_game(5, 5, 3, [(2, 4), (3, 3), (4, 2)], figure)
    assert game.checkForWinner() == figure
    assert game.stillCouldHaveWinner is True


@pytest.mark.parametrize("width,height,cells", [
    (7, 4, [(4, 3), (5, 3), (6, 3)]),
    (4, 7, [(3, 4), (3, 5), (3, 6)]),
    (7, 4, [(4, 1), (5, 2), (6, 3)]),
    (4, 7, [(1, 6), (2, 5), (3, 4)]),
])
@pytest.mark.parametrize("figure", [X, O])
def test_rectangular_boards_cover_all_four_directions(width, height, cells, figure):
    game = make_game(width, height, 3, cells, figure)
    before = deepcopy(game.grid)
    assert game.checkForWinner() == figure
    assert game.checkForWinner() == figure
    assert game.grid == before
    assert game.stillCouldHaveWinner is True


def test_full_draw_has_no_possible_winning_window():
    game = make_game(3, 3, 3)
    game.grid = [[X, O, X], [X, O, O], [O, X, X]]
    assert game.checkForWinner() is False
    assert game.stillCouldHaveWinner is False


def test_empty_board_has_potential_and_recomputes_it_after_a_draw():
    game = make_game(3, 3, 3)
    game.grid = [[X, O, X], [X, O, O], [O, X, X]]
    assert game.checkForWinner() is False
    assert game.stillCouldHaveWinner is False
    game.grid = [[E] * 3 for _ in range(3)]
    assert game.checkForWinner() is False
    assert game.stillCouldHaveWinner is True


def test_already_winning_window_counts_as_possible():
    game = make_game(3, 3, 3)
    game.grid = [[E, X, O], [E, X, O], [X, X, X]]
    assert game.checkForWinner() == X
    assert game.stillCouldHaveWinner is True
