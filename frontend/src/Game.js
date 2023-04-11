import './App.css';
import React, { useState, useCallback, useEffect } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import Board from "./Board";

const WS_URL = 'ws://127.0.0.1:8000';

// client_id
// game_id
// create_new_game
// get_game_state

function Game() {
  // let client_id = Date.now()

  // useWebSocket(`ws://localhost:8000/ws/${client_id}`, {
  const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket(`ws://localhost:8000/ws/game/12`, {
    onOpen: (event) => {
      console.log('WebSocket connection established.');
    }
  });

  const [messageHistory, setMessageHistory] = useState([]);
  const [player, setPlayer] = useState("");

  useEffect(() => {
    if (lastJsonMessage !== null) {
      setMessageHistory((prev) => prev.concat(lastJsonMessage));
    }
  }, [lastJsonMessage, setMessageHistory]);

  useEffect(() => {
    if (player != "") return;
    if (!lastJsonMessage?.player) return;
    setPlayer(lastJsonMessage.player);
  }, [lastJsonMessage]);

  const handleClickSendMessage = useCallback(() => sendJsonMessage({
    player: player,
    row: 2,
    side: "Right",
  }), [player]);

  const onPlay = (row, side) => sendJsonMessage({
    player,
    row,
    side
  });


  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  return (
    <div className="App">
      <h1>Side Stacker</h1>
      <h2>Player: {player}</h2>
      <button onClick={handleClickSendMessage}>Send</button>
      <div>The WebSocket is currently {connectionStatus}</div>
      <hr />
      {lastJsonMessage?.board ? <Board board={lastJsonMessage.board} onPlay={onPlay} result={lastJsonMessage.result}/> : null}
    </div>
  );
}

export default Game;
