import sys
from config.constants import CMD_CLICK, CMD_WAIT, CMD_PRINT
from core.interfaces import IGameController

# מחלקה שמטפלת בקלט של פקודות מהמשתמש ומעבירה אותן לבקר המשחק
class CommandStreamProcessor:
    def __init__(self, controller: IGameController) -> None:
        self._controller = controller

    # פונקציה זו מעבדת שורה אחת של פקודה ומבצעת את הפעולה המתאימה בבקר המשחק    
    def process_line(self, line: str) -> None:
        clean_line = line.strip()
        if not clean_line or clean_line.startswith("Commands:"):
            return

        if clean_line == CMD_PRINT:
            self._controller.print_board()
            return

        parts = clean_line.split()
        if not parts:
            return

        cmd_type = parts[0]

        if cmd_type == CMD_CLICK and len(parts) == 3:
            try:
                x, y = int(parts[1]), int(parts[2])
                self._controller.handle_click(x, y)
            except ValueError as e:
                # הודעת שגיאה מפורטת לערוץ השגיאות הסטנדרטי
                print(f"[DEBUG ERROR] Invalid integers for click command: '{clean_line}'. Error: {e}", file=sys.stderr)
                pass  

        elif cmd_type == CMD_WAIT and len(parts) == 2:
            try:
                ms = int(parts[1])
                self._controller.handle_wait(ms)
            except ValueError as e:
                # הודעת שגיאה מפורטת לערוץ השגיאות הסטנדרטי
                print(f"[DEBUG ERROR] Invalid integer for wait command: '{clean_line}'. Error: {e}", file=sys.stderr)
                pass
        else:
            # טיפול במצב שבו מבנה הפקודה אינו חוקי 
            if cmd_type in (CMD_CLICK, CMD_WAIT):
                print(f"[DEBUG ERROR] Malformed structural length for command '{cmd_type}'. Line: '{clean_line}'", file=sys.stderr)