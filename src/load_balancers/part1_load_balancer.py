from .base_load_balancer import BaseLoadBalancer

class Part1LoadBalancer(BaseLoadBalancer):

    def __init__(self, initial_worker_count):
        super().__init__(initial_worker_count)
        self.W_arr = [0.0] * 5


    def balance_worker_load(self, worker_group_size: int, processing_queue_frame_count: int):
        """
        This is the main function that balances the worker load.
        W is the average number of frames in the processing queue(A) per worker(B).
        W = A / B.

        Results with ExampleTraffic.json:
            Average VRT: 68.17338149485968
            WMU: 5663789
        """
        A = processing_queue_frame_count

        # Number of workers. This does not include idle workers.
        # I am not sure if I am calculating this number correctly. So if B has to include idle workers,
        # then comment line bellow and uncomment the line after.
        B = max(1, (self.worker_count - worker_group_size))
        # B = self.worker_count

        W = A / B
        self.W_arr.append(W)

        # average of last 5 minutes
        average_w = sum(self.W_arr[-5:]) / 5
        if average_w > 12:
            self.number_of_workers_to_add = 5
        elif average_w < 5:
            self.number_of_workers_to_remove = min(4, max(self.worker_count - 20, 0))
