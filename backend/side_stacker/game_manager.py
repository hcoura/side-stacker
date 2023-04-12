from fastapi import WebSocket

from side_stacker.side_stacker import (
    PLAYER_ONE,
    PLAYER_TWO,
    STATE_FINISHED,
    InvalidMoveException,
    SideStacker,
)


class InvalidGame(Exception):
    pass


class GameManager:
    def __init__(self) -> None:
        self.games = {}
        pass

    def new_game(self) -> str:
        game = SideStacker()
        self.games[game.id] = {
            "game": game,
            PLAYER_ONE: None,
            PLAYER_TWO: None,
        }
        return game.id

    async def join_game(self, websocket: WebSocket, game_id: str):
        if game_id not in self.games:
            raise InvalidGame("Game doesnt exist")
        game_dict = self.games[game_id]

        # TODO: right now first to join is always PLAYER_ONE
        await websocket.accept()
        if game_dict[PLAYER_ONE] is None:
            game_dict[PLAYER_ONE] = websocket
            await websocket.send_json({"type": "player", "player": PLAYER_ONE})
        elif game_dict[PLAYER_TWO] is None:
            game_dict[PLAYER_TWO] = websocket
            await websocket.send_json({"type": "player", "player": PLAYER_TWO})
        else:
            raise InvalidGame("Game is full")
        await self.broadcast_game_state(game_id)

    def leave_game(self, websocket: WebSocket, game_id: str):
        if game_id not in self.games:
            raise InvalidGame("Game doesnt exist")

        # TODO: broadcast the other player won

        del self.games[game_id]

    async def play(self, data: dict, game_id: str):
        # TODO: can't play until everyone joined
        if game_id not in self.games:
            raise InvalidGame("Game doesnt exist")
        if data["player"] not in (PLAYER_ONE, PLAYER_TWO):
            # TODO: invalid player (let burn, whatever... ??)
            return
        game = self.games[game_id]["game"]
        try:
            game.play(data["player"], data["row"], data["side"])
        except InvalidMoveException as e:
            # TODO: communicate move is invalid and why
            return

        await self.broadcast_game_state(game_id)

    async def broadcast_game_state(self, game_id: str):
        if game_id not in self.games:
            raise InvalidGame("Game doesnt exist")

        game_dict = self.games[game_id]
        state = game_dict["game"].game_state()
        state["type"] = "state"

        p1 = game_dict[PLAYER_ONE]
        p2 = game_dict[PLAYER_TWO]

        if p1 is not None:
            await p1.send_json(state)
        if p2 is not None:
            await p2.send_json(state)

        if state["state"] == STATE_FINISHED:
            del self.games[game_id]
