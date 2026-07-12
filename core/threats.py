
from core.models import Position
from core.move_validation import is_legal_move


# פונקציה שבודקת אם המלך במצב של שח
def is_in_check(board, color: str) -> bool:
    if hasattr(board, 'find_king'):
        king_pos = board.find_king(color)
    else:
        king_pos = None
        for r in range(getattr(board, 'height', 8)):
            for c in range(getattr(board, 'width', 8)):
                pos = Position(r, c)
                piece = board.get_piece(pos)
                if piece and piece.type.upper() == 'K' and piece.color == color:
                    king_pos = pos
                    break
            if king_pos:
                break

    if not king_pos:
        return False

    opponent_color = 'b' if color == 'w' else 'w'
    
    # בדיקה האם המשבצת של המלך מאוימת על ידי כלי יריב
    if hasattr(board, 'is_square_attacked'):
        return board.is_square_attacked(king_pos, opponent_color)
    else:
        # סריקה ידנית של הלוח לבדיקת איומים של כלי היריב על משבצת המלך
        for r in range(getattr(board, 'height', 8)):
            for c in range(getattr(board, 'width', 8)):
                pos = Position(r, c)
                piece = board.get_piece(pos)
                if piece and piece.color == opponent_color:
                    if is_legal_move(pos, king_pos, board):
                        return True
        return False

def is_checkmate(board, color: str) -> bool:
    if not is_in_check(board, color):
        return False
        
    # שליפת כל המהלכים הפוטנציאליים של השחקן
    if hasattr(board, 'get_all_legal_moves'):
        moves = board.get_all_legal_moves(color)
    else:
        moves = []
        for r1 in range(getattr(board, 'height', 8)):
            for c1 in range(getattr(board, 'width', 8)):
                start = Position(r1, c1)
                piece = board.get_piece(start)
                if piece and piece.color == color:
                    for r2 in range(getattr(board, 'height', 8)):
                        for c2 in range(getattr(board, 'width', 8)):
                            end = Position(r2, c2)
                            if is_legal_move(start, end, board):
                                moves.append((start, end))

    for start, end in moves:
        if not would_be_in_check_after_move(board, (start, end), color):
            return False
    return True


# פונקציה שבודקת אם המהלך לא יגרום למלך להיות במצב של שח לאחר ביצועו
def would_be_in_check_after_move(board, move, color: str) -> bool:
    if hasattr(board, 'clone'):
        temp_board = board.clone()
        temp_board.execute_move(move)
        return is_in_check(temp_board, color)
    else:
        # במידה והלוח לא מומש נבצע את המהלך זמנית ונבדוק אם המלך במצב שח
        start, end = move
        moving_piece = board.get_piece(start)
        target_piece = board.get_piece(end)
        
        # ביצוע המהלך זמנית
        if hasattr(board, 'set_piece'):
            board.set_piece(start, None)
            board.set_piece(end, moving_piece)
            
        in_check = is_in_check(board, color)
        
        # החזרת המצב לקדמותו (Rollback)
        if hasattr(board, 'set_piece'):
            board.set_piece(start, moving_piece)
            board.set_piece(end, target_piece)
            
        return in_check