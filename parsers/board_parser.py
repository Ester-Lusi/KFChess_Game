from typing import List
from core.interfaces import IBoardRepresentation
from core.board import TextGridBoardAdapter
from core.models import Position, Piece
from config.constants import EMPTY_CELL, ERROR_INVALID_DIMENSIONS, ERROR_EMPTY_INPUT

class BoardParser:
    @staticmethod
    def parse_from_string(lines: List[str]) -> IBoardRepresentation:
        board_lines = []
        for line in lines:
            cleaned = line.strip()
            # סינון שורות ריקות או כאלו שאינן חלק מהלוח
            if cleaned and not cleaned.startswith(("Board:", "Commands:")) and cleaned != "print board":
                board_lines.append(cleaned.split())
        
        if not board_lines:
            raise ValueError(ERROR_EMPTY_INPUT)
        
        num_rows = len(board_lines)
        num_cols = len(board_lines[0])
        if not all(len(row) == num_cols for row in board_lines):
            raise ValueError(ERROR_INVALID_DIMENSIONS)

        board = TextGridBoardAdapter(num_rows, num_cols)
        for r_idx, row in enumerate(board_lines):
            for c_idx, cell in enumerate(row):
                if cell == EMPTY_CELL:
                    continue
                try:
                    board.set_piece(Position(r_idx, c_idx), Piece.from_symbol(cell))
                except:
                    raise ValueError("ERROR_UNKNOWN_TOKEN")
        return board