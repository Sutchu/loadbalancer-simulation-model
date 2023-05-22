from .base_simulation_event import BaseSimulationEvent
from ..simulation_event_enum import SimulationEventEnum


class AddWorkersEvent(BaseSimulationEvent):

    def __init__(self, timestamp: int, number_of_workers_to_add: int):
        super().__init__(event_type=SimulationEventEnum.ADD_WORKERS,
                         timestamp=timestamp)

        self.number_of_workers_to_add = number_of_workers_to_add
