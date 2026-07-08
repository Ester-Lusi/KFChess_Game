
from core.interfaces import IClock

class SimulatedClock(IClock):
    # ממשק פשוט של שעון שמדמה את הזמן במילישניות
    def __init__(self) -> None:
        self._current_time_ms: int = 0

    def advance(self, ms: int) -> None:
        if ms < 0:
            return
        self._current_time_ms += ms

    def get_current_time(self) -> int:
        return self._current_time_ms
