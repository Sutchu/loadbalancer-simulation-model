from collections import deque
from typing import List

from .video import Video
from .worker import Worker
from .metrics_logger import MetricsLogger
from .time_keeper import SimulationClock


class TrafficManager:
    def __init__(self, traffic_json_arr: List[dict]):
        self.video_ready_time_arr: List[float] = []

        initial_video_timestamp = traffic_json_arr[-1]['properties']['time']
        on_fully_processed = lambda video: self.video_ready_time_arr.append(video.video_ready_time)

        self.traffic = [Video(data,
                              initial_video_timestamp,
                              on_fully_processed)
                        for data in traffic_json_arr]
        self.video_queue: deque[Video] = deque()

    def add_videos_to_queue(self):
        while self.traffic and SimulationClock.current_time_in_secs >= self.traffic[-1].timestamp:
            video = self.traffic.pop()
            self.video_queue.append(video)
        if SimulationClock.is_minute_boundary:
            MetricsLogger.update_queue_length(self.processing_queue_frame_count)

    def assign_video_to_worker(self, worker: Worker) -> bool:
        """
        Assigns the first unprocessed video to the worker
        If first video is fully processed, removes it from the queue and tries again

        :param worker: Worker instance
        :return: bool, True if video was assigned, False otherwise
        """
        while self.video_queue:
            video: Video = self.video_queue[0]  # Peek at the first video in the queue
            if video.has_unprocessed_frames:
                worker.assign_video(video)
                return True
            else:
                self.video_queue.popleft()

        return False

    @property
    def is_traffic_finished(self) -> bool:
        return not self.traffic

    @property
    def is_video_queue_finished(self) -> bool:
        return not self.video_queue

    @property
    def processing_queue_frame_count(self) -> int:
        return sum(
            video.remaining_frame_count for video in self.video_queue)

    @property
    def average_video_ready_time(self) -> float:
        return sum(self.video_ready_time_arr) / len(self.video_ready_time_arr)
