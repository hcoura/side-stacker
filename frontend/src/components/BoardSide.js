import './Board.css';

export default function BoardPiece({side, onClick, disabled}) {
  return (
    <button disabled={disabled} className="Piece" onClick={onClick}>{side === "Left" ? "[" : "]"}</button>
  )
}