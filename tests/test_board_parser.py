
import pytest
from core.models import Position
from parsers.board_parser import BoardParser
from config.constants import ERROR_INVALID_DIMENSIONS, ERROR_EMPTY_INPUT

@pytest.mark.parametrize("input_lines, expected_dims, expected_canonical", [
    # לוח שחמט סטנדרטי עם רווחים בין התאים
    (
        [
            "R  .  B  Q  K  B  .  R",
            ".  P  P  P  P  P  P  .",
            ".  .  .  .  .  .  .  .",
            ".  .  .  .  .  .  .  .",
            ".  .  .  .  .  .  .  .",
            ".  .  .  .  .  .  .  .",
            ".  p  p  p  p  p  p  .",
            "r  .  b  q  k  b  .  r"
        ],
        (8, 8),
        "R . B Q K B . R\n. P P P P P P .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. p p p p p p .\nr . b q k b . r"
    ),
    # עם תו יחיד, לוח אחד
    (
        ["K"],
        (1, 1),
        "K"
    ),
    # עם רווחים מיותרים ושורות ריקות
    (
        [
            "   \n",  
            "P . . . P",
            ". K . k .",
            "R . . . R",
            "\n   "   
        ],
        (3, 5),
        "P . . . P\n. K . k .\nR . . . R"
    )
])



def test_parser_valid_inputs(input_lines, expected_dims, expected_canonical):
    # מחזירה אובייקט עם המימדים והייצוג הקנוני הצפוי parse_from_string - בודק שהפונקציה 
    board = BoardParser.parse_from_string(input_lines)
    
    assert board.get_dimensions() == expected_dims
    assert board.to_canonical_string() == expected_canonical


def test_board_encapsulation_and_state():
    # בודק שהלוח שומר על ייצוג פנימי מבודד ושניתן לגשת למידע דרך הממשק בלבד.
    input_lines = [
        "R .",
        ". k"
    ]
    board = BoardParser.parse_from_string(input_lines)
    
    # Models -בדיקת קריאה ישירה מהממשק באמצעות ה
    piece_top_left = board.get_piece(Position(0, 0))
    piece_bottom_right = board.get_piece(Position(1, 1))
    empty_cell = board.get_piece(Position(0, 1))
    
    assert piece_top_left.symbol == "R"
    assert piece_bottom_right.symbol == "k"
    assert empty_cell is None


@pytest.mark.parametrize("invalid_input, expected_error_msg", [
    # מקרה 1: שורות באורכים שונים (לוח לא מלבני)
    (
        [
            ". . .",
            ". .", 
            ". . ."
        ],
        ERROR_INVALID_DIMENSIONS
    ),
    # מקרה 2: קלט המכיל רק שורות ריקות או רווחים
    (
        [
            "   ",
            "\n",
            "   \n"
        ],
        ERROR_EMPTY_INPUT
    ),
    # מקרה 3: רשימת קלט ריקה לחלוטין
    (
        [],
        ERROR_EMPTY_INPUT
    )
])
def test_parser_invalid_inputs_raise_value_error(invalid_input, expected_error_msg):
    # בודק שהפונקציה מעלה שגיאה עבור קלט לא חוקי, ושגיאת הערך תואמת את ההודעה הצפויה
    with pytest.raises(ValueError) as exc_info:
        BoardParser.parse_from_string(invalid_input)
    
    assert str(exc_info.value) == expected_error_msg