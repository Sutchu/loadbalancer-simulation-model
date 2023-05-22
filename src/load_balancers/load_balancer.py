from src.worker import Worker
from src.metrics_logger import MetricsLogger

from src.traffic_manager import TrafficManager
class LoadBalancer:

    def __init__(self, initial_worker_count: int,
                 traffic_manager: TrafficManager):
        self.W_arr = [0.0] * 5
        self._worker_count: int = initial_worker_count
        self._traffic_manager: TrafficManager = traffic_manager

    def balance_worker_load(self, available_worker_count: int, processing_queue_frame_count: int, current_timestamp: int):
        """
        This is the main function that balances the worker load.
        W is the average number of frames in the processing queue(A) per worker(B).
        W = A / B.
        """
        A = processing_queue_frame_count

        # Number of workers. This does not include idle workers.
        # I am not sure if I am calculating this number correctly. So if B has to include idle workers,
        # then comment line bellow and uncomment the line after.
        B = max(1, (self._worker_count - available_worker_count))
        # B = self.worker_count

        W = A / B
        self.W_arr.append(W)

        # average of last 5 minutes
        average_w = sum(self.W_arr[-5:]) / 5
        if average_w > 12:
            self.add_workers(5, current_timestamp)
        elif average_w < 5:
            self.remove_workers(min(4, max(self._worker_count - 20, 0)))

    def add_workers(self, count: int, current_timestamp: int):
        self._traffic_manager.create_add_workers_event(current_timestamp, count)
        self._worker_count += 1

    def remove_workers(self, count: int, current_timestamp: int):
        def decrease_worker_count():
            self._worker_count -= 1

        self._traffic_manager.create_remove_workers_event(current_timestamp, count, decrease_worker_count)
