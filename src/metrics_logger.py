from typing import List


class _MetricsLogger:
    def __init__(self):
        self.queue_lengths: List[int] = []
        self.worker_counts: List[int] = []
        self.cumulative_worker_usage_time = 0 # WMU (worker machine usage)
        self.average_video_ready_time = 0 # Average VRT (video ready time)

    def update_queue_length(self, queue_length: int):
        self.queue_lengths.append(queue_length)

    def update_worker_counts(self, worker_count: int):
        self.worker_counts.append(worker_count)

    def update_average_vrt(self, avg_vrt: float):
        self.average_video_ready_time = avg_vrt

    def increment_worker_usage_time(self, increment_by: int):
        self.cumulative_worker_usage_time += increment_by


# Singleton
MetricsLogger = _MetricsLogger()
