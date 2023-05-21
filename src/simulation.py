from typing import List

from .traffic_manager import TrafficManager
from .metrics_logger import MetricsLogger
from .worker_pool import WorkerPool
from src.load_balancers.load_balancer import LoadBalancer


class Simulation:
    def __init__(self, traffic_json_arr: List[dict], load_balancer_class: type, initial_worker_count=20):
        self._current_simulation_time = 0
        def get_current_simulation_time():
            return self._current_simulation_time

        self.traffic_manager = TrafficManager(traffic_json_arr)
        self.load_balancer: LoadBalancer = load_balancer_class(initial_worker_count)
        self.worker_pool = WorkerPool(get_current_simulation_time, initial_worker_count)

    def simulate_traffic(self):
        idle_worker_count = 0

        while not self.traffic_manager.is_video_queue_finished or not self.traffic_manager.is_traffic_finished:
            self.traffic_manager.add_videos_to_queue(self._current_simulation_time)

            current_worker_group = self.worker_pool.get_and_update_current_worker_group()
            self.worker_pool.finish_processing_frames()
            MetricsLogger.increment_worker_usage_time(idle_worker_count)

            if self._current_simulation_time % 60 == 0:
                MetricsLogger.increment_worker_usage_time(self.load_balancer.number_of_workers_to_add * 60)
                self.load_balancer.add_workers(current_worker_group)

                processing_queue_frame_count = self.traffic_manager.processing_queue_frame_count
                MetricsLogger.update_queue_length(processing_queue_frame_count)
                MetricsLogger.update_worker_counts(self.load_balancer.worker_count)

                self.load_balancer.balance_worker_load(len(current_worker_group), processing_queue_frame_count)

            self.load_balancer.remove_workers(current_worker_group)

            idle_worker_count = self.worker_pool.assign_new_frames_to_available_workers(traffic_manager=self.traffic_manager)

            self._current_simulation_time += 1

        MetricsLogger.update_average_vrt(self.traffic_manager.average_video_ready_time)
