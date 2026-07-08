
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from core.models import Position, Piece


# ממשק לתיאור הלוח
class IBoardRepresentation(ABC):
    @abstractmethod
    def set_piece(self, position: Position, piece: Optional[Piece]) -> None:
        # אם החלקה היא אינה = להסיר את החלקה מהלוח, אחרת להוסיף את החלקה למיקום הנתון 
        pass

    @abstractmethod
    def get_piece(self, position: Position) -> Optional[Piece]:
        # מחזיר את החלקה אם לא נתונה כזו
        pass

    @abstractmethod
    def get_dimensions(self) -> Tuple[int, int]:
        # מחזיר את הממדים של הלוח (שורות, עמודות)
        pass

    @abstractmethod
    def is_within_bounds(self, position: Position) -> bool:
        # בודק האם המיקום הנתון נמצא בתוך גבולות הלוח
        pass

    @abstractmethod
    def to_canonical_string(self) -> str:
        # מחזיר מחרוזת שמייצגת את הלוח בצורה קנונית 
        pass

    @property
    @abstractmethod
    def error_state(self) -> Optional[str]:
        # מחזיר את מצב השגיאה הנוכחי של הלוח, אם קיים
        pass


# ממשק לתיאור השעון = זמן המשחק
class IClock(ABC):
    @abstractmethod
    def advance(self, ms: int) -> None:
        # מעביר את הזמן קדימה במספר מילישניות הנתון
        pass

    @abstractmethod
    def get_current_time(self) -> int:
        # מחזיר את הזמן הנוכחי במילישניות
        pass


# ממשק לתיאור הבקר של המשחק
class IGameController(ABC):
    @abstractmethod
    def handle_click(self, x: int, y: int) -> None:
        # על הלוח (x, y) מטפל בלחיצה על המיקום הנתון  
        pass

    @abstractmethod
    def handle_wait(self, ms: int) -> None:
        # מטפל בהמתנה של מספר מילישניות הנתון
        pass

    @abstractmethod
    def print_board(self) -> None:
        # מדפיס את הלוח הנוכחי
        pass