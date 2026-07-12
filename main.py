# main.py
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

        board_lines = []
        command_lines = []
        is_commands_section = False
        
        for line in input_lines:
            clean_line = line.strip()
            if not clean_line:
                continue
            if "Commands:" in clean_line:
                is_commands_section = True
                continue
            
            if is_commands_section:
                command_lines.append(clean_line)
            else:
                board_lines.append(clean_line)
        
        board = BoardParser.parse_from_string(board_lines)
        
        clock = SimulatedClock()
        game_controller = RealTimeGameController(board=board, clock=clock)
        command_processor = CommandStreamProcessor(controller=game_controller)

        # הרצת הפקודות שנאספו
        for cmd_line in command_lines:
            command_processor.process_line(cmd_line)
                
    except ValueError as e:
        sys.stdout.write(str(e) + "\n")

if __name__ == "__main__":
    main()