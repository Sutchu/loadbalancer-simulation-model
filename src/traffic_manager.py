from collections import deque
from typing import List

from .video import Video


class TrafficManager:
    def __init__(self, traffic_json_arr: List[dict]):
        self.average_video_processing_time_arr = []

        def on_fully_processed(video: Video):
            self.average_video_processing_time_arr.append(video.video_ready_time)

        initial_video_timestamp = traffic_json_arr[-1]['properties']['time']
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
    def average_video_processing_time(self) -> float:
        return sum(self.average_video_processing_time_arr) / len(self.average_video_processing_time_arr)

    def assign_video_to_worker(self, worker) -> bool:
        while self.video_queue:
            video: Video = self.video_queue[0]  # Peek at the first video in the queue
            if video.has_unprocessed_frames:
                worker.assign_video(video)
                return True
            else:
                self.video_queue.popleft()

        return False
