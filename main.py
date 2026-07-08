import sys
from parsers.board_parser import BoardParser
from core.clock import SimulatedClock
from core.game_controller import RealTimeGameController
from parsers.command_handler import CommandStreamProcessor

# הפונקציה הראשית שמטפלת בקלט מהמשתמש ומפעילה את המשחק
def main() -> None:
    try:
        input_lines = sys.stdin.read().splitlines()
        if not input_lines:
            return
            
        board = BoardParser.parse_from_string(input_lines)
        
        clock = SimulatedClock()
        game_controller = RealTimeGameController(board=board, clock=clock)
        command_processor = CommandStreamProcessor(controller=game_controller)

        is_commands_section = False
        for line in input_lines:
            clean_line = line.strip()
            if "Commands:" in clean_line:
                is_commands_section = True
                continue
            
            if is_commands_section:
                command_processor.process_line(clean_line)
                
    except ValueError as e:
        # הדפסה במקרה חירום של קריסה לא צפויה
        sys.stdout.write(str(e) + "\n")

if __name__ == "__main__":
    main()