
from core.models import Position

def find_king(board, color: str) -> Position:
    if hasattr(board, 'find_king'):
        return board.find_king(color)
    for r in range(getattr(board, 'height', 8)):
        for c in range(getattr(board, 'width', 8)):
            pos = Position(r, c)
            piece = board.get_piece(pos)
            if piece and piece.type.upper() == 'K' and piece.color == color:
                return pos
    return None

def is_in_check(board, color: str) -> bool:
    from core.move_validation import is_legal_move # ייבוא מקומי
    king_pos = find_king(board, color)
    if not king_pos: return False

    opponent_color = 'b' if color == 'w' else 'w'
    
    if hasattr(board, 'is_square_attacked'):
        return board.is_square_attacked(king_pos, opponent_color)
    
    for r in range(getattr(board, 'height', 8)):
        for c in range(getattr(board, 'width', 8)):
            pos = Position(r, c)
            piece = board.get_piece(pos)
            if piece and piece.color == opponent_color:
                if is_legal_move(pos, king_pos, board, check_safety=False):
                    return True
    return False

def would_be_in_check_after_move(board, move, color: str) -> bool:
    start, end = move
    moving_piece = board.get_piece(start)
    target_piece = board.get_piece(end)
    
    board.set_piece(start, None)
    board.set_piece(end, moving_piece)
    
    in_check = is_in_check(board, color)
    
    board.set_piece(start, moving_piece)
    board.set_piece(end, target_piece)
    
    return in_check

def is_checkmate(board, color: str) -> bool:
    from core.move_validation import is_legal_move 
    
    if not is_in_check(board, color):
        return False
        
    for r1 in range(getattr(board, 'height', 8)):
        for c1 in range(getattr(board, 'width', 8)):
            start = Position(r1, c1)
            piece = board.get_piece(start)
            if piece and piece.color == color:
                for r2 in range(getattr(board, 'height', 8)):
                    for c2 in range(getattr(board, 'width', 8)):
                        end = Position(r2, c2)
                        if is_legal_move(start, end, board, check_safety=False):
                            if not would_be_in_check_after_move(board, (start, end), color):
                                return False
    return True