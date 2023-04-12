import './App.css';
import React, { useState, useCallback, useEffect } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import Board from "./components/Board";

const WS_URL = 'ws://localhost:8000/ws/game/';

function Game({ gameId }) {
  const [err, setErr] = useState("");

  const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket(`${WS_URL}${gameId}`, {
    onOpen: () => {
      setErr("");
    },
    onError: () => {
      setErr("Invalid Game ID");
    }
  });

  const [boardState, setBoardState] = useState({});
  const [player, setPlayer] = useState("");

  useEffect(() => {
    if (!lastJsonMessage?.board) return;
    setBoardState(lastJsonMessage);
  }, [lastJsonMessage]);

  useEffect(() => {
    if (!lastJsonMessage?.player) return;
    setPlayer(lastJsonMessage.player);
  }, [lastJsonMessage]);

  const onPlay = (row, side) => sendJsonMessage({
    player,
    row,
    side
  });

  return (
    <div className="App">
      {
        err ?
          <h2>Error: {err}</h2> :
          <div>
            <h4>GameId: {gameId}</h4>
            <h4>You're: {player}</h4>
            {boardState?.winner && <h4>{boardState.winner} Won!!!!</h4>}
            <hr />
            {boardState?.board && <Board boardState={boardState} onPlay={onPlay} />}
          </div>
      }
    </div>
  );
}

export default Game;
