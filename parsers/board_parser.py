
from typing import List
from core.interfaces import IBoardRepresentation
from core.board import TextGridBoardAdapter
from core.models import Position, Piece
from config.constants import EMPTY_CELL, ERROR_INVALID_DIMENSIONS, ERROR_EMPTY_INPUT

class BoardParser:
    
    # IBoardRepresentation מחלקה זו אחראית על ניתוח מחרוזת קלט המייצגת לוח משחק והמרתה לאובייקט המממש את הממשק 
    @staticmethod
    def parse_from_string(lines: List[str]) -> IBoardRepresentation:
        # ניקוי רווחים לבנים ושורות ריקות מהקצוות
        cleaned_lines = [line.strip().split() for line in lines if line.strip()]
        
        if not cleaned_lines:
            raise ValueError(ERROR_EMPTY_INPUT)
            
        num_rows = len(cleaned_lines)
        num_cols = len(cleaned_lines[0])
        
        # שמירה על מימדי הלוח: כל השורות חייבות להיות באורך זהה
        if not all(len(row) == num_cols for row in cleaned_lines):
            raise ValueError(ERROR_INVALID_DIMENSIONS)
            
        # יצירת הלוח דרך הממשק האבסטרקטי
        board: IBoardRepresentation = TextGridBoardAdapter(num_rows, num_cols)
        
        for r_idx, row in enumerate(cleaned_lines):
            for c_idx, cell in enumerate(row):
                if cell != EMPTY_CELL:
                    board.set_piece(Position(r_idx, c_idx), Piece(symbol=cell))
                    
        return board