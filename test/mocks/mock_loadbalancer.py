from src.load_balancers.load_balancer import LoadBalancer

class MockLoadBalancer(LoadBalancer):
    """
    Mock LoadBalancer that does not add or remove workers.
    """

    def add_workers(self, current_worker_group):
        return

    def remove_workers(self, current_worker_group):
        return