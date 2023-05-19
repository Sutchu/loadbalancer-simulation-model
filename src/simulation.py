from src.video import Video
from src.worker import Worker

from collections import deque
from typing import List

from .errors import TrafficFinishedError


class Simulation:
    def __init__(self, traffic: List[Video], load_balancer_class: type, initial_worker_count=20):
        self.traffic = traffic

        # Initialize the queue of videos to be processed
        self.video_queue = deque()

        # Initialize the worker pool
        self.worker_indexes = [[] for _ in range(9)]
        self.worker_indexes[0] = [Worker(self.video_queue) for _ in range(initial_worker_count)]

        # Initialize lists to hold data for graphs
        self.vrt_arrray = []

        self.current_simulation_time = 0

        self.load_balancer = load_balancer_class(self.video_queue, initial_worker_count)
        self.total_worker_usage_time = 0 # WMU (worker machine usage)
        self.average_vrt = 0 # average VRT (video ready time)

    def update_video_queue_from_traffic(self):
        try:
            while self.current_simulation_time >= self.traffic[-1].timestamp:
                video: Video = self.traffic.pop()
                self.video_queue.append(video)
        except IndexError:
            raise TrafficFinishedError()

    def finish_processing_frames(self, current_worker_group):
        for worker in current_worker_group:
            if worker._video:
                self.total_worker_usage_time += 8

            worker.finish_processing_frame(self.current_simulation_time, self.vrt_arrray)

    def assign_new_frames_to_available_workers(self, current_worker_group):
        idle_worker_index = len(current_worker_group)
        for index, worker in enumerate(current_worker_group):
            # If there are no more videos to process, break out of the loop
            if not worker.process_new_frame():
                idle_worker_index = index
                break

        # Divide current worker group into idle and busy workers
        idle_workers = current_worker_group[idle_worker_index:]
        busy_workers = current_worker_group[:idle_worker_index]

        worker_group_index = self.current_simulation_time % 9
        # Set busy workers to previous worker group
        self.worker_indexes[worker_group_index - 1] = busy_workers
        self.worker_indexes[worker_group_index] = []
        # Add idle workers to next worker group
        self.worker_indexes[(worker_group_index + 1) % 9].extend(idle_workers)

        return len(idle_workers)

    def simulate_traffic(self):
        is_traffic_empty = False
        idle_worker_count = 0

        while self.video_queue or not is_traffic_empty:
            try:
                self.update_video_queue_from_traffic()
            except TrafficFinishedError:
                is_traffic_empty = True

            current_worker_group = self.worker_indexes[self.current_simulation_time % 9]
            self.finish_processing_frames(current_worker_group)
            self.total_worker_usage_time += idle_worker_count

            if self.current_simulation_time % 60 == 0:
                self.load_balancer.add_workers(current_worker_group)
                self.load_balancer.update_graph_arrays()
                self.load_balancer.balance_worker_load(len(current_worker_group))

            self.load_balancer.remove_workers(current_worker_group)
            idle_worker_count = self.assign_new_frames_to_available_workers(current_worker_group)

            self.current_simulation_time += 1

        self.average_vrt = sum(self.vrt_arrray) // len(self.vrt_arrray)

        return self.load_balancer.queue_sizes, self.load_balancer.worker_counts