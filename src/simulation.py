from typing import List

from .traffic_manager import TrafficManager
from .worker import Worker


class Simulation:
    def __init__(self, traffic_json_arr: List[dict], load_balancer_class: type, initial_worker_count=20):
        self.traffic_manager = TrafficManager(traffic_json_arr)

        # Initialize the worker pool
        self.worker_indexes = [[] for _ in range(9)]
        self.worker_indexes[0] = [Worker() for _ in range(initial_worker_count)]

        self.current_simulation_time = 0

        self.load_balancer = load_balancer_class(self.traffic_manager.video_queue, initial_worker_count)
        self.total_worker_usage_time = 0  # WMU (worker machine usage)
        self.average_vrt = 0  # average VRT (video ready time)

    def finish_processing_frames(self, current_worker_group: List[Worker]):
        for worker in current_worker_group:
            if worker._video:
                self.total_worker_usage_time += 8

            worker.finish_processing_frame(self.current_simulation_time)

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

        worker_group_index = self.current_simulation_time % 9
        # Set busy workers to previous worker group
        self.worker_indexes[worker_group_index - 1] = busy_workers
        self.worker_indexes[worker_group_index] = []
        # Add idle workers to next worker group
        self.worker_indexes[(worker_group_index + 1) % 9].extend(idle_workers)

        return len(idle_workers)

    def simulate_traffic(self):
        idle_worker_count = 0

        while self.traffic_manager.video_queue or not self.traffic_manager.is_traffic_finished:
            self.traffic_manager.add_videos_to_queue(self.current_simulation_time)

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

        self.average_vrt = self.traffic_manager.average_video_processing_time

        return self.load_balancer.queue_sizes, self.load_balancer.worker_counts
