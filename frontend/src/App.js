import { useState } from "react";
import './App.css';
import Game from "./Game";

function App() {
  const [gameId, setGameId] = useState("");
  const [inputGameId, setInputGameId] = useState("");

  const createNewGame = () => {
    fetch('http://localhost:8000/game/new', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      },
    }).then((response) => response.json())
      .then((data) => {
        setInputGameId("");
        setGameId(data.game_id);
      })
      .catch((err) => {
        // TODO
        console.log(err.message);
      });
  };

  return (
    <div className="App">
      <h1>Side Stacker</h1>
      <div>
        <button onClick={createNewGame}>New Game</button>
      </div>
      <br />
      <div>
        Game id: <input value={inputGameId} onChange={(e) => setInputGameId(e.target.value)} />
        {" "}<button onClick={() => setGameId(inputGameId)}>Join game</button>
      </div>

      <hr />
      {gameId && <Game gameId={gameId} />}
    </div>
  );
}

export default App;
