from core.models import Position, Piece
from core.clock import SimulatedClock
from core.game_controller import RealTimeGameController

class MockBoardRepresentation:

    # איתחול לוח מדומה 
    def __init__(self):
        self.grid = {
            Position(0, 0): Piece('K', 'w'),
            Position(0, 1): None,
            Position(1, 1): None
        }
        self._error_state = None 

    def is_square_attacked(self, position: Position, opponent_color: str) -> bool:
        return False

    @property
    def error_state(self): 
        return self._error_state

    def is_within_bounds(self, pos: Position) -> bool: 
        return 0 <= pos.row < 8 and 0 <= pos.col < 8
    
    def get_piece(self, pos: Position): 
        return self.grid.get(pos)
        
    def set_piece(self, pos: Position, piece): 
        self.grid[pos] = piece
        
    def get_dimensions(self): 
        return (8, 8)
        
    def to_canonical_string(self): 
        return ""
        
    def get_piece_at(self, pos: Position): 
        return self.get_piece(pos)
        
    def set_piece_at(self, pos: Position, piece): 
        self.set_piece(pos, piece)


    def clone(self): 
        return MockBoardRepresentation()
    
    def find_king(self, color): 
        return Position(0, 0)
    
    def execute_move(self, move): 
        pass
    
    def get_all_legal_moves(self, color): 
        return []


# פונקציה זו בודקת את תהליך ההתקדמות של השעון המדומה.
def test_clock_advancement():
    clock = SimulatedClock()
    clock.advance(150)
    assert clock.get_current_time() == 150


# פונקציה זו בודקת את תהליך הבחירה וההחלפה של עמדות על הלוח המדומה
def test_click_selection_and_switch():
    board = MockBoardRepresentation()
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)
    controller.handle_click(50, 50) 
    assert controller._selected_position == Position(0, 0)
    
    controller.handle_click(150, 50)  
    assert controller._selected_position is None


# פונקציה זו בודקת את ביצוע תנועת הקליק על הלוח המדומה
def test_click_movement_execution():
    board = MockBoardRepresentation()
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)
    
    controller.handle_click(50, 50) 
    controller.handle_click(150, 50) 

    controller.handle_wait(1000)
    
    assert board.get_piece_at(Position(0, 0)) is None
    assert board.get_piece_at(Position(0, 1)) is not None
    assert board.get_piece_at(Position(0, 1)).type == 'K'


