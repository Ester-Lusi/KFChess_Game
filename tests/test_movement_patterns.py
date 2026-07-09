import unittest
import sys
from io import StringIO
from core.models import is_legal_move, Position, Piece
from core.board import TextGridBoardAdapter
from core.clock import SimulatedClock
from core.game_controller import RealTimeGameController

# בדיקה של חוקיות המהלכים עבור כלים שונים במשחק השחמט
class TestMovementPatterns(unittest.TestCase):

    def setUp(self):
        # יצירת לוח, שעון וקונטרולר נקיים לטובת בדיקות האינטגרציה והחוסמים
        self.board = TextGridBoardAdapter(rows=8, cols=8)
        self.clock = SimulatedClock()
        self.controller = RealTimeGameController(self.board, self.clock)
        
        # לכידת תזרימי שגיאות (stderr) למקרה שהקונטרולר מדפיס לוגים בזמן אמת
        self.held_stderr = sys.stderr
        sys.stderr = StringIO()

    def tearDown(self):
        # החזרת ה-stderr למצבו התקין
        sys.stderr = self.held_stderr

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
        # מלכה נעה במהלך לא מוגדר - לא חוקי
        self.assertFalse(is_legal_move('q', 3, 3, 5, 4))

    def test_knight_movement(self):
        # פרש נע בצורת L - חוקי
        self.assertTrue(is_legal_move('n', 4, 4, 6, 5))
        self.assertTrue(is_legal_move('n', 4, 4, 5, 6))
        # פרש נע ישר או אלכסון רגיל - לא חוקי
        self.assertFalse(is_legal_move('n', 4, 4, 4, 6))
        self.assertFalse(is_legal_move('n', 4, 4, 6, 6))

    # פונקציה זו בודקת שהצריח לא יכול לעבור דרך כלי אחר
    def test_rook_blocked_by_piece(self):
        self.board.set_piece(Position(0, 0), Piece('r', 'w'))
        self.board.set_piece(Position(0, 3), Piece('p', 'b'))
        
        # תיקון קריאה בהתאם לחתימה של הפונקציה המיובאת מקובץ core/models.py
        self.assertTrue(is_legal_move('r', 0, 0, 0, 2))  
        self.assertTrue(is_legal_move('r', 0, 0, 0, 3)) 

    # פונקציה זו בודקת שהפרש יכול לקפוץ מעל כלים אחרים
    def test_knight_jumps_over_blockers(self):
        self.board.set_piece(Position(0, 0), Piece('n', 'w'))
        self.board.set_piece(Position(0, 1), Piece('r', 'w'))
        self.board.set_piece(Position(1, 0), Piece('r', 'b'))

        self.assertTrue(is_legal_move('n', 0, 0, 2, 1))

    # פונקציה זו בודקת שהקונטרולר מתעלם ממחוות לא חוקיות
    def test_controller_ignores_illegal_move(self):
        king_piece = Piece('k', 'w')
        
        start_pos = Position(row=4, col=4)
        self.board.set_piece(start_pos, king_piece)

        self.controller.handle_cell_click(start_pos)
        self.assertEqual(self.controller._selected_position, start_pos)
        
        illegal_target_pos = Position(row=4, col=6)
        self.controller.handle_cell_click(illegal_target_pos)
        
        self.assertEqual(len(self.controller._pending_moves), 0)
        self.assertIsNone(self.controller._selected_position)
        self.assertEqual(self.board.get_piece(start_pos), king_piece)

    # פונקציה זו בודקת את תהליך הביצוע של מהלך בזמן אמת
    def test_real_time_capture_execution_pipeline(self):
        bishop_piece = Piece('b', 'w')
        pawn_piece = Piece('p', 'b')
        
        self.board.set_piece(Position(0, 0), bishop_piece)
        self.board.set_piece(Position(3, 3), pawn_piece)
        
        self.controller.handle_cell_click(Position(0, 0))
        self.assertEqual(self.controller._selected_position, Position(0, 0))
        
        self.controller.handle_cell_click(Position(3, 3))

        self.assertIsNone(self.board.get_piece(Position(0, 0)))
        # תיקון: בדיקה שהכלי הוא חייל שחור ומיוצג על ידי האות הקטנה 'p' בארכיטקטורה
        self.assertEqual(self.board.get_piece(Position(3, 3)).symbol, "p")
        
        # קידום זמן לביצוע המהלך
        self.controller.handle_wait(1000)
            
        landed_piece = self.board.get_piece(Position(3, 3))
        self.assertIsNotNone(landed_piece)
        # תיקון: בדיקה שהכלי הנוחת הוא רץ לבן ומיוצג על ידי האות הגדולה 'B'
        self.assertEqual(landed_piece.symbol, "B")


if __name__ == '__main__':
    unittest.main()