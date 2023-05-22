from .base_simulation_event import BaseSimulationEvent
from ..simulation_event_enum import SimulationEventEnum


class RemoveWorkersEvent(BaseSimulationEvent):

    def __init__(self, timestamp: int, worker_count: int):
        super().__init__(event_type=SimulationEventEnum.ADD_WORKERS,
                         timestamp=timestamp)

        self._worker_count = worker_count