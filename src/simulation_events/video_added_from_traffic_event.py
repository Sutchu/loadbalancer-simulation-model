from collections import deque
from typing import Callable

from .base_simulation_event import BaseSimulationEvent
from ..simulation_event_enum import SimulationEventEnum
from ..video import Video


class VideoAddedFromTrafficEvent(BaseSimulationEvent):

    def __init__(self, timestamp: int, video: Video, video_queue: deque[Video], assign_video_to_available_workers_callback: Callable):
        super().__init__(event_type=SimulationEventEnum.VIDEO_ADDED_FROM_TRAFFIC,
                        timestamp=timestamp)

        self.video: Video = video
        self.video_queue: deque[Video] = video_queue
        self.assign_video_to_available_workers_callback = assign_video_to_available_workers_callback


    def execute(self):
        self.video_queue.append(self.video)

        self.assign_video_to_available_workers_callback(self.timestamp)
