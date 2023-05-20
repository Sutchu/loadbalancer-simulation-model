from collections import deque
from typing import List

from .video import Video
from .worker import Worker


class TrafficManager:
    def __init__(self, traffic_json_arr: List[dict]):
        self.video_ready_time_arr = []

        initial_video_timestamp = traffic_json_arr[-1]['properties']['time']
        on_fully_processed = lambda video: self.video_ready_time_arr.append(video.video_ready_time)

        self.traffic = [Video(data,
                              initial_video_timestamp,
                              on_fully_processed)
                        for data in traffic_json_arr]
        self.video_queue = deque()

    def add_videos_to_queue(self, current_time: int):
        while self.traffic and current_time >= self.traffic[-1].timestamp:
            video = self.traffic.pop()
            self.video_queue.append(video)

    @property
    def is_traffic_finished(self) -> bool:
        return not self.traffic

    @property
    def is_video_queue_finished(self) -> bool:
        return not self.video_queue

    @property
    def processing_queue_frame_count(self) -> int:
        return sum(
            video._unprocessed_frame_count + video._processing_frame_count for video in self.video_queue)

    @property
    def average_video_ready_time(self) -> float:
        return sum(self.video_ready_time_arr) / len(self.video_ready_time_arr)

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