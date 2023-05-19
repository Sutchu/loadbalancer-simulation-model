from unittest import TestCase
from test.mocks.mock_loadbalancer import MockLoadBalancer
from src.simulation import Simulation
from src.video import Video

class TestSimulation(TestCase):

    def create_video_data(self, time, duration):
        return {'properties': {'time': time, 'Duration': duration}}

    def setUp(self) -> None:
        # Video with 16 frame.
        data = self.create_video_data(0, 16/15)

        self.traffic = [Video(data, 0)]

    def test_1_video_1_worker(self):
        """
        Test that a single video is processed by a single worker with 16 frames.
        average VRT should be 16 frames * 8 seconds per frame
        WMU should be 16 frames * 8 seconds per frame + 1 second.
        The extra second is because first frame starts being processed at first second.
        """
        simulation = Simulation(traffic=self.traffic,
                                load_balancer_class=MockLoadBalancer,
                                initial_worker_count=1)

        queue_sizes, worker_counts = simulation.simulate_traffic()
        self.assertEqual(queue_sizes, [0, 9, 2])
        self.assertEqual(worker_counts, [1, 1, 1])
        self.assertEqual(simulation.average_vrt, 16 * 8) # 16 frames * 8 seconds per frame
        self.assertEqual(simulation.total_worker_usage_time, 16 * 8 + 1) # 16 frames * 8 seconds per frame

    def test_1_video_2_workers(self):
        simulation = Simulation(traffic=self.traffic,
                                load_balancer_class=MockLoadBalancer,
                                initial_worker_count=2)

        queue_sizes, worker_counts = simulation.simulate_traffic()
        self.assertEqual(queue_sizes, [0, 2])
        self.assertEqual(worker_counts, [2, 2])
        self.assertEqual(simulation.average_vrt, 16 * 8 / 2)  # 16 frames * 8 seconds per frame
        self.assertEqual(simulation.total_worker_usage_time, 16 * 8 + 2)  # 16 frames * 8 seconds per frame

    def test_2_video_1_workers(self):
        video_2 = Video(self.create_video_data(180, 16/15), 0)
        self.traffic.insert(0, video_2)

        simulation = Simulation(traffic=self.traffic,
                                load_balancer_class=MockLoadBalancer,
                                initial_worker_count=1)

        queue_sizes, worker_counts = simulation.simulate_traffic()
        self.assertEqual(queue_sizes, [0, 9, 2, 0, 9, 2])
        self.assertEqual(worker_counts, [1, 1, 1, 1, 1, 1])
        self.assertEqual(simulation.average_vrt, 16 * 8)  # 16 frames * 8 seconds per frame

        expected_wmu = 16 * 8 * 2 + (181 - 129) + 1
        self.assertEqual(simulation.total_worker_usage_time, expected_wmu)

    def test_2_video_2_workers(self):
        video_2 = Video(self.create_video_data(180, 16/15), 0)
        self.traffic.insert(0, video_2)

        simulation = Simulation(traffic=self.traffic,
                                load_balancer_class=MockLoadBalancer,
                                initial_worker_count=2)

        queue_sizes, worker_counts = simulation.simulate_traffic()
        self.assertEqual(queue_sizes, [0, 2, 0, 0, 2])
        self.assertEqual(worker_counts, [2, 2, 2, 2, 2])
        self.assertEqual(simulation.average_vrt, 16 * 8 / 2)

        expected_wmu = 16 * 8 * 2 + ((181 - 65) + 1) * 2
        self.assertEqual(simulation.total_worker_usage_time, expected_wmu)
