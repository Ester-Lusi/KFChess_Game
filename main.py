
import sys
from parsers.board_parser import BoardParser


def main() -> None:
    try:
        input_lines = sys.stdin.readlines()
        if not input_lines:
            return
            
        board = BoardParser.parse_from_string(input_lines)
        sys.stdout.write(board.to_canonical_string() + "\n")
        
    except ValueError as e:
        # הדפסת הודעת שגיאה והחזרת קוד יציאה 
        sys.stdout.write(str(e) + "\n")
        sys.exit(0)

if __name__ == "__main__":
    main()