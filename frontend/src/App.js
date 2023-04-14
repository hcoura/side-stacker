import { useState } from "react";
import './App.css';
import { useNavigate } from "react-router-dom";

function App() {
  const [inputGameId, setInputGameId] = useState("");
  const navigate = useNavigate();

  const createNewGame = () => {
    fetch('http://localhost:8000/game/new', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      },
    }).then((response) => response.json())
      .then((data) => {
        navigate(`/game/${data.game_id}`);
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
        {" "}<button onClick={() => navigate(`/game/${inputGameId}`)}>Join game</button>
      </div>
    </div>
  );
}

export default App;
