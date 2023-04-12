import BoardPiece from "./BoardPiece";
import BoardSide from "./BoardSide";

function Board({boardState, onPlay}) {
  const disabled = (row) => {
    if (boardState.state === "Finished") return true;
    return row.every(e => e !== "_");
  }

  return (
    <div>
      {boardState.board.map((row, rowIdx) => (
        <div key={rowIdx}>
          <BoardSide onClick={() => onPlay(rowIdx, "Left")} side="Left" disabled={disabled(row)}/>
            {row.map((piece, pieceIdx) => (
              <BoardPiece key={pieceIdx} piece={piece} />
            ))}
          <BoardSide onClick={() => onPlay(rowIdx, "Right")} side="Right" disabled={disabled(row)}/>
        </div>
      ))}
    </div>
  );
}

export default Board;
