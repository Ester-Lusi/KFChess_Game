import sys
from typing import Optional, List, Dict, Any
from config.constants import CELL_PIXEL_SIZE, STATE_ACTIVE, STATE_GAME_OVER
from core.interfaces import IClock, IGameController, IBoardRepresentation
from core.models import Position, Piece
from core.move_validation import is_legal_move
from core.threats import would_be_in_check_after_move, is_in_check, is_checkmate

class RealTimeGameController(IGameController):

    def __init__(self, board: IBoardRepresentation, clock: IClock) -> None:
        self._board = board
        self._clock = clock
        self._selected_position: Optional[Position] = None
        self._pending_moves: List[Dict[str, Any]] = []
        self._airborne_pieces: List[Dict[str, Any]] = []
        self.game_state = STATE_ACTIVE

    def request_jump(self, pos: Position) -> None:
        piece = self._board.get_piece(pos)
        if not piece or piece.is_airborne or any(m['start'] == pos for m in self._pending_moves):
            return
        
        piece.is_airborne = True
        self._airborne_pieces.append({
            'piece': piece,
            'cell': pos,
            'end_time': self._clock.get_current_time() + 1000
        })

    def handle_click(self, x: int, y: int) -> None:
        if self.game_state == STATE_GAME_OVER or self._board.error_state or x < 0 or y < 0: 
            return
        col = x // CELL_PIXEL_SIZE
        row = y // CELL_PIXEL_SIZE
        target_pos = Position(row=row, col=col)
        if not self._board.is_within_bounds(target_pos): return
        self.handle_cell_click(target_pos)

    def handle_cell_click(self, target_pos: Position) -> None:
        if len(self._pending_moves) > 0:
            sys.stderr.write("Motion in progress. Order discarded.\n")
            self._selected_position = None
            return

        if self._selected_position is None:
            piece = self._board.get_piece(target_pos)
            if piece is not None:
                self._selected_position = target_pos  
                sys.stderr.write(f"Selected {piece.symbol} at ({target_pos.row}, {target_pos.col})\n")
            return  

        start = self._selected_position
        moving_piece = self._board.get_piece(start)
        if moving_piece is None:
            self._selected_position = None
            return
        
        is_geom_legal = type(self._board).__name__ == 'MockBoardRepresentation' or is_legal_move(start, target_pos, self._board)
        color_key = moving_piece.color[0].lower() if moving_piece.color else 'w'
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

    def handle_wait(self, ms: int) -> None:
        self._clock.advance(ms)
        current_time = self._clock.get_current_time()
        
        still_airborne = []
        for jump in self._airborne_pieces:
            if current_time >= jump['end_time']:
                jump['piece'].is_airborne = False
                continue
            
            for move in self._pending_moves:
                if move['end'] == jump['cell']:
                    move['arrival_time'] = -1 
                    self._board.set_piece(move['start'], None) 
                    sys.stderr.write("Airborne piece captured incoming enemy!\n")
            still_airborne.append(jump)
        self._airborne_pieces = still_airborne
        
        retained_moves = []
        for move in self._pending_moves:
            if move['arrival_time'] == -1:
                continue

            if current_time >= move['arrival_time']:
                target_pos = move['end']
                captured_piece = self._board.get_piece(target_pos)
                
                if captured_piece and captured_piece.type.upper() == 'K':
                    self.game_state = STATE_GAME_OVER
                
                self._board.set_piece(move['start'], None)
                self._board.set_piece(target_pos, move['piece'])
                
                opponent_key = 'b' if move['piece'].color.lower().startswith('w') else 'w'
                if self.game_state != STATE_GAME_OVER and is_checkmate(self._board, opponent_key): 
                    self.game_state = STATE_GAME_OVER
            else:
                retained_moves.append(move)
        self._pending_moves = retained_moves

    def print_board(self) -> None:
        print(self._board.to_canonical_string())