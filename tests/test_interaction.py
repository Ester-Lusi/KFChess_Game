
from core.models import Position, Piece
from core.clock import SimulatedClock
from core.game_controller import RealTimeGameController

# מחלקה שמדמה את הלוח עבור בדיקות יחידה
class MockBoardRepresentation:

    def __init__(self):
        self.grid = {
            Position(0, 0): Piece(symbol='wK', color='w', type='K'),
            Position(0, 1): Piece(symbol='wP', color='w', type='P'),
            Position(1, 1): None
        }

    def is_within_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < 8 and 0 <= pos.col < 8
    
    def get_piece_at(self, pos: Position):
        return self.grid.get(pos)
    
    def set_piece_at(self, pos: Position, piece):
        self.grid[pos] = piece


# בדיקה של התקדמות השעון המדומה 
def test_clock_advancement():
    clock = SimulatedClock()
    clock.advance(150)
    assert clock.get_current_time() == 150
    clock.advance(50)
    assert clock.get_current_time() == 200


# בדיקה של לחיצה על משבצת עם כלי נבחר
def test_click_selection_and_switch():
    board = MockBoardRepresentation()
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)

    controller.handle_click(50, 50)
    assert controller._selected_position == Position(0, 0)

    controller.handle_click(150, 50)
    assert controller._selected_position == Position(0, 1)


# בדיקה של תנועת לחיצה על משבצת ריקה
def test_click_movement_execution():
    board = MockBoardRepresentation()
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)

    controller.handle_click(150, 50)

    controller.handle_click(150, 150)

    assert board.get_piece_at(Position(0, 1)) is None
    assert board.get_piece_at(Position(1, 1)).symbol == 'wP'
    assert controller._selected_position is None  