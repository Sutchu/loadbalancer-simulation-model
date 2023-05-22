from typing import Callable
from ..load_balancers.load_balancer import LoadBalancer
from ..traffic_manager import TrafficManager

from .base_simulation_event import BaseSimulationEvent
from ..simulation_event_enum import SimulationEventEnum


class LoadBalancerCheckEvent(BaseSimulationEvent):
    def __init__(self, timestamp: int, load_balancer: LoadBalancer, traffic_manager: TrafficManager):
        super().__init__(event_type=SimulationEventEnum.LOAD_BALANCER_CHECK,
                         timestamp=timestamp)

        self._load_balancer = load_balancer
        self._traffic_manager = traffic_manager

    def execute(self):
        self._load_balancer.balance_worker_load(
            available_worker_count=len(self._traffic_manager.available_workers),
            processing_queue_frame_count=self._traffic_manager.processing_queue_frame_count)
