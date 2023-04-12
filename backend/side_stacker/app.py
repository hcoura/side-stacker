from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from side_stacker.game_manager import GameManager

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

game_manager = GameManager()


@app.post("/game/new")
async def new_game():
    return {"game_id": game_manager.new_game()}


@app.websocket("/ws/game/{game_id}")
async def game(websocket: WebSocket, game_id: str):
    await game_manager.join_game(websocket, game_id)

    try:
        while True:
            data = await websocket.receive_json()
            await game_manager.play(data, game_id)
    except WebSocketDisconnect:
        game_manager.leave_game(websocket, game_id)
        # TODO: player left, broadcast to the other player they won
        # await manager.broadcast(games[game_id].state(), game_id)
