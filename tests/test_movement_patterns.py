# tests/test_movement_patterns.py
import unittest
from core.models import is_legal_move, Position, Piece
from core.board import TextGridBoardAdapter
from core.clock import SimulatedClock
from core.game_controller import RealTimeGameController

# בדיקה של חוקיות המהלכים עבור כלים שונים במשחק השחמט
class TestMovementPatterns(unittest.TestCase):

    def test_king_movement(self):
        # מלך נע משבצת אחת - חוקי
        self.assertTrue(is_legal_move('k', 4, 4, 5, 5))
        self.assertTrue(is_legal_move('k', 4, 4, 4, 5))
        # מלך נע שתי משבצות - לא חוקי
        self.assertFalse(is_legal_move('k', 4, 4, 4, 6))
        self.assertFalse(is_legal_move('k', 4, 4, 6, 6))

    def test_rook_movement(self):
        # צריח נע קו ישר - חוקי
        self.assertTrue(is_legal_move('r', 0, 0, 0, 5))
        self.assertTrue(is_legal_move('r', 0, 0, 7, 0))
        # צריח נע באלכסון - לא חוקי
        self.assertFalse(is_legal_move('r', 0, 0, 3, 3))

    def test_bishop_movement(self):
        # רץ נע באלכסון - חוקי
        self.assertTrue(is_legal_move('b', 2, 2, 5, 5))
        self.assertTrue(is_legal_move('b', 2, 5, 5, 2))
        # רץ נע ישר - לא חוקי
        self.assertFalse(is_legal_move('b', 2, 2, 2, 5))

    def test_queen_movement(self):
        # מלכה נעה ישר ובאלכסון - חוקי
        self.assertTrue(is_legal_move('q', 3, 3, 3, 7))
        self.assertTrue(is_legal_move('q', 3, 3, 7, 7))
        # מלכה נעה במהלך לא מוגדר (כמו פרש) - לא חוקי
        self.assertFalse(is_legal_move('q', 3, 3, 5, 4))

    def test_knight_movement(self):
        # L פרש נע בצורת  - חוקי
        self.assertTrue(is_legal_move('n', 4, 4, 6, 5))
        self.assertTrue(is_legal_move('n', 4, 4, 5, 6))
        # פרש נע ישר או אלכסון רגיל - לא חוקי
        self.assertFalse(is_legal_move('n', 4, 4, 4, 6))
        self.assertFalse(is_legal_move('n', 4, 4, 6, 6))


    # כדי לוודא שהכלי לא נתקע מהלוח במקרה של ניסיון לבצע מהלך לא חוקי, נבצע בדיקה אינטגרטיבית עם הקונטרולר
    def test_controller_ignores_illegal_move(self):
        board = TextGridBoardAdapter(rows=8, cols=8)
    
        king_piece = Piece(piece_type='k', color='w')
        object.__setattr__(king_piece, 'symbol', 'wK') 
        
        start_pos = Position(row=4, col=4)
        board.set_piece(start_pos, king_piece)

        clock = SimulatedClock()
        controller = RealTimeGameController(board, clock)
        
        controller.handle_cell_click(start_pos)
        self.assertEqual(controller._selected_position, start_pos)
        
        illegal_target_pos = Position(row=4, col=6)
        controller.handle_cell_click(illegal_target_pos)
        
        self.assertEqual(len(controller._pending_moves), 0)

        self.assertIsNone(controller._selected_position)
        
        self.assertEqual(board.get_piece(start_pos), king_piece)

if __name__ == '__main__':
    unittest.main()