
import sys
from parsers.board_parser import BoardParser

def main() -> None:
    
    # ניתוחו והדפסה החוצה ,stdin -קריאה של קלט מה
    try:
        input_lines = sys.stdin.readlines()
        if not input_lines:
            return
            
        board = BoardParser.parse_from_string(input_lines)
        sys.stdout.write(board.to_canonical_string() + "\n")
        
    except ValueError:
       # הדפסת הודעת שגיאה והחזרת קוד יציאה 1
        sys.stderr.write("Error: Invalid board input.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()