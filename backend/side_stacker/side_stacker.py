class SideStacker:
    # TODO: Side / Player / Result should be an enum no?
    board: list[list] = None
    current_player: str = None
    result: str = None
    # TODO: rename
    combinations: list[tuple] = None

    def __init__(self) -> None:
        # Initial board state
        self.board = [["_" for _ in range(7)] for _ in range(7)]
        # Starting player
        self.current_player = "X"
        self.combinations = self._gen_combinations()

    def board_state(self) -> str:
        rows = [" ".join(row) for row in self.board]
        return "\n".join(rows)
    
    def state(self) -> dict:
        return {
            "current_player": self.current_player,
            "board": self.board,
            "result": self.result,
        }

    def play(self, player: str, row: int, side: str) -> str:
        if self.result is not None:
            raise
        if self.current_player is None:
            raise
        if player != self.current_player:
            raise
        if not 0 <= row < 7:
            raise
        if side != "Left" and side != "Right":
            raise

        self._make_move(player, row, side)
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

        self.result = self._eval_board()
        return self.board_state()

    def _make_move(self, player: str, row: int, side: str):
        play_row = self.board[row]

        if all([field != "_" for field in play_row]):
            raise

        if side == "Left":
            for i in range(7):
                if play_row[i] == "_":
                    play_row[i] = player
                    break
        elif side == "Right":
            for i in reversed(range(7)):
                if play_row[i] == "_":
                    play_row[i] = player
                    break
        else:
            raise

    # TODO: quite ugly
    def _gen_combinations(self):
        combinations = []

        # rows
        for i in range(7):
            # columns
            for j in range(7):
                # row
                if j + 3 < 7:
                    combinations.append([(i, j), (i, j + 1), (i, j + 2), (i, j + 3)])
                # column
                if i + 3 < 7:
                    combinations.append([(i, j), (i + 1, j), (i + 2, j), (i + 3, j)])
                # d1
                if i + 3 < 7 and j + 3 < 7:
                    combinations.append([(i, j), (i + 1, j + 1), (i + 2, j + 2), (i + 3, j + 3)])
                # d2
                if i + 3 < 7 and j - 3 >= 0:
                    combinations.append([(i, j), (i + 1, j - 1), (i + 2, j - 2), (i + 3, j - 3)])
        return combinations

    def _eval_board(self) -> str:
        for comb in self.combinations:
            first = self.board[comb[0][0]][comb[0][1]]
            if first == "_":
                continue
            if all(self.board[field[0]][field[1]] == first for field in comb):
                return first

        if self._is_board_full():
            return "tie"
        return None

    def _is_board_full(self) -> bool:
        return all(all([field != "_" for field in row]) for row in self.board)
