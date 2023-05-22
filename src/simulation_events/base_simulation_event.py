from src.simulation_event_enum import SimulationEventEnum


class BaseSimulationEvent:
    def __init__(self, timestamp: int, event_type: SimulationEventEnum):
        self.timestamp = timestamp
        self._type: SimulationEventEnum = event_type

    def execute(self):
        pass

    def __lt__(self, other):
        if self.timestamp < other.timestamp:
            return True
        elif self.timestamp > other.timestamp:
            return False
        else: # if self.timestamp == other.timestamp:
            return self._type.value <= other._type.value

