
from core.models import Position
from core.clock import SimulatedClock  # תיקון הייבוא לשם המחלקה האמיתי שלך!
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
        for (row, col), piece in self.grid.items():
            if piece and piece.color == color and piece.symbol.upper() == 'K':
                return Position(row, col)
        return Position(0, 0)

    # >>> מתודה חדשה שפותרת את שגיאת ה-is_square_attacked <<<
    def is_square_attacked(self, pos: Position, attacker_color: str) -> bool:
        return False

    def to_canonical_string(self) -> str:
        if not self.grid:
            return "Empty Board"
        return ", ".join([f"{p.symbol}@{r}:{c}" for (r, c), p in self.grid.items()])


# בדיקה של מחזור החיים של תנועת כלי על פני זמן
def test_movement_over_time_lifecycle():
    board = MockBoardRepresentation()
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)

    king = MockPiece(symbol="K", color="white")
    board.set_piece(Position(0, 0), king)

    pawn = MockPiece(symbol="P", color="white")
    start_pos = Position(row=1, col=1)
    dest_pos = Position(row=2, col=1)
    board.set_piece(start_pos, pawn)

    controller._selected_position = start_pos
    controller.handle_cell_click(dest_pos)  
    
    # וידאו שהמהלך נכנס לתור ההמתנה
    assert len(controller._pending_moves) == 1

    controller.handle_wait(500)
    
    # וידוא שהכלי עדיין מוצג ומודפס במיקומו המקורי בלבד
    assert board.get_piece(start_pos) == pawn
    assert board.get_piece(dest_pos) is None
    assert "P@1:1" in board.to_canonical_string()

    controller.handle_wait(600)

    # וידוא שהכלי הוסר מהמיקום המקורי והועבר למיקום החדש
    assert board.get_piece(start_pos) is None
    assert board.get_piece(dest_pos) == pawn
    assert "P@2:1" in board.to_canonical_string()
    assert len(controller._pending_moves) == 0