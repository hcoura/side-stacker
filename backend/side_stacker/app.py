from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .game_manager import GameManager
from .models import Base

# Skipping alembic (aka migrations) since it's just one simple table
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


game_manager = GameManager()


@app.post("/game/new")
async def new_game(db: Session = Depends(get_db)):
    return {"game_id": game_manager.new_game()}


@app.websocket("/ws/game/{game_id}")
async def game(websocket: WebSocket, game_id: str, db: Session = Depends(get_db)):
    await game_manager.join_game(websocket, game_id, db)

    try:
        while True:
            data = await websocket.receive_json()
            await game_manager.play(data, game_id, db)
    except WebSocketDisconnect:
        await game_manager.leave_game(websocket, game_id, db)
