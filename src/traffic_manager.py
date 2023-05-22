from collections import deque
from typing import List, Callable

from .video import Video
from .worker import Worker
from .simulation_events.video_added_from_traffic_event import VideoAddedFromTrafficEvent
from .simulation_events.worker_finished_processing_event import WorkerFinishedProcessingEvent
from .simulation_events.add_workers_event import AddWorkersEvent
from .simulation_events.remove_workers_event import RemoveWorkersEvent

class TrafficManager:
    def __init__(self, traffic_json_arr: List[dict], add_event_to_queue_callback: Callable, initial_worker_count: int = 20):
        self.video_ready_time_arr: List[float] = []

        initial_video_timestamp = traffic_json_arr[-1]['properties']['time']

        on_fully_processed = lambda video: self.video_ready_time_arr.append(video.video_ready_time)
        traffic = [Video(data,
                      initial_video_timestamp,
                      on_fully_processed)
                for data in traffic_json_arr]
        self.video_queue: deque[Video] = deque()

        self._add_event_to_queue_callback = add_event_to_queue_callback
        self._create_events_from_traffic(traffic)

        self.available_workers: List[Worker] = [Worker(self._add_worker_to_available_workers, 0) for _ in range(initial_worker_count)]

    def _add_worker_to_available_workers(self, worker: Worker):
        self.available_workers.append(worker)

    def _create_events_from_traffic(self, traffic):
        for video in traffic:
            event = VideoAddedFromTrafficEvent(timestamp=video.timestamp,
                                               video=video,
                                               video_queue=self.video_queue,
                                               assign_video_to_available_workers_callback=self._assign_frame_to_available_workers)

            self._add_event_to_queue_callback(event)

    def _assign_frame_to_available_workers(self, current_timestamp: int):
        while self.video_queue and self.available_workers:
            video: Video = self.video_queue[0]
            if video.has_unprocessed_frames:
                worker = self.available_workers.pop()
                worker.assign_video(video)

                event = WorkerFinishedProcessingEvent(timestamp=current_timestamp + 8,
                                                      worker=worker,
                                                      assign_video_to_available_workers_callback=self._assign_frame_to_available_workers)
                self._add_event_to_queue_callback(event)
            else:
                self.video_queue.popleft()

    def create_add_workers_event(self, current_timestamp: int, worker_count: int):
        pass


    def create_remove_workers_event(self, current_timestamp: int, worker_count: int, decrease_worker_count_callback: Callable):
        pass

    @property
    def processing_queue_frame_count(self) -> int:
        return sum(
            video.remaining_frame_count for video in self.video_queue)

    @property
    def average_video_ready_time(self) -> float:
        return sum(self.video_ready_time_arr) / len(self.video_ready_time_arr)
