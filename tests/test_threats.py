
from core.board import TextGridBoardAdapter 
from core.models import Position, Piece
from core.threats import is_in_check, is_checkmate
from core.move_validation import is_legal_move

def test_check_detection():
    board = TextGridBoardAdapter(8, 8)
    board.set_piece(Position(0, 0), Piece('K', 'w'))
    board.set_piece(Position(1, 2), Piece('N', 'b'))
    assert is_in_check(board, "w") == True

def test_checkmate_logic():
    board = TextGridBoardAdapter(8, 8)
    board.set_piece(Position(0, 0), Piece('K', 'b'))
    board.set_piece(Position(0, 2), Piece('Q', 'w'))
    board.set_piece(Position(1, 2), Piece('R', 'w'))
    assert is_checkmate(board, "b") == True

# בדיקה שהמהלך החושף את המלך לשח נדחה
def test_illegal_move_exposing_king():
    board = TextGridBoardAdapter(8, 8)
    board.set_piece(Position(0, 4), Piece('K', 'w'))
    board.set_piece(Position(0, 3), Piece('P', 'w')) # רגלי המגן
    board.set_piece(Position(0, 0), Piece('R', 'b')) # צריח מאיים אם הרגלי יזוז
    
    start = Position(0, 3)
    end = Position(1, 3)

    assert is_legal_move(start, end, board) == False