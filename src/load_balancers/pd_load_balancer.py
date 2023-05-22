from .base_load_balancer import BaseLoadBalancer

class PDLoadBalancer(BaseLoadBalancer):

    def __init__(self, initial_worker_count: int):
        super().__init__(initial_worker_count)
        self.Kp = 10
        self.Kd = 2

        self.prev_cost = 0

    def balance_worker_load(self, worker_group_size: int, processing_queue_frame_count: int):
        """
        This load balancer uses a PD controller to balance the worker load.

        Results with ExampleTraffic.json is better than other load balancers:
            Average VRT: 43.62906362878577
            WMU: 5218871
        """
        A = processing_queue_frame_count
        B = self.worker_count
        cost = A/(B*4) - 1

        P = self.Kp * cost
        D = self.Kd * (cost - self.prev_cost)
        self.prev_cost = cost

        worker_count = int(P + D)
        if worker_count < 0:
            self.number_of_workers_to_remove = abs(worker_count)
            # Don't remove workers if there will be less than 50 workers.
            if self.worker_count - self.number_of_workers_to_remove < 50:
                self.number_of_workers_to_remove = self.worker_count - 50
        else:
            self.number_of_workers_to_add = worker_count
