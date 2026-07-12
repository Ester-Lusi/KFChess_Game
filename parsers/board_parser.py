from typing import List
from core.interfaces import IBoardRepresentation
from core.board import TextGridBoardAdapter
from core.models import Position, Piece
from config.constants import EMPTY_CELL, ERROR_INVALID_DIMENSIONS, ERROR_EMPTY_INPUT

class BoardParser:
    @staticmethod
    def parse_from_string(lines: List[str]) -> IBoardRepresentation:
        board = None
        # רשימה זמנית לאחסון שורות לוח טקסטואליות למקרה שלא היו פקודות ADD_PIECE
        raw_board_lines = []

        for line in lines:
            cleaned = line.strip()
            if cleaned.startswith("Commands:"):
                break
            
            if cleaned.startswith("INIT_BOARD"):
                parts = cleaned.split()
                rows, cols = int(parts[1]), int(parts[2])
                board = TextGridBoardAdapter(rows, cols)
            
            elif cleaned.startswith("ADD_PIECE"):
                if board:
                    parts = cleaned.split()
                    r, c, symbol = int(parts[1]), int(parts[2]), parts[3]
                    board.set_piece(Position(r, c), Piece.from_symbol(symbol))
            
            # אם השורה היא שורת לוח (לא פקודה)
            elif cleaned and not cleaned.startswith(("Board:", "INIT_BOARD", "ADD_PIECE")):
                raw_board_lines.append(cleaned.split())
        
        # אם הלוח לא נוצר ע"י INIT_BOARD, צור אותו מהשורות הטקסטואליות
        if board is None:
            if not raw_board_lines:
                raise ValueError(ERROR_EMPTY_INPUT)
            rows = len(raw_board_lines)
            cols = len(raw_board_lines[0])
            board = TextGridBoardAdapter(rows, cols)
            for r_idx, row in enumerate(raw_board_lines):
                for c_idx, cell in enumerate(row):
                    if cell != EMPTY_CELL:
                        board.set_piece(Position(r_idx, c_idx), Piece.from_symbol(cell))
            
        return board