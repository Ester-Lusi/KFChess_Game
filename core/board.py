
from typing import Tuple, Optional, List
from core.interfaces import IBoardRepresentation
from core.models import Position, Piece
from config.constants import EMPTY_CELL, SPACE, NEWLINE

class TextGridBoardAdapter(IBoardRepresentation):

    # ייצוג פנימי של הלוח כטבלת טקסט דו-ממדית
    def __init__(self, rows: int, cols: int):
        self._rows = rows
        self._cols = cols
        # ייצוג קפסולרי פרטי לחלוטין
        self._grid: List[List[Optional[Piece]]] = [[None for _ in range(cols)] for _ in range(rows)]


    # יישום של הממשק IBoardRepresentation
    def set_piece(self, position: Position, piece: Optional[Piece]) -> None:
        self._grid[position.row][position.col] = piece


    # יישום של הממשק IBoardRepresentation
    def get_piece(self, position: Position) -> Optional[Piece]:
        return self._grid[position.row][position.col]


    # יישום של הממשק IBoardRepresentation
    def get_dimensions(self) -> Tuple[int, int]:
        return self._rows, self._cols


    # יישום של הממשק IBoardRepresentation
    def to_canonical_string(self) -> str:
        lines = []
        for row in self._grid:
            row_str = SPACE.join(
                (piece.symbol if piece else EMPTY_CELL) for piece in row
            )
            lines.append(row_str)
        return NEWLINE.join(lines)