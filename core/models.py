
from dataclasses import dataclass

# בעתיד נוכל להוסיף כאן שדות נוספים כמו צבע החלקה, סוג החלקה, או אסטרטגיות תנועה
@dataclass(frozen=True)
class Position:
    row: int
    col: int
from dataclasses import dataclass

@dataclass(frozen=True)
class Piece:
    symbol: str  

    # פונקציה שמחזירה את צבע החלקה (לבן או שחור) על סמך הסימול שלה
    @property
    def color(self) -> str:
        return self.symbol[0] if len(self.symbol) > 0 else ""

    # פונקציה שמחזירה את סוג החלקה (מלך, צריח, רץ, מלכה, פרש) על סמך הסימול שלה
    @property
    def type(self) -> str:
        return self.symbol[1].lower() if len(self.symbol) > 1 else ""

# פונקציה שמבצעת בדיקה אם תנועת החלקה חוקית בהתאם לסוג החלקה
def is_legal_move(piece_type: str, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
    # חישוב ההבדלים בין המיקום ההתחלתי למיקום הסופי
    dr = abs(end_row - start_row)
    dc = abs(end_col - start_col)
    
    # מהלך של 0 משבצות אינו חוקי לתנועה
    if dr == 0 and dc == 0:
        return False

    p_type = piece_type.lower()

    # המלך נע משבצת אחת לכל כיוון
    if p_type == 'k':  
        return dr <= 1 and dc <= 1
    
    # הצריח נע רק בשורות או בעמודות
    elif p_type == 'r': 
        return dr == 0 or dc == 0

    # הרץ נע רק באלכסונים
    elif p_type == 'b':  
        return dr == dc

    # המלכה נעה כמו צריח או רץ (ישר או אלכסון)
    elif p_type == 'q': 
        return (dr == 0 or dc == 0) or (dr == dc)

    # L הפרש נע בצורת  
    elif p_type == 'n': 
        return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)

    return False