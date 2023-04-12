import pytest
from side_stacker.side_stacker import BOARD_LEFT, BOARD_RIGHT, PLAYER_ONE, PLAYER_TWO, InvalidMoveException, SideStacker


def test_initial_board_state():
    game = SideStacker()
    expected = [
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
    ]

    assert game.game_state()["board"] == expected


def test_play():
    game = SideStacker()
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    expected = [
        "_ _ _ _ _ _ _".split(),
        "X _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
    ]

    assert game.game_state()["board"] == expected

    game.play(PLAYER_TWO, 1, BOARD_LEFT)
    expected = [
        "_ _ _ _ _ _ _".split(),
        "X O _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
    ]

    assert game.game_state()["board"] == expected

    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 6, BOARD_RIGHT)
    game.play(PLAYER_ONE, 6, BOARD_RIGHT)
    game.play(PLAYER_TWO, 5, BOARD_RIGHT)
    game.play(PLAYER_ONE, 5, BOARD_LEFT)
    expected = [
        "_ _ _ _ _ _ _".split(),
        "X O X _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "_ _ _ _ _ _ _".split(),
        "X _ _ _ _ _ O".split(),
        "_ _ _ _ _ X O".split(),
    ]

    assert game.game_state()["board"] == expected


def test_row_full():
    game = SideStacker()
    # Fill row 1
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 1, BOARD_LEFT)
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 1, BOARD_LEFT)
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 1, BOARD_LEFT)
    game.play(PLAYER_ONE, 1, BOARD_LEFT)

    with pytest.raises(InvalidMoveException):
        game.play(PLAYER_TWO, 1, BOARD_LEFT)


def test_row_win():
    game = SideStacker()
    # Player one wins row 1
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 3, BOARD_LEFT)
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 3, BOARD_LEFT)
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 3, BOARD_LEFT)
    game.play(PLAYER_ONE, 1, BOARD_LEFT)

    assert game.winner == PLAYER_ONE


def test_column_win():
    game = SideStacker()
    # Player one wins column 0
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 3, BOARD_RIGHT)
    game.play(PLAYER_ONE, 2, BOARD_LEFT)
    game.play(PLAYER_TWO, 3, BOARD_RIGHT)
    game.play(PLAYER_ONE, 3, BOARD_LEFT)
    game.play(PLAYER_TWO, 3, BOARD_RIGHT)
    game.play(PLAYER_ONE, 4, BOARD_LEFT)

    assert game.winner == PLAYER_ONE


def test_diagonal_win():
    game = SideStacker()
    # Player one wins (1,0), (2,1), (3,2), (4,3)
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 2, BOARD_LEFT)
    game.play(PLAYER_ONE, 2, BOARD_LEFT)
    game.play(PLAYER_TWO, 3, BOARD_LEFT)
    game.play(PLAYER_ONE, 3, BOARD_LEFT)
    game.play(PLAYER_TWO, 4, BOARD_LEFT)
    game.play(PLAYER_ONE, 3, BOARD_LEFT)
    game.play(PLAYER_TWO, 4, BOARD_LEFT)
    game.play(PLAYER_ONE, 3, BOARD_LEFT)
    game.play(PLAYER_TWO, 4, BOARD_LEFT)
    game.play(PLAYER_ONE, 4, BOARD_LEFT)

    assert game.winner == PLAYER_ONE

    # Other side
    game = SideStacker()
    # Player one wins (1,6), (2,5), (3,4), (4,3)
    game.play(PLAYER_ONE, 1, BOARD_RIGHT)
    game.play(PLAYER_TWO, 2, BOARD_RIGHT)
    game.play(PLAYER_ONE, 2, BOARD_RIGHT)
    game.play(PLAYER_TWO, 3, BOARD_RIGHT)
    game.play(PLAYER_ONE, 3, BOARD_RIGHT)
    game.play(PLAYER_TWO, 4, BOARD_RIGHT)
    game.play(PLAYER_ONE, 3, BOARD_RIGHT)
    game.play(PLAYER_TWO, 4, BOARD_RIGHT)
    game.play(PLAYER_ONE, 3, BOARD_RIGHT)
    game.play(PLAYER_TWO, 4, BOARD_RIGHT)
    game.play(PLAYER_ONE, 4, BOARD_RIGHT)

    assert game.winner == PLAYER_ONE


def test_cant_play_after_win():
    game = SideStacker()
    # Player one wins row 1
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 3, BOARD_LEFT)
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 3, BOARD_LEFT)
    game.play(PLAYER_ONE, 1, BOARD_LEFT)
    game.play(PLAYER_TWO, 3, BOARD_LEFT)
    game.play(PLAYER_ONE, 1, BOARD_LEFT)

    with pytest.raises(InvalidMoveException):
        game.play(PLAYER_TWO, 3, BOARD_LEFT)


def test_full_board_winner():
    game = SideStacker()
    game.board = [
        "X O X X _ X O".split(),
        "X X O X O X X".split(),
        "O X O X O O O".split(),
        "X O X O X O X".split(),
        "X O O O X X O".split(),
        "O X O X O X O".split(),
        "X X O O X O X".split(),
    ]

    game.play(PLAYER_ONE, 0, BOARD_LEFT)

    assert game.winner == PLAYER_ONE


def test_full_board_tie():
    game = SideStacker()
    game.board = [
        "X O X O _ X O".split(),
        "X X O X O X X".split(),
        "O X O X O O O".split(),
        "X O X O X O X".split(),
        "X O X O X X O".split(),
        "O X O X O X O".split(),
        "X X O O X O X".split(),
    ]

    game.play(PLAYER_ONE, 0, BOARD_LEFT)

    assert game.winner == "tie"
