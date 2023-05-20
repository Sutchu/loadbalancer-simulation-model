from .load_balancer import LoadBalancer

class PIDLoadBalancer(LoadBalancer):

    def __init__(self, initial_worker_count: int):
        super().__init__(initial_worker_count)
        self.p = 0.2
        self.i = 0
        self.d = 0

    def balance_worker_load(self, worker_group_size: int, processing_queue_frame_count: int):
        cost = processing_queue_frame_count / self.worker_count

        self.i += cost
        self.d = cost - self.p
        self.p = cost

        worker_count = int(self.p + self.i + self.d)
        if worker_count < 0:
            self.number_of_workers_to_remove = min(worker_count, max(self.worker_count - 20, 0))
        else:
            self.number_of_workers_to_add = worker_count
