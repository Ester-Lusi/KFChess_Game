
from dataclasses import dataclass

# בעתיד נוכל להוסיף כאן שדות נוספים כמו צבע החלקה, סוג החלקה, או אסטרטגיות תנועה
@dataclass(frozen=True)
class Position:
    row: int
    col: int

# בעתיד נוכל להוסיף כאן שדות נוספים כמו צבע החלקה, סוג החלקה, או אסטרטגיות תנועה
@dataclass(frozen=True)
class Piece:
    symbol: str  # 'P' / 'R' / 'k'
    # בעתיד יכיל סוגים נוספים של החלקה, צבע, או תכונות אחרות של החלקה