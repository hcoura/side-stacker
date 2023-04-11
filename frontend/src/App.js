import { Link } from "react-router-dom";
import './App.css';

// TODO:
  //  Home - New Game / Join Game
  //  GameView (ws stuff)
  //  favicon and stuff
  //  clean repo

function App() {
  return (
    <div className="App">
      {/* <header className="App-header">
        
      </header> */}
      <button><Link to={`game`}>New Game</Link></button>
      <div>
        Game id: <input></input> <button>Join game</button>
      </div>
    </div>
  );
}

export default App;
