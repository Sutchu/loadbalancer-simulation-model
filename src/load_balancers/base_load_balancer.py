from src.worker import Worker
from src.metrics_logger import MetricsLogger

class BaseLoadBalancer:
    """
    This is the abstract base class for all load balancers.
    """
    def __init__(self, initial_worker_count):
        self.worker_count: int = initial_worker_count

        self.number_of_workers_to_remove = 0
        self.number_of_workers_to_add = 0

    def balance_worker_load(self, worker_group_size: int, processing_queue_frame_count: int):
        return

    def add_workers(self, current_worker_group):
        """
        This function adds new workers to the current worker group.
        """
        for _ in range(self.number_of_workers_to_add):
            current_worker_group.append(Worker())
            self.worker_count += 1

        MetricsLogger.increment_worker_usage_time(self.number_of_workers_to_add * 60)
        self.number_of_workers_to_add = 0

    def remove_workers(self, current_worker_group):
        """
        This function removes workers from the current worker group.
        Given worker group represents workers that are not busy.
        If number of workers to remove is greater than the number of workers in the group,
        then the number_of_workers_to_remove is reduced to remove workers on next iteration.
        """
        for i in range(self.number_of_workers_to_remove):
            try:
                current_worker_group.pop()
                self.worker_count -= 1
            except IndexError:
                self.number_of_workers_to_remove = self.number_of_workers_to_remove - i
                break

            self.number_of_workers_to_remove = 0
