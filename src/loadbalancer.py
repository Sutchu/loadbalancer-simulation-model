from .worker import Worker
from typing import List

class LoadBalancer:

    def __init__(self, video_queue, initial_worker_count):
        self.W = [0.0] * 5
        self.queue_size: int = 0
        self.worker_count: int = initial_worker_count

        self.worker_counts: List[int] = []
        self.queue_sizes: List[int] = []

        self.video_queue = video_queue

        self.number_of_workers_to_remove = 0
        self.number_of_workers_to_add = 0

    def update_graph_arrays(self):
        self.queue_size = sum(
            video._unprocessed_frame_count + video._processing_frame_count for video in self.video_queue)
        self.queue_sizes.append(self.queue_size)
        self.worker_counts.append(self.worker_count)

    def balance_worker_load(self, current_worker_group_size):
        self.W.append(self.queue_size / max(1, (self.worker_count - current_worker_group_size)))

        # average of last 5 minutes
        average_w = sum(self.W[-5:]) / 5
        if average_w > 12:
            self.number_of_workers_to_add = 5
        elif average_w < 5:
            self.number_of_workers_to_remove = min(4, max(self.worker_count - 20, 0))

    def add_workers(self, current_worker_group):
        """
        This function adds new workers to the current worker group.
        """
        for _ in range(self.number_of_workers_to_add):
            current_worker_group.append(Worker())
            self.worker_count += 1

        self.number_of_workers_to_add = 0

    def remove_workers(self, current_worker_group):
        for i in range(self.number_of_workers_to_remove):
            try:
                current_worker_group.pop()
                self.worker_count -= 1
            except IndexError:
                self.number_of_workers_to_remove = self.number_of_workers_to_remove - i
                break

            self.number_of_workers_to_remove = 0
