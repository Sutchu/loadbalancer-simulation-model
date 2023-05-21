class _SimulationClock:
    def __init__(self):
        self._current_time_in_seconds = 0

    def reset(self):
        self._current_time_in_seconds = 0

    def advance_by_one_second(self):
        self._current_time_in_seconds += 1

    @property
    def current_time_in_secs(self):
        return self._current_time_in_seconds

    @property
    def is_minute_boundary(self):
        return self._current_time_in_seconds % 60 == 0


SimulationClock: _SimulationClock = _SimulationClock()