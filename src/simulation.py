from typing import List

from .traffic_manager import TrafficManager
from .metrics_logger import MetricsLogger
from .worker_pool import WorkerPool
from src.load_balancers.load_balancer import LoadBalancer
from .time_keeper import SimulationClock


class Simulation:
    def __init__(self, traffic_json_arr: List[dict], load_balancer_class: type, initial_worker_count=20):

        self.traffic_manager = TrafficManager(traffic_json_arr)
        self.load_balancer: LoadBalancer = load_balancer_class(initial_worker_count)
        self.worker_pool = WorkerPool(initial_worker_count)

    def simulate_traffic(self):

        while not self.traffic_manager.is_video_queue_finished or not self.traffic_manager.is_traffic_finished:
            self.traffic_manager.add_videos_to_queue()

            current_worker_group = self.worker_pool.get_and_update_current_worker_group()
            self.worker_pool.finish_processing_frames()

            if SimulationClock.is_minute_boundary:
                self.load_balancer.add_workers(current_worker_group)
                processing_queue_frame_count = self.traffic_manager.processing_queue_frame_count
                MetricsLogger.update_worker_counts(self.load_balancer.worker_count)

                self.load_balancer.balance_worker_load(len(current_worker_group), processing_queue_frame_count)

            self.load_balancer.remove_workers(current_worker_group)

            self.worker_pool.assign_new_frames_to_available_workers(traffic_manager=self.traffic_manager)

            SimulationClock.advance_by_one_second()
        MetricsLogger.update_average_vrt(self.traffic_manager.average_video_ready_time)
