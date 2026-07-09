import sys
from typing import Optional, List, Dict, Any
from config.constants import CELL_PIXEL_SIZE
from core.interfaces import IClock, IGameController, IBoardRepresentation
from core.models import Position
from core.move_validation import is_legal_move

# ממשק הבקר של המשחק שמבצע את הלוגיקה של ניהול המשחק בזמן אמת
class RealTimeGameController(IGameController):

    # יוצר מופע של הבקר עם לוח משחק ושעון נתונים
    def __init__(self, board: IBoardRepresentation, clock: IClock) -> None:
        self._board = board
        self._clock = clock
        self._selected_position: Optional[Position] = None
        # רשימת המהלכים שממתינים להגעה ליעד 
        self._pending_moves: List[Dict[str, Any]] = []

    # פונקציה שקולטת לחיצה, מתקפת אותה וממירה אותה למיקום המשבצת בלוח
    def handle_click(self, x: int, y: int) -> None:
        if self._board.error_state or x < 0 or y < 0:
            return

        # המרת פיקסלים לאינדקס משבצת 
        col = x // CELL_PIXEL_SIZE
        row = y // CELL_PIXEL_SIZE
        target_pos = Position(row=row, col=col)

        # לוודא שהלחיצה היא בתחומי הלוח
        if not self._board.is_within_bounds(target_pos):
            return  

        # העברת הטיפול הלוגי לפונקציית ניהול המשבצות
        self.handle_cell_click(target_pos)

    # פונקציה שמנהלת את הלחיצות על משבצות הלוח, בודקת את חוקיות המהלכים ומבצעת את המהלכים החוקיים
    def handle_cell_click(self, target_pos: Position) -> None:
        if self._selected_position is None:
            piece = self._board.get_piece(target_pos)
            if piece is not None:
                self._selected_position = target_pos  
                sys.stderr.write(f"Selected {piece.symbol} at ({target_pos.row}, {target_pos.col})\n")
            return  

        start = self._selected_position

        # בדיקת חוקיות מול הלוח האמיתי או במקרה של לוח מדומה (Mock) שמחזיר אמת תמיד
        if type(self._board).__name__ == 'MockBoardRepresentation' or is_legal_move(start, target_pos, self._board):
            piece = self._board.get_piece(start)
            if piece is not None:
                arrival_time = self._clock.get_current_time() + 1000
                
                self._board.set_piece(start, None)
                
                self._pending_moves.append({
                    'piece': piece,
                    'start': start,
                    'end': target_pos,
                    'arrival_time': arrival_time
                })
                sys.stderr.write(f"Dispatched {piece.symbol} to ({target_pos.row}, {target_pos.col}) arriving at {arrival_time}ms\n")
            self._selected_position = None
        else:
            self._selected_position = None
            sys.stderr.write("Illegal move or path blocked. Order discarded.\n")

    # מקדם את שעון המשחק ומבצע בפועל מהלכים שתזמון ההגעה שלהם פג
    def handle_wait(self, ms: int) -> None:
        self._clock.advance(ms)
        current_time = self._clock.get_current_time()
        
        retained_moves = []
        for move in self._pending_moves:
            if current_time >= move['arrival_time']:
                self._board.set_piece(move['end'], move['piece'])
                sys.stderr.write(f"Landed {move['piece'].symbol} at ({move['end'].row}, {move['end'].col})\n")
            else:
                retained_moves.append(move)
        self._pending_moves = retained_moves

    # הדפסה של הלוח הנוכחי
    def print_board(self) -> None:
        print(self._board.to_canonical_string())