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


    # מחזיר את ייצוג הלוח כמחרוזת קנונית
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
    

    # יוצר עותק של הלוח הנוכחי
    def clone(self) -> 'TextGridBoardAdapter':
        new_board = TextGridBoardAdapter(self._rows, self._cols)
        for r in range(self._rows):
            for c in range(self._cols):
                new_board.set_piece(Position(r, c), self._grid[r][c])
        return new_board


    #מוצא את מיקום המלך של הצבע הנתון על הלוח 
    def find_king(self, color: str) -> Optional[Position]:
        for r in range(self._rows):
            for c in range(self._cols):
                piece = self._grid[r][c]
                if piece and piece.type.upper() == 'K' and piece.color == color:
                    return Position(r, c)
        return None
    

    # מבצע את המהלך הנתון על הלוח
    def execute_move(self, move: Tuple[Position, Position]) -> None:
        start, end = move
        piece = self.get_piece(start)
        self.set_piece(end, piece)
        self.set_piece(start, None)
        

    # מחזיר את כל המהלכים החוקיים עבור הצבע הנתון
    def get_all_legal_moves(self, color: str) -> List[Tuple[Position, Position]]:
        from core.move_validation import is_legal_move
        moves = []
        for r in range(self._rows):
            for c in range(self._cols):
                start = Position(r, c)
                piece = self.get_piece(start)
                
                # סינון לפי צבע השחקן
                if piece and piece.color == color:
                    for tr in range(self._rows):
                        for tc in range(self._cols):
                            end = Position(tr, tc)
                            # סינון מהלכים לפי חוקיות בלבד
                            if is_legal_move(start, end, self):
                                moves.append((start, end))
        return moves


    # בודק אם הריבוע הנתון מותקף על ידי היריב
    def is_square_attacked(self, position: Position, opponent_color: str) -> bool:
        from core.move_validation import is_legal_move
        
        for r in range(self._rows):
            for c in range(self._cols):
                start_pos = Position(r, c)
                piece = self.get_piece(start_pos)
                
                # השוואה מדויקת של צבע היריב ('w' או 'b')
                if piece is not None and piece.color == opponent_color:
                    if is_legal_move(start_pos, position, self):
                        return True
        return False