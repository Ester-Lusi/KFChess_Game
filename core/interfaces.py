
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from core.models import Position, Piece


# ממשק לתיאור הלוח
class IBoardRepresentation(ABC):
    @abstractmethod
    # אם החלקה היא אינה = להסיר את החלקה מהלוח, אחרת להוסיף את החלקה למיקום הנתון 
    def set_piece(self, position: Position, piece: Optional[Piece]) -> None:
        pass

    @abstractmethod
    # מחזיר את החלקה אם לא נתונה כזו
    def get_piece(self, position: Position) -> Optional[Piece]:
        pass

    @abstractmethod
    # מחזיר את הממדים של הלוח (שורות, עמודות)
    def get_dimensions(self) -> Tuple[int, int]:   
        pass

    @abstractmethod
    # בודק האם המיקום הנתון נמצא בתוך גבולות הלוח
    def is_within_bounds(self, position: Position) -> bool:     
        pass

    @abstractmethod
    # מחזיר מחרוזת שמייצגת את הלוח בצורה קנונית 
    def to_canonical_string(self) -> str:
        pass

    @property
    @abstractmethod
    # מחזיר את מצב השגיאה הנוכחי של הלוח, אם קיים
    def error_state(self) -> Optional[str]:
        pass


# ממשק לתיאור השעון = זמן המשחק
class IClock(ABC):
    @abstractmethod
    # מעביר את הזמן קדימה במספר מילישניות הנתון
    def advance(self, ms: int) -> None:
        pass

    @abstractmethod
    # מחזיר את הזמן הנוכחי במילישניות
    def get_current_time(self) -> int:
        pass


# ממשק לתיאור הבקר של המשחק
class IGameController(ABC):
    @abstractmethod
    # על הלוח (x, y) מטפל בלחיצה על המיקום הנתון  
    def handle_click(self, x: int, y: int) -> None:    
        pass

    @abstractmethod
    # מטפל בהמתנה של מספר מילישניות הנתון
    def handle_wait(self, ms: int) -> None:     
        pass

    @abstractmethod
    # מדפיס את הלוח הנוכחי
    def print_board(self) -> None: 
        pass