from core.models import Position
from core.interfaces import IBoardRepresentation

# פונקציה זו בודקת אם המסלול בין שתי משבצות פנוי מחסימות
def is_path_clear(start: Position, end: Position, board: IBoardRepresentation) -> bool:
    dr = end.row - start.row
    dc = end.col - start.col
    
    # חישוב כיוון הצעד
    step_r = (dr // abs(dr)) if dr != 0 else 0
    step_c = (dc // abs(dc)) if dc != 0 else 0
    
    curr_r, curr_c = start.row + step_r, start.col + step_c
    while (curr_r, curr_c) != (end.row, end.col):
        if board.get_piece(Position(curr_r, curr_c)) is not None:
            return False  
        
        curr_r += step_r
        curr_c += step_c
    return True

# פונקציה זו בודקת אם מהלך מסוים חוקי לפי החוקים הבסיסיים של המשחק
def is_legal_move(start: Position, end: Position, board: IBoardRepresentation) -> bool:
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
    
    if moving_piece.type == 'k':
        return dr <= 1 and dc <= 1
        
    elif moving_piece.type == 'q':
        if not (dr == dc or start.row == end.row or start.col == end.col):
            return False
        return is_path_clear(start, end, board)
        
    elif moving_piece.type == 'r':
        if not (start.row == end.row or start.col == end.col):
            return False
        return is_path_clear(start, end, board)
        
    elif moving_piece.type == 'b': 
        if dr != dc:
            return False
        return is_path_clear(start, end, board)
        
    elif moving_piece.type == 'n':
        return (dr == 1 and dc == 2) or (dr == 2 and dc == 1)
        
    elif moving_piece.type == 'p': 
        direction = -1 if moving_piece.color == 'w' else 1

        if start.col == end.col and (end.row - start.row) == direction:
            return target_piece is None

        if dr == 1 and dc == 1 and (end.row - start.row) == direction:
            return target_piece is not None and target_piece.color != moving_piece.color
            
    return False