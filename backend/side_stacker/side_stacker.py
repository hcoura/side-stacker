PLAYER_ONE = "X"
PLAYER_TWO = "O"
TIE = "tie"

BOARD_LEFT = "Left"
BOARD_RIGHT = "Right"

STATE_NEW = "New"
STATE_RUNNING = "Running"
STATE_FINISHED = "Finished"


class InvalidMoveException(Exception):
    pass


class SideStacker:
    # TODO: really None here?
    board: list[list] = None
    current_player: str = None
    winner: str = None
    # TODO: test state
    state: str = None

    def __init__(self) -> None:
        self.board = [["_" for _ in range(7)] for _ in range(7)]
        # TODO: randomly assign starting player
        self.current_player = PLAYER_ONE
        self.state = STATE_NEW
        self.winning_lines = self._get_winning_lines()

    def game_state(self) -> dict:
        return {
            "current_player": self.current_player,
            "board": self.board,
            "state": self.state,
            "winner": self.winner,
        }

    def play(self, player: str, row: int, side: str) -> dict:
        if self.winner is not None:
            raise InvalidMoveException("Game is over")
        if player != self.current_player:
            raise InvalidMoveException(f"You are not the current player!")

        self._make_move(player, row, side)
        self._switch_current_player()
        self._eval_board()
        return self.game_state()

    def _make_move(self, player: str, row: int, side: str):
        if not 0 <= row < 7:
            raise InvalidMoveException(f"Invalid row: {row}")
        if side not in (BOARD_LEFT, BOARD_RIGHT):
            raise InvalidMoveException(f"Given board size doesn't exist: {side}")

        play_row = self.board[row]

        if all([field != "_" for field in play_row]):
            raise InvalidMoveException("Row is full")

        r = range(7) if side == BOARD_LEFT else reversed(range(7))

        for i in r:
            if play_row[i] == "_":
                play_row[i] = player
                break

    def _eval_board(self):
        for line in self.winning_lines:
            first = self.board[line[0][0]][line[0][1]]
            if first == "_":
                continue
            if all(self.board[field[0]][field[1]] == first for field in line):
                self.winner = first
                self.state = STATE_FINISHED
                return

        if self._is_board_full():
            self.winner = TIE
            self.state = STATE_FINISHED
            return

        self.state = STATE_RUNNING

    def _switch_current_player(self):
        self.current_player = (
            PLAYER_TWO if self.current_player == PLAYER_ONE else PLAYER_ONE
        )

    def _is_board_full(self) -> bool:
        return all(all([field != "_" for field in row]) for row in self.board)

    def _get_winning_lines(self):
        """
        get_winning_lines returns all potential combinations of 4 points in the game grid
        that could be a winning line.

        Each line is a list of tuples with the indices for accessing the 2D array the board is
        """
        lines = []

        # rows
        for i in range(7):
            # columns
            for j in range(7):
                # row
                if j + 3 < 7:
                    lines.append([(i, j), (i, j + 1), (i, j + 2), (i, j + 3)])
                # column
                if i + 3 < 7:
                    lines.append([(i, j), (i + 1, j), (i + 2, j), (i + 3, j)])
                # d1
                if i + 3 < 7 and j + 3 < 7:
                    lines.append(
                        [(i, j), (i + 1, j + 1), (i + 2, j + 2), (i + 3, j + 3)]
                    )
                # d2
                if i + 3 < 7 and j - 3 >= 0:
                    lines.append(
                        [(i, j), (i + 1, j - 1), (i + 2, j - 2), (i + 3, j - 3)]
                    )
        return lines
