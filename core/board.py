from typing import Tuple, Optional, List
from core.interfaces import IBoardRepresentation
from core.models import Position, Piece
from config.constants import EMPTY_CELL, SPACE, NEWLINE

class TextGridBoardAdapter(IBoardRepresentation):

    # ייצוג פנימי של הלוח כטבלת טקסט דו-ממדית
    def __init__(self, rows: int, cols: int, error_state: Optional[str] = None):
        self._rows = rows
        self._cols = cols

        self._grid: List[List[Optional[Piece]]] = [[None for _ in range(cols)] for _ in range(rows)]
        self._error_state = error_state


    # IBoardRepresentation יישום של הממשק 
    def set_piece(self, position: Position, piece: Optional[Piece]) -> None:
        if self.is_within_bounds(position):
            self._grid[position.row][position.col] = piece


    # IBoardRepresentation יישום של הממשק 
    def get_piece(self, position: Position) -> Optional[Piece]:
        if not self.is_within_bounds(position):
            return None
        return self._grid[position.row][position.col]


    # IBoardRepresentation יישום של הממשק 
    def get_dimensions(self) -> Tuple[int, int]:
        return self._rows, self._cols


    def is_within_bounds(self, position: Position) -> bool:
        return 0 <= position.row < self._rows and 0 <= position.col < self._cols


    @property
    def error_state(self) -> Optional[str]:
        return self._error_state


    # IBoardRepresentation יישום של הממשק 
    def to_canonical_string(self) -> str:
        if self._error_state:
            return self._error_state

        lines = []
        for row in self._grid:
            row_str = SPACE.join(
                (piece.symbol if piece else EMPTY_CELL) for piece in row
            )
            lines.append(row_str)
        return NEWLINE.join(lines)