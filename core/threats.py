
def is_in_check(board, color: str) -> bool:
    king_pos = board.find_king(color)
    if not king_pos:
        return False

    opponent_color = 'b' if color == 'w' else 'w'
    return board.is_square_attacked(king_pos, opponent_color)

def is_checkmate(board, color: str) -> bool:
    if not is_in_check(board, color):
        return False
    for start, end in board.get_all_legal_moves(color):
        if not would_be_in_check_after_move(board, (start, end), color):
            return False
    return True

def would_be_in_check_after_move(board, move, color: str) -> bool:
    temp_board = board.clone()
    temp_board.execute_move(move)
    return is_in_check(temp_board, color)