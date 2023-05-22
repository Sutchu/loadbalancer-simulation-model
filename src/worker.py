from .video import Video
from typing import Callable


class Worker:
    def __init__(self, on_finished_processing: Callable, startup_timestamp: int):
        self._video: Video = None
        self._startup_timestamp: int = startup_timestamp

        self._on_finished_processing = on_finished_processing

    def finish_processing_frame(self, current_simulation_time):
        self._video.mark_frame_as_processed(current_simulation_time)
        self._video = None

        self._on_finished_processing(self)

    def assign_video(self, video: Video):
        video.mark_frame_as_processing()
        self._video = video

    def get_and_calculate_uptime(self, current_simulation_time: int) -> int:
        return current_simulation_time - self._startup_timestamp
