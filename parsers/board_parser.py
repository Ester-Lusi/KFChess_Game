from typing import List
from core.interfaces import IBoardRepresentation
from core.board import TextGridBoardAdapter
from core.models import Position, Piece
from config.constants import (
    EMPTY_CELL, 
    ERROR_UNKNOWN_TOKEN, 
    ERROR_ROW_WIDTH_MISMATCH, 
    VALID_COLORS, 
    VALID_PIECES
)

class BoardParser:

    # IBoardRepresentation מחלקה זו אחראית על ניתוח מחרוזת קלט המייצגת לוח משחק והמרתה לאובייקט המממש את הממשק 
    @staticmethod
    def parse_from_string(lines: List[str]) -> IBoardRepresentation:
        board_lines: List[List[str]] = []
        in_board_section = False

        # סינון שורות הלוח מתוך קלט הפלטפורמה המכיל כותרות ופקודות
        for line in lines:
            cleaned = line.strip()
            if not cleaned:
                continue
            if cleaned.startswith("Board:"):
                in_board_section = True
                continue
            if cleaned.startswith("Commands:"):
                in_board_section = False
                continue
            
            if in_board_section:
                board_lines.append(cleaned.split())

        # פתרון גיבוי למקרה שהקלט מגיע ללא כותרות
        if not board_lines:
            for line in lines:
                cleaned = line.strip()
                if cleaned and not cleaned.startswith("Commands:") and cleaned != "print board":
                    board_lines.append(cleaned.split())

        num_rows = len(board_lines)
        num_cols = len(board_lines[0]) if num_rows > 0 else 0

        # בדיקת תקינות מימדי הלוח
        if not all(len(row) == num_cols for row in board_lines):
            raise ValueError(ERROR_ROW_WIDTH_MISMATCH)


        # יצירת הלוח דרך הממשק האבסטרקטי
        board: IBoardRepresentation = TextGridBoardAdapter(num_rows, num_cols)
        for r_idx, row in enumerate(board_lines):
            for c_idx, cell in enumerate(row):
                if cell == EMPTY_CELL:
                    continue
                
                # ולידציהשל תו הלוח: בדיקה אם התו מייצג צבע וחלק חוקיים
                if len(cell) != 2 or cell[0] not in VALID_COLORS or cell[1] not in VALID_PIECES:
                    raise ValueError(ERROR_UNKNOWN_TOKEN)
                
                board.set_piece(Position(r_idx, c_idx), Piece(symbol=cell))

        return board