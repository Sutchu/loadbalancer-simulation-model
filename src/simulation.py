from typing import List

from .traffic_manager import TrafficManager
from .metrics_logger import MetricsLogger
from .worker import Worker
from .load_balancer import LoadBalancer


class Simulation:
    def __init__(self, traffic_json_arr: List[dict], load_balancer_class: type, initial_worker_count=20):
        self.metrics_logger = MetricsLogger()
        self.traffic_manager = TrafficManager(traffic_json_arr)
        self.load_balancer: LoadBalancer = load_balancer_class(initial_worker_count)

        # Initialize the worker pool
        self.worker_indexes = [[] for _ in range(9)]
        self.worker_indexes[0] = [Worker() for _ in range(initial_worker_count)]

        self._current_simulation_time = 0


    def finish_processing_frames(self, current_worker_group: List[Worker]):
        for worker in current_worker_group:
            if worker.is_busy:
                self.metrics_logger.increment_worker_usage_time(8)

            worker.finish_processing_frame(self._current_simulation_time)

    def assign_new_frames_to_available_workers(self, current_worker_group: List[Worker]) -> int:
        idle_worker_index = len(current_worker_group)
        for index, worker in enumerate(current_worker_group):
            # If there are no more videos to process, break out of the loop
            if not self.traffic_manager.assign_video_to_worker(worker):
                idle_worker_index = index
                break

        # Divide current worker group into idle and busy workers
        idle_workers = current_worker_group[idle_worker_index:]
        busy_workers = current_worker_group[:idle_worker_index]

        worker_group_index = self._current_simulation_time % 9
        # Set busy workers to previous worker group
        self.worker_indexes[worker_group_index - 1] = busy_workers
        self.worker_indexes[worker_group_index] = []
        # Add idle workers to next worker group
        self.worker_indexes[(worker_group_index + 1) % 9].extend(idle_workers)

        return len(idle_workers)

    def simulate_traffic(self):
        idle_worker_count = 0

        while not self.traffic_manager.is_video_queue_finished or not self.traffic_manager.is_traffic_finished:
            self.traffic_manager.add_videos_to_queue(self._current_simulation_time)

            current_worker_group = self.worker_indexes[self._current_simulation_time % 9]
            self.finish_processing_frames(current_worker_group)
            self.metrics_logger.increment_worker_usage_time(idle_worker_count)

            if self._current_simulation_time % 60 == 0:
                self.load_balancer.add_workers(current_worker_group)

                processing_queue_frame_count = self.traffic_manager.processing_queue_frame_count
                self.metrics_logger.update_queue_length(processing_queue_frame_count)
                self.metrics_logger.update_worker_counts(self.load_balancer.worker_count)

                self.load_balancer.balance_worker_load(len(current_worker_group), processing_queue_frame_count)

            self.load_balancer.remove_workers(current_worker_group)
            idle_worker_count = self.assign_new_frames_to_available_workers(current_worker_group)

            self._current_simulation_time += 1

        self.metrics_logger.update_average_vrt(self.traffic_manager.average_video_ready_time)
