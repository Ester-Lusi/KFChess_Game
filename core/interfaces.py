
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from core.models import Position, Piece

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
    def to_canonical_string(self) -> str:
        # מחזיר מחרוזת שמייצגת את הלוח בצורה קנונית 
        pass