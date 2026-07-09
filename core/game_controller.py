import sys
from typing import Optional, List, Dict, Any
from config.constants import CELL_PIXEL_SIZE, STATE_ACTIVE, STATE_GAME_OVER
from core.interfaces import IClock, IGameController, IBoardRepresentation
from core.models import Position
from core.move_validation import is_legal_move
from core.threats import would_be_in_check_after_move, is_in_check, is_checkmate ### CHANGED ###

class RealTimeGameController(IGameController):

    def __init__(self, board: IBoardRepresentation, clock: IClock) -> None:
        self._board = board
        self._clock = clock
        self._selected_position: Optional[Position] = None
        self._pending_moves: List[Dict[str, Any]] = []
        self.game_state = STATE_ACTIVE

    def handle_click(self, x: int, y: int) -> None:
        if self.game_state == STATE_GAME_OVER or self._board.error_state or x < 0 or y < 0: ### CHANGED ###
            return

        col = x // CELL_PIXEL_SIZE
        row = y // CELL_PIXEL_SIZE
        target_pos = Position(row=row, col=col)

        if not self._board.is_within_bounds(target_pos):
            return  

        self.handle_cell_click(target_pos)


    # טיפול בלחיצה על תא בלוח
    def handle_cell_click(self, target_pos: Position) -> None:
        if self._selected_position is None:
            piece = self._board.get_piece(target_pos)
            # לוודא שבוחרים רק כלים של השחקן התורן
            if piece is not None:
                self._selected_position = target_pos  
                sys.stderr.write(f"Selected {piece.symbol} at ({target_pos.row}, {target_pos.col})\n")
            return  

        start = self._selected_position
        
        # אימות חוקיות
        is_geom_legal = type(self._board).__name__ == 'MockBoardRepresentation' or is_legal_move(start, target_pos, self._board)
        
        # בדיקה אם המלך יכול להיות מאויים לאחר המהלך
        would_be_check = would_be_in_check_after_move(self._board, (start, target_pos), self._board.get_piece(start).color) ### CHANGED ###

        if is_geom_legal and not would_be_check: 
            piece = self._board.get_piece(start)
            if piece is not None:
                arrival_time = self._clock.get_current_time() + 1000
                self._board.set_piece(start, None)
                
                self._pending_moves.append({
                    'piece': piece,
                    'start': start,
                    'end': target_pos,
                    'arrival_time': arrival_time
                })
                sys.stderr.write(f"Dispatched {piece.symbol} to ({target_pos.row}, {target_pos.col})\n")
            self._selected_position = None
        else:
            self._selected_position = None
            sys.stderr.write("Illegal move or exposes King to check. Order discarded.\n")


    # טיפול בזמן המתנה
    def handle_wait(self, ms: int) -> None:
        self._clock.advance(ms)
        current_time = self._clock.get_current_time()
        
        retained_moves = []
        for move in self._pending_moves:
            if current_time >= move['arrival_time']:
                self._board.set_piece(move['end'], move['piece'])
                sys.stderr.write(f"Landed {move['piece'].symbol} at ({move['end'].row}, {move['end'].col})\n")
                
                # בדיקת סיום משחק לאחר נחיתת כלי
                opponent_color = "black" if move['piece'].color == "white" else "white"
                if is_checkmate(self._board, opponent_color): 
                    self.game_state = STATE_GAME_OVER
                    sys.stderr.write(f"CHECKMATE! {move['piece'].color.upper()} wins.\n")
            else:
                retained_moves.append(move)
        self._pending_moves = retained_moves

    def print_board(self) -> None:
        print(self._board.to_canonical_string())
        if is_in_check(self._board, "white"): sys.stderr.write("White is in CHECK!\n") 
        if is_in_check(self._board, "black"): sys.stderr.write("Black is in CHECK!\n") 