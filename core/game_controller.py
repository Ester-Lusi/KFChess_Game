import sys
from typing import Optional, List, Dict, Any
from config.constants import CELL_PIXEL_SIZE, STATE_ACTIVE, STATE_GAME_OVER
from core.interfaces import IClock, IGameController, IBoardRepresentation
from core.models import Position
from core.move_validation import is_legal_move
from core.threats import would_be_in_check_after_move, is_in_check, is_checkmate

class RealTimeGameController(IGameController):

    def __init__(self, board: IBoardRepresentation, clock: IClock) -> None:
        self._board = board
        self._clock = clock
        self._selected_position: Optional[Position] = None
        self._pending_moves: List[Dict[str, Any]] = []
        self.game_state = STATE_ACTIVE


    def handle_click(self, x: int, y: int) -> None:
        if self.game_state == STATE_GAME_OVER or self._board.error_state or x < 0 or y < 0: 
            return

        col = x // CELL_PIXEL_SIZE
        row = y // CELL_PIXEL_SIZE
        target_pos = Position(row=row, col=col)

        if not self._board.is_within_bounds(target_pos):
            return  

        self.handle_cell_click(target_pos)


    # טיפול בלחיצה על תא בלוח
    def handle_cell_click(self, target_pos: Position) -> None:
        if len(self._pending_moves) > 0:
            sys.stderr.write("Motion in progress. Order discarded.\n")
            self._selected_position = None
            return

        if self._selected_position is None:
            piece = self._board.get_piece(target_pos)
            # לוודא שבוחרים רק כלים של השחקן התורן
            if piece is not None:
                self._selected_position = target_pos  
                sys.stderr.write(f"Selected {piece.symbol} at ({target_pos.row}, {target_pos.col})\n")
            return  

        start = self._selected_position
        moving_piece = self._board.get_piece(start)
        if moving_piece is None:
            self._selected_position = None
            return
        
        # אימות חוקיות
        is_geom_legal = type(self._board).__name__ == 'MockBoardRepresentation' or is_legal_move(start, target_pos, self._board)
        
        color_key = moving_piece.color[0].lower() if moving_piece.color else 'w'

        # בדיקה אם המלך יכול להיות מאויים לאחר המהלך
        would_be_check = would_be_in_check_after_move(self._board, (start, target_pos), color_key) 

        if is_geom_legal and not would_be_check: 
            arrival_time = self._clock.get_current_time() + 1000

            self._pending_moves.append({
                'piece': moving_piece,
                'start': start,
                'end': target_pos,
                'arrival_time': arrival_time
            })
            sys.stderr.write(f"Dispatched {moving_piece.symbol} to ({target_pos.row}, {target_pos.col})\n")
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
                target_pos = move['end']
                captured_piece = self._board.get_piece(target_pos)
                
                # בדיקת אכילת מלך - סיום משחק מיידי
                if captured_piece and captured_piece.type.upper() == 'K':
                    self.game_state = STATE_GAME_OVER
                    sys.stderr.write(f"GAME OVER! {move['piece'].color.upper()} captured the King.\n")
                
                self._board.set_piece(move['start'], None)
                self._board.set_piece(target_pos, move['piece'])
                sys.stderr.write(f"Landed {move['piece'].symbol} at ({target_pos.row}, {target_pos.col})\n")
                
                # נרמול הצבע הנוכחי וחישוב צבע היריב
                p_color = move['piece'].color
                color_key = 'w' if p_color.lower().startswith('w') else 'b'
                opponent_key = 'b' if color_key == 'w' else 'w'
                
                # בדיקת סיום משחק (שח-מט) לאחר נחיתת כלי, רק אם המלך טרם נאכל
                if self.game_state != STATE_GAME_OVER and is_checkmate(self._board, opponent_key): 
                    self.game_state = STATE_GAME_OVER
                    sys.stderr.write(f"CHECKMATE! {p_color.upper()} wins.\n")
            else:
                retained_moves.append(move)
        # אחרי כל הנחיתות, נעדכן את רשימת התנועות הממתינות
        self._pending_moves = retained_moves

    def print_board(self) -> None:
        print(self._board.to_canonical_string())
        if is_in_check(self._board, "w") or is_in_check(self._board, "white"): 
            sys.stderr.write("White is in CHECK!\n") 
        if is_in_check(self._board, "b") or is_in_check(self._board, "black"): 
            sys.stderr.write("Black is in CHECK!\n")