
from core.models import Position
from core.clock import SimulatedClock
from core.game_controller import RealTimeGameController
from config.constants import STATE_GAME_OVER

class MockPiece:
    def __init__(self, symbol: str, color: str, p_type: str = ""):
        self.symbol = symbol
        self.color = color
        self.type = p_type if p_type else symbol

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
    board = MockBoardRepresentation()
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)

    pawn = MockPiece(symbol="P", color="white")
    rook = MockPiece(symbol="R", color="white")
    board.set_piece(Position(1, 1), pawn)
    board.set_piece(Position(0, 0), rook)

    controller.handle_click(150, 150)
    controller.handle_click(150, 250)
    
    assert len(controller._pending_moves) == 1
    
    controller.handle_click(50, 50) 
    assert controller._selected_position is None
    
    controller.handle_click(50, 150)
    assert len(controller._pending_moves) == 1


def test_zero_cooldown_immediate_subsequent_move():
    board = MockBoardRepresentation()
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)

    pawn = MockPiece(symbol="P", color="white")
    board.set_piece(Position(1, 1), pawn)

    controller.handle_click(150, 150)
    controller.handle_click(150, 250)
    assert len(controller._pending_moves) == 1

    controller.handle_wait(1000)
    assert len(controller._pending_moves) == 0
    assert board.get_piece(Position(2, 1)) == pawn

    controller.handle_click(150, 250)
    controller.handle_click(150, 350)
    
    assert len(controller._pending_moves) == 1
    assert controller._pending_moves[0]['piece'] == pawn
    assert controller._pending_moves[0]['start'] == Position(2, 1)
    assert controller._pending_moves[0]['end'] == Position(3, 1)


def test_king_capture_ends_game():
    board = MockBoardRepresentation()
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)

    attacker = MockPiece(symbol="R", color="white", p_type="R")
    king = MockPiece(symbol="k", color="black", p_type="K")
    
    board.set_piece(Position(0, 0), attacker)
    board.set_piece(Position(0, 1), king)

    # ביצוע אכילה
    controller.handle_click(50, 50) # בחירת הצריח ב-(0,0)
    controller.handle_click(150, 50) # יעד אכילה (0,1)
    
    controller.handle_wait(1000)
    
    # וידוא סיום משחק
    assert controller.game_state == STATE_GAME_OVER
    
    # ניסיון לבצע מהלך נוסף לאחר סיום משחק
    controller.handle_click(150, 50) # בחירת המיקום החדש
    controller.handle_click(150, 150) # ניסיון תנועה
    
    # וידוא שלא התווספו מהלכים עקב חסימת ה-game_state
    assert len(controller._pending_moves) == 0