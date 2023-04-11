import pytest
from side_stacker.side_stacker import SideStacker

# TODO: test all exceptions
# TODO: create proper exceptions
def test_initial_board_state():
    game = SideStacker()
    expected = """
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
""".strip()

    assert game.board_state() == expected


def test_play():
    game = SideStacker()
    game.play("X", 1, "Left")
    expected = """
_ _ _ _ _ _ _
X _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
""".strip()

    assert game.board_state() == expected

    game.play("O", 1, "Left")
    expected = """
_ _ _ _ _ _ _
X O _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
""".strip()

    assert game.board_state() == expected

    game.play("X", 1, "Left")
    game.play("O", 6, "Right")
    game.play("X", 6, "Right")
    game.play("O", 5, "Right")
    game.play("X", 5, "Left")
    expected = """
_ _ _ _ _ _ _
X O X _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
X _ _ _ _ _ O
_ _ _ _ _ X O
""".strip()

    assert game.board_state() == expected


def test_row_full():
    game = SideStacker()
    # Fill row 1
    game.play("X", 1, "Left")
    game.play("O", 1, "Left")
    game.play("X", 1, "Left")
    game.play("O", 1, "Left")
    game.play("X", 1, "Left")
    game.play("O", 1, "Left")
    game.play("X", 1, "Left")

    with pytest.raises(Exception):
        game.play("O", 1, "Left")


def test_row_win():
    game = SideStacker()
    # X wins row 1
    game.play("X", 1, "Left")
    game.play("O", 3, "Left")
    game.play("X", 1, "Left")
    game.play("O", 3, "Left")
    game.play("X", 1, "Left")
    game.play("O", 3, "Left")
    game.play("X", 1, "Left")

    assert game.result == "X"


def test_column_win():
    game = SideStacker()
    # X wins column 0
    game.play("X", 1, "Left")
    game.play("O", 3, "Right")
    game.play("X", 2, "Left")
    game.play("O", 3, "Right")
    game.play("X", 3, "Left")
    game.play("O", 3, "Right")
    game.play("X", 4, "Left")

    assert game.result == "X"


def test_diagonal_win():
    game = SideStacker()
    # X wins (1,0), (2,1), (3,2), (4,3)
    game.play("X", 1, "Left")
    game.play("O", 2, "Left")
    game.play("X", 2, "Left")
    game.play("O", 3, "Left")
    game.play("X", 3, "Left")
    game.play("O", 4, "Left")
    game.play("X", 3, "Left")
    game.play("O", 4, "Left")
    game.play("X", 3, "Left")
    game.play("O", 4, "Left")
    game.play("X", 4, "Left")

    assert game.result == "X"

    # Other side
    game = SideStacker()
    # X wins (1,6), (2,5), (3,4), (4,3)
    game.play("X", 1, "Right")
    game.play("O", 2, "Right")
    game.play("X", 2, "Right")
    game.play("O", 3, "Right")
    game.play("X", 3, "Right")
    game.play("O", 4, "Right")
    game.play("X", 3, "Right")
    game.play("O", 4, "Right")
    game.play("X", 3, "Right")
    game.play("O", 4, "Right")
    game.play("X", 4, "Right")

    assert game.result == "X"


def test_cant_play_after_win():
    game = SideStacker()
    # X wins row 1
    game.play("X", 1, "Left")
    game.play("O", 3, "Left")
    game.play("X", 1, "Left")
    game.play("O", 3, "Left")
    game.play("X", 1, "Left")
    game.play("O", 3, "Left")
    game.play("X", 1, "Left")

    with pytest.raises(Exception):
        game.play("O", 3, "Left")


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

    game.play("X", 0, "Left")

    assert game.result == "X"


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

    game.play("X", 0, "Left")

    assert game.result == "tie"


# full board with winner
# full board with tie
