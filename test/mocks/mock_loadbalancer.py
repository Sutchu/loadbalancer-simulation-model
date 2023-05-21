from src.load_balancers.load_balancer import LoadBalancer

class MockLoadBalancer(LoadBalancer):
    """
    Mock LoadBalancer that does not add or remove workers.
    """

    def balance_worker_load(self, worker_count, processing_queue_frame_count):
        return
