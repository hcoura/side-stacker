function Board({board, onPlay, result}) {
  return (
    <div>
      {result ? <div>Player {result} won</div> : null}
      {board.map((row, rowIdx) => (
        <div key={rowIdx}>
          <span onClick={() => onPlay(rowIdx, "Left")}>[</span>
            {row.map((piece, pieceIdx) => (
              <span key={pieceIdx}> {piece} </span>
            ))}
          <span onClick={() => onPlay(rowIdx, "Right")}>]</span>
        </div>
      ))}
    </div>
  );
}

export default Board;
