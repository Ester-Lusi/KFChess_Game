
from core.models import Position
from core.interfaces import IBoardRepresentation
from core.threats import would_be_in_check_after_move # הוספת הייבוא

def is_path_clear(start: Position, end: Position, board: IBoardRepresentation) -> bool:
    dr = end.row - start.row
    dc = end.col - start.col
    step_r = (dr // abs(dr)) if dr != 0 else 0
    step_c = (dc // abs(dc)) if dc != 0 else 0
    
    curr_r, curr_c = start.row + step_r, start.col + step_c
    while (curr_r, curr_c) != (end.row, end.col):
        if board.get_piece(Position(curr_r, curr_c)) is not None:
            return False  
        curr_r += step_r
        curr_c += step_c
    return True

def is_legal_move(start: Position, end: Position, board: IBoardRepresentation, check_safety=True) -> bool:
    if not board.is_within_bounds(end):
        return False
        
    moving_piece = board.get_piece(start)
    if not moving_piece:
        return False
        
    target_piece = board.get_piece(end)
    if target_piece and target_piece.color == moving_piece.color:
        return False
        
    dr = abs(end.row - start.row)
    dc = abs(end.col - start.col)
    piece_type = moving_piece.type.upper()

    # בדיקת חוקיות בסיסית לפי סוג כלי
    move_is_valid = False
    if piece_type == 'K':
        move_is_valid = dr <= 1 and dc <= 1
    elif piece_type == 'Q':
        move_is_valid = (dr == dc or start.row == end.row or start.col == end.col) and is_path_clear(start, end, board)
    elif piece_type == 'R':
        move_is_valid = (start.row == end.row or start.col == end.col) and is_path_clear(start, end, board)
    elif piece_type == 'B': 
        move_is_valid = (dr == dc) and is_path_clear(start, end, board)
    elif piece_type == 'N':
        move_is_valid = (dr == 1 and dc == 2) or (dr == 2 and dc == 1)
    elif piece_type == 'P': 
        direction = -1 if moving_piece.color == 'w' else 1
        if start.col == end.col and (end.row - start.row) == direction:
            move_is_valid = target_piece is None
        elif dr == 1 and dc == 1 and (end.row - start.row) == direction:
            move_is_valid = target_piece is not None and target_piece.color != moving_piece.color
            
    if not move_is_valid:
        return False

    if check_safety:
        if would_be_in_check_after_move(board, (start, end), moving_piece.color):
            return False
            
    return True