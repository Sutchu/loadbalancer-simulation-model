from typing import Callable

from src.simulation_event_enum import SimulationEventEnum
from .base_simulation_event import BaseSimulationEvent
from ..worker import Worker


class WorkerFinishedProcessingEvent(BaseSimulationEvent):

    def __init__(self, timestamp: int,
                 worker: Worker,
                 assign_video_to_available_workers_callback: Callable):
        super().__init__(event_type=SimulationEventEnum.WORKER_FINISHED_PROCESSING,
                        timestamp=timestamp)

        self.worker: Worker = worker
        self.assign_video_to_available_workers_callback = assign_video_to_available_workers_callback

    def execute(self):
        self.worker.finish_processing_frame(self.timestamp)

        self.assign_video_to_available_workers_callback(self.timestamp)

