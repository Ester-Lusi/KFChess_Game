from core.board import TextGridBoardAdapter 
from core.models import Position, Piece
from core.threats import is_in_check, is_checkmate

# פונקציה שבודקת אם המלך במצב של שח - כלומר אם הוא מאוים על ידי כלי יריב
def test_check_detection():
    board = TextGridBoardAdapter(8, 8)

    board.set_piece(Position(0, 0), Piece('K', 'w'))
    board.set_piece(Position(1, 2), Piece('N', 'b'))

    assert is_in_check(board, "w") == True


# פונקציה זו בודקת אם המלך במצב של מט - כלומר אם הוא מאוים ואין לו מהלכים חוקיים להימלט מהם
def test_checkmate_logic():
    board = TextGridBoardAdapter(8, 8)
    board.set_piece(Position(0, 0), Piece('K', 'b'))
    board.set_piece(Position(0, 2), Piece('Q', 'w'))
    board.set_piece(Position(1, 2), Piece('R', 'w'))

    assert is_checkmate(board, "b") == True