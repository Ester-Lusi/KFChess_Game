import sys
from typing import Optional, List, Tuple, Dict, Any
from config.constants import CELL_PIXEL_SIZE
from core.interfaces import IClock, IGameController, IBoardRepresentation
from core.models import Position, Piece
from core.models import is_legal_move

# ממשק הבקר של המשחק שמבצע את הלוגיקה של ניהול המשחק בזמן אמת
class RealTimeGameController(IGameController):

    # יוצר מופע של הבקר עם לוח משחק ושעון נתונים
    def __init__(self, board: IBoardRepresentation, clock: IClock) -> None:
        self._board = board
        self._clock = clock
        self._selected_position: Optional[Position] = None
        # רשימת המהלכים שממתינים להגעה ליעד (הכלי, מיקום התחלה, מיקום סוף, זמן הגעה במילישניות)
        self._pending_moves: List[Tuple[Piece, Position, Position, int]] = []

    # פונקציה שקולטת לחיצה, מתקפת אותה וממיר אותה למיקום המשבצת בלוח
    def handle_click(self, x: int, y: int) -> None:
        # בדיקה שהלוח אינו במצב שגיאה ושקואורדינטות הלחיצה תקינות
        if self._board.error_state or x < 0 or y < 0:
            return

        # המרת פיקסלים לאינדקס משבצת (שורה ועמודה)
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
        # מקרה 1: אין כלי נבחר כרגע
        if self._selected_position is None:
            piece = self._board.get_piece(target_pos)
            if piece is not None:
                self._selected_position = target_pos  
                sys.stderr.write(f"[DEBUG ERROR] Selected piece {piece.type} at ({target_pos.row}, {target_pos.col})\n")
            return  

        # מקרה 2: יש כבר כלי נבחר, הלחיצה הנוכחית היא תא היעד
        current_piece = self._board.get_piece(self._selected_position)
        if current_piece is None:
            self._selected_position = None
            return

        # בדיקה האם השחקן לחץ על כלי אחר שלו (החלפת בחירה)
        target_piece = self._board.get_piece(target_pos)
        if target_piece is not None and target_piece.color == current_piece.color:
            self._selected_position = target_pos
            sys.stderr.write(f"[DEBUG ERROR] Switched selection to {target_piece.type} at ({target_pos.row}, {target_pos.col})\n")
            return

        # בדיקת חוקיות התנועה הבסיסית (לפי דרישות האיטרציה)
        if not is_legal_move(current_piece.type, self._selected_position.row, self._selected_position.col, target_pos.row, target_pos.col):
            # מהלך לא חוקי - נתעלם ממנו ונאפס את הבחירה
            sys.stderr.write(f"[DEBUG ERROR] Illegal move attempted for {current_piece.type} from ({self._selected_position.row}, {self._selected_position.col}) to ({target_pos.row}, {target_pos.col}). Ignored.\n")
            self._selected_position = None  
            return

        # במידה והמהלך חוקי, נבצע את ניתוב המהלך ותזמונו
        sys.stderr.write(f"[DEBUG ERROR] Legal move approved for {current_piece.type}. Routing...\n")
        self._execute_move(self._selected_position, target_pos)
        self._selected_position = None  # איפוס הבחירה לאחר תחילת התנועה

    # מקדם את שעון המשחק ומבצע בפועל מהלכים שתזמון ההגעה שלהם פג
    def handle_wait(self, ms: int) -> None:
        self._clock.advance(ms)
        current_time = self._clock.get_current_time()
        
        # עדכון וביצוע תנועות שהגיע זמן הגעתן לקצה 
        settled = [m for m in self._pending_moves if m[3] <= current_time]
        for piece, _, dst, _ in settled:
            self._board.set_piece(dst, piece)
            sys.stderr.write(f"[DEBUG] Piece {piece.type} arrived at destination ({dst.row}, {dst.col})\n")
            
        # השארת המהלכים שעדיין נמצאים בתנועה 
        self._pending_moves = [m for m in self._pending_moves if m[3] > current_time]

    # הדפסה של הלוח הנוכחי
    def print_board(self) -> None:
        print(self._board.to_canonical_string())

    # פונקציה פנימית שמבצעת את ניתוב המהלך והוספתו לרשימת המהלכים הממתינים
    def _execute_move(self, start: Position, end: Position) -> None:
        # בדיקה אם יש כלי במיקום ההתחלתי
        piece = self._board.get_piece(start)
        if piece is not None:
            # הסרת הכלי ממיקום ההתחלה
            self._board.set_piece(start, None)
            
            # תזמון הגעתו ליעד בעוד 1000 מילישניות מהזמן הנוכחי של השעון
            arrival_time = self._clock.get_current_time() + 1000
            self._pending_moves.append((piece, start, end, arrival_time))