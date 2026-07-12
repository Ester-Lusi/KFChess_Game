import pytest
from core.models import Position
from core.clock import SimulatedClock
from core.game_controller import RealTimeGameController

class MockPiece:
    def __init__(self, symbol: str, color: str):
        self.symbol = symbol
        self.color = color

class MockBoardRepresentation:
    def __init__(self) -> None:
        self.grid = {}
        self.error_state = False

    def is_within_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < 8 and 0 <= pos.col < 8

    def get_piece(self, pos: Position):
        return self.grid.get((pos.row, pos.col), None)

    def set_piece(self, pos: Position, piece) -> None:
        if piece is None:
            if (pos.row, pos.col) in self.grid:
                del self.grid[(pos.row, pos.col)]
        else:
            self.grid[(pos.row, pos.col)] = piece

    def clone(self):
        cloned = MockBoardRepresentation()
        cloned.grid = self.grid.copy()
        cloned.error_state = self.error_state
        return cloned

    def execute_move(self, move) -> None:
        start, target = move
        piece = self.get_piece(start)
        self.set_piece(start, None)
        self.set_piece(target, piece)

    def find_king(self, color: str) -> Position:
        return Position(0, 0)

    def is_square_attacked(self, pos: Position, attacker_color: str) -> bool:
        return False

    def to_canonical_string(self) -> str:
        return "Mock Canonical String"


def test_single_active_motion_and_ignore_redirect():
    """
    כלל 1 + 2: בודק שלא ניתן לבצע מהלך נוסף או לשנות כיוון/ניתוב מחדש 
    של כלי בזמן שיש כבר תנועה פעילה אחת באוויר.
    """
    board = MockBoardRepresentation()
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)

    pawn = MockPiece(symbol="P", color="white")
    rook = MockPiece(symbol="R", color="white")
    board.set_piece(Position(1, 1), pawn)
    board.set_piece(Position(0, 0), rook)

    # מהלך ראשון: בחירה והזנקה של הרגלי מ-(1,1) ל-(2,1) -> (CELL_PIXEL_SIZE = 100)
    controller.handle_click(150, 150)  # קליק ראשון - בחירת הרגלי ב-(1,1)
    controller.handle_click(150, 250)  # קליק שני - הזנקה למשבצת (2,1)
    
    # וידאו שהמהלך הראשון נקלט ונמצא באוויר
    assert len(controller._pending_moves) == 1
    
    # ניסיון הפרה: לחיצה על כלי אחר (הצריח ב-0,0) בזמן שהרגלי עדיין בתנועה
    controller.handle_click(50, 50) 
    
    # וידאו שהבחירה נחסמה והתנקה המצב (Ignore Redirect וביטול בחירה מיידי)
    assert controller._selected_position is None
    
    # ניסיון הפרה נוסף: ניסיון פקודת תנועה נוספת ללא בחירה חוקית
    controller.handle_click(50, 150)
    
    # וידאו שלא התווספו מהלכים חדשים ותור התנועות נשאר על מהלך יחיד מקסימום
    assert len(controller._pending_moves) == 1


def test_zero_cooldown_immediate_subsequent_move():
    """
    כלל 3: בודק שמיד ברגע הגעת הכלי ליעדו וניקוי התנועה הפעילה,
    ניתן לבצע מהלך חדש לחלוטין באותו שבריר שנייה ללא כל השהיית צינון (Zero Cooldown).
    """
    board = MockBoardRepresentation()
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)

    pawn = MockPiece(symbol="P", color="white")
    board.set_piece(Position(1, 1), pawn)

    # שלב א': ביצוע מהלך ראשון מ-(1,1) ל-(2,1)
    controller.handle_click(150, 150)
    controller.handle_click(150, 250)
    assert len(controller._pending_moves) == 1

    # שלב ב': קידום השעון ב-1000 מילישניות לסיום מלא של התנועה ונחיתה אטומית
    controller.handle_wait(1000)
    assert len(controller._pending_moves) == 0
    assert board.get_piece(Position(2, 1)) == pawn

    # שלב ג': ביצוע מיידי של מהלך שני מ-(2,1) ל-(3,1) באותו הרגע ללא שום קולדאון
    controller.handle_click(150, 250)  # בחירה מחדש במיקום הנחיתה החדש
    controller.handle_click(150, 350)  # פקודת תנועה למשבצת הבאה (3,1)
    
    # וידאו שהמהלך השני התקבל ואושר בהצלחה ללא כל שגיאה או חסימת זמן
    assert len(controller._pending_moves) == 1
    assert controller._pending_moves[0]['piece'] == pawn
    assert controller._pending_moves[0]['start'] == Position(2, 1)
    assert controller._pending_moves[0]['end'] == Position(3, 1)