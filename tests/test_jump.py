from core.models import Position, Piece
from core.game_controller import RealTimeGameController
from core.board import TextGridBoardAdapter
from core.clock import SimulatedClock


def test_jump_capture_logic():
    board = TextGridBoardAdapter(8, 8)
    clock = SimulatedClock()
    controller = RealTimeGameController(board, clock)
    
    pos_a = Position(0, 0)
    pos_b = Position(0, 1)
    
    piece_a = Piece('P', 'w')
    piece_b = Piece('P', 'b')
    board.set_piece(pos_a, piece_a)
    board.set_piece(pos_b, piece_b)
    
    controller.request_jump(pos_a)
    
    # הזרקת תנועת אויב
    controller._pending_moves.append({
        'piece': piece_b,
        'start': pos_b,
        'end': pos_a,
        'arrival_time': clock.get_current_time() + 800
    })
    
    controller.handle_wait(500) 
    
    # Airborne בדיקה שהכלי הלבן עדיין שם ושהוא במצב 
    current_piece_at_a = board.get_piece(pos_a)
    assert current_piece_at_a is not None
    assert current_piece_at_a.color == 'w'
    assert current_piece_at_a.is_airborne == True

    assert board.get_piece(pos_b) is None