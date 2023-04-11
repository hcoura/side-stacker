# from typing import Annotated

# from fastapi import (
#     Cookie,
#     Depends,
#     FastAPI,
#     Query,
#     WebSocket,
#     WebSocketException,
#     WebSocketDisconnect,
#     status,
# )
# from fastapi.responses import HTMLResponse

# app = FastAPI()


# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <form action="" onsubmit="sendMessage(event)">
#             <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
#             <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
#             <button onclick="connect(event)">Connect</button>
#             <hr>
#             <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#         var ws = null;
#             function connect(event) {
#                 var itemId = document.getElementById("itemId")
#                 var token = document.getElementById("token")
#                 ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
#                 ws.onmessage = function(event) {
#                     var messages = document.getElementById('messages')
#                     var message = document.createElement('li')
#                     var content = document.createTextNode(event.data)
#                     message.appendChild(content)
#                     messages.appendChild(message)
#                 };
#                 event.preventDefault()
#             }
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)


# manager = ConnectionManager()



# @app.get("/")
# async def get():
#     return HTMLResponse(html)


# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")


# async def get_cookie_or_token(
#     websocket: WebSocket,
#     session: Annotated[str | None, Cookie()] = None,
#     token: Annotated[str | None, Query()] = None,
# ):
#     if session is None and token is None:
#         raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
#     return session or token


# @app.websocket("/items/{item_id}/ws")
# async def websocket_endpoint(
#     *,
#     websocket: WebSocket,
#     item_id: str,
#     q: int | None = None,
#     cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
# ):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(
#             f"Session cookie or query token value is: {cookie_or_token}"
#         )
#         if q is not None:
#             await websocket.send_text(f"Query parameter q is: {q}")
#         await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from collections import defaultdict
from .side_stacker import SideStacker

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, game_id: int):
        await websocket.accept()
        self.active_connections[game_id].append(websocket)

    def disconnect(self, websocket: WebSocket, game_id: int):
        self.active_connections[game_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, data: dict, game_id: int):
        for connection in self.active_connections[game_id]:
            await connection.send_json(data)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/game/new")
async def get():
    # creates a new game and returns it's id
    return {}


games = {}

@app.websocket("/ws/game/{game_id}")
async def game(websocket: WebSocket, game_id: int):
    await manager.connect(websocket, game_id)

    # just to get it working
    if game_id in games:
        state = games[game_id].state()
        state["player"] = "O"
        await websocket.send_json(state)
    else:
        games[game_id] = SideStacker()
        state = games[game_id].state()
        state["player"] = "X"
        await websocket.send_json(state)

    try:
        while True:
            data = await websocket.receive_json()
            try:
                # TODO:
                games[game_id].play(data['player'] , data['row'], data["side"])
            except:
                pass
            
            await manager.broadcast(games[game_id].state(), game_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)
        # TODO: handle disconnect / reconnect properly
        await manager.broadcast(games[game_id].state(), game_id)

