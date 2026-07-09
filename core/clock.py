
from core.interfaces import IClock

class SimulatedClock(IClock):

    # ממשק פשוט של שעון שמדמה את הזמן במילישניות
    def __init__(self) -> None:
        self._current_time_ms: int = 0

    # מאפשר לדמות את הזמן על ידי קריאה לפונקציה זו עם מספר המילישניות שברצוננו להוסיף לשעון
    def advance(self, ms: int) -> None:
        if ms < 0:
            return
        self._current_time_ms += ms

    # מאפשר לקבל את הזמן הנוכחי במילישניות
    def get_current_time(self) -> int:
        return self._current_time_ms
