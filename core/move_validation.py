# core/move_validation.py
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

    # לא ניתן לדרוס כלי של אותו צבע
    if target_piece and target_piece.color == moving_piece.color:
        return False
        
    dr = abs(end.row - start.row)
    dc = abs(end.col - start.col)
    
    # כדי להבטיח זיהוי תקין גם אם הוזנו אותיות קטנות או גדולות
    piece_type = moving_piece.type.upper()

    if piece_type == 'K':
        return dr <= 1 and dc <= 1
        
    elif piece_type == 'Q':
        if not (dr == dc or start.row == end.row or start.col == end.col):
            return False
        return is_path_clear(start, end, board)
        
    elif piece_type == 'R':
        if not (start.row == end.row or start.col == end.col):
            return False
        return is_path_clear(start, end, board)
        
    elif piece_type == 'B': 
        if dr != dc:
            return False
        return is_path_clear(start, end, board)
        
    elif piece_type == 'N':
        return (dr == 1 and dc == 2) or (dr == 2 and dc == 1)
        
    elif piece_type == 'P': 
        direction = -1 if moving_piece.color == 'w' else 1

        # תנועה קדימה למשבצת ריקה
        if start.col == end.col and (end.row - start.row) == direction:
            return target_piece is None

        # הכאה באלכסון
        if dr == 1 and dc == 1 and (end.row - start.row) == direction:
            return target_piece is not None and target_piece.color != moving_piece.color
            
    return False