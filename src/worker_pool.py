from .worker import Worker
from .traffic_manager import TrafficManager
from .metrics_logger import MetricsLogger

from typing import List, Callable


class WorkerPool:
    def __init__(self, current_simulation_time_callback: Callable, initial_worker_count=20):
        self.worker_indexes: List[List[Worker]] = [[] for _ in range(9)]
        self.worker_indexes[0] = [Worker() for _ in range(initial_worker_count)]

        self._current_worker_group: List[Worker] = []

        self._get_current_simulation_time = current_simulation_time_callback


    def assign_new_frames_to_available_workers(self, traffic_manager: TrafficManager) -> int:
        idle_worker_index = len(self._current_worker_group)
        for index, worker in enumerate(self._current_worker_group):
            # If there are no more videos to process, break out of the loop
            if not traffic_manager.assign_video_to_worker(worker):
                idle_worker_index = index
                break

        # Divide current worker group into idle and busy workers
        idle_workers = self._current_worker_group[idle_worker_index:]
        busy_workers = self._current_worker_group[:idle_worker_index]

        worker_group_index = self._get_current_simulation_time() % 9
        # Set busy workers to previous worker group
        self.worker_indexes[worker_group_index - 1] = busy_workers
        self.worker_indexes[worker_group_index] = []
        # Add idle workers to next worker group
        self.worker_indexes[(worker_group_index + 1) % 9].extend(idle_workers)

        return len(idle_workers)

    def finish_processing_frames(self):
        for worker in self._current_worker_group:
            if worker.is_busy:
                MetricsLogger.increment_worker_usage_time(8)

            worker.finish_processing_frame(self._get_current_simulation_time())

    def get_and_update_current_worker_group(self):
        self._current_worker_group = self.worker_indexes[self._get_current_simulation_time() % 9]
        return self._current_worker_group
