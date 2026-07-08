import sys
from typing import Optional, List, Tuple
from config.constants import CELL_PIXEL_SIZE
from core.interfaces import IClock, IGameController, IBoardRepresentation
from core.models import Position, Piece

# ממשק הבקר של המשחק שמבצע את הלוגיקה של ניהול המשחק בזמן אמת
class RealTimeGameController(IGameController):
    def __init__(self, board: IBoardRepresentation, clock: IClock) -> None:
        self._board = board
        self._clock = clock
        self._selected_position: Optional[Position] = None
        self._pending_moves: List[Tuple[Piece, Position, Position, int]] = []

    def handle_click(self, x: int, y: int) -> None:
        # בדיקה שהלוח אינו במצב שגיאה ושקואורדינטות הלחיצה תקינות
        if self._board.error_state or x < 0 or y < 0:
            return

        # המרת פיקסלים לאינדקס משבצת 
        col = x // CELL_PIXEL_SIZE
        row = y // CELL_PIXEL_SIZE
        target_pos = Position(row=row, col=col)

        # לוודא שהלחיצה היא בתחומי הלוח
        if not self._board.is_within_bounds(target_pos):
            return  

        # מקרה 1: אין כלי נבחר כרגע 
        piece = self._board.get_piece(target_pos)

        if self._selected_position is None:
            if piece is not None:
                self._selected_position = target_pos  
            return  

        # מקרה 2: יש כבר כלי נבחר
        current_piece = self._board.get_piece(self._selected_position)
        
        if current_piece is not None:
            if piece is not None and piece.color == current_piece.color:
                self._selected_position = target_pos
            else:
                self._execute_move(self._selected_position, target_pos)
                self._selected_position = None  # איפוס הבחירה לאחר ניסיון תנועה

    # מטפל בהמתנה של מספר מילישניות הנתון
    def handle_wait(self, ms: int) -> None:
        self._clock.advance(ms)
        current_time = self._clock.get_current_time()
        
        # עדכון וביצוע תנועות שהגיע זמן הגעתן לקצה
        settled = [m for m in self._pending_moves if m[3] <= current_time]
        for piece, _, dst, _ in settled:
            self._board.set_piece(dst, piece)
            
        self._pending_moves = [m for m in self._pending_moves if m[3] > current_time]

    # מדפיס את הלוח הנוכחי
    def print_board(self) -> None:
        print(self._board.to_canonical_string())

    # מבצע תנועה פיזית על הלוח (בשלב זה תנועה ישירה ללא הגבלת חוקים)
    def _execute_move(self, start: Position, end: Position) -> None:
        piece = self._board.get_piece(start)
        if piece is not None:
            # הסרת הכלי ממיקום ההתחלה ותזמון הגעתו ליעד בעוד 1000 מילישניות
            self._board.set_piece(start, None)
            arrival_time = self._clock.get_current_time() + 1000
            self._pending_moves.append((piece, start, end, arrival_time))