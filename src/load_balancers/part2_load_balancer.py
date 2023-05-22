from .base_load_balancer import BaseLoadBalancer

class Part2LoadBalancer(BaseLoadBalancer):

    def __init__(self, initial_worker_count):
        super().__init__(initial_worker_count)
        self.W_arr = [0.0] * 5

    def balance_worker_load(self, worker_group_size: int, processing_queue_frame_count: int):
        """
        Cost function of this load balancer is kept exactly the same with the Part1LoadBalancer.
        I changed lower and upper bounds of the number of workers to add and remove. I also changed
        average_w value. Now it is calculated with the last 3 minutes instead of 5 minutes.

        With these changes, I was able to get a better result than Part1LoadBalancer.
            Average VRT: 49.893581550430675
            WMU: 5717648
        """
        A = processing_queue_frame_count
        B = max(1, (self.worker_count - worker_group_size))

        W = A / B
        self.W_arr.append(W)

        # average of last 5 minutes
        average_w = sum(self.W_arr[-3:]) / 3
        if average_w > 4:
            self.number_of_workers_to_add = 5
        elif average_w < 3:
            self.number_of_workers_to_remove = min(4, max(self.worker_count - 20, 0))