import './Board.css';

export default function BoardPiece({piece}) {
  let color;
  if (piece === "X") {
    color = "red";
  } else if (piece === "O") {
    color = "blue";
  }

  return (
    <div className="Piece" style={{color}}>{piece}</div>
  )
}