from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    row: int
    col: int

@dataclass
class Piece:
    type: str
    color: str

    @property
    def symbol(self):
        # מחזיר אות גדולה ללבן ואות קטנה לשחור, ללא תחילית צבע
        return self.type.upper() if self.color == 'w' else self.type.lower()

    @classmethod
    def from_symbol(cls, symbol: str):
        # אם התו הוא אות גדולה, מניחים לבן, אחרת שחור
        if len(symbol) == 1:
            color = 'w' if symbol.isupper() else 'b'
            return cls(type=symbol.upper(), color=color)
        
        # טיפול במקרה של 2 תווים (למשל "wR")
        color = 'w' if symbol[0] == 'w' else 'b'
        p_type = symbol[1]
        return cls(type=p_type.upper(), color=color)

# פונקציה שמבצעת בדיקה אם תנועת החלקה חוקית
def is_legal_move(piece_type: str, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
    dr = abs(end_row - start_row)
    dc = abs(end_col - start_col)
    
    if dr == 0 and dc == 0:
        return False

    p_type = piece_type.lower()

    if p_type == 'k':  
        return dr <= 1 and dc <= 1
    elif p_type == 'r': 
        return dr == 0 or dc == 0
    elif p_type == 'b':  
        return dr == dc
    elif p_type == 'q': 
        return (dr == 0 or dc == 0) or (dr == dc)
    elif p_type == 'n': 
        return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)
    elif p_type == 'p': 
        return dr == 1 and dc == 0
    
    return False