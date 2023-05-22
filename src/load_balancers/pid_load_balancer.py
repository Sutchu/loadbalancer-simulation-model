from .load_balancer import LoadBalancer

class PIDLoadBalancer(LoadBalancer):

    def __init__(self, initial_worker_count: int):
        super().__init__(initial_worker_count)
        self.Kp = 1
        self.Kd = 0.1

        self.prev_cost = 0

    def balance_worker_load(self, worker_group_size: int, processing_queue_frame_count: int):
        A = processing_queue_frame_count
        B = self._worker_count
        cost = (A/(B*4)-1)*10 # - max(0, B - A)

        P = self.Kp * cost
        D = self.Kd * (cost - self.prev_cost)
        self.prev_cost = cost

        worker_count = int(P + D)
        if worker_count < 0:
            self.number_of_workers_to_remove = abs(worker_count)
            if self._worker_count - self.number_of_workers_to_remove < 50:
                self.number_of_workers_to_remove = self._worker_count - 50
        else:
            self.number_of_workers_to_add = worker_count
