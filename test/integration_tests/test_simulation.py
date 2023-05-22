from unittest import TestCase
from test.mocks.mock_loadbalancer import MockLoadBalancer
from src.simulation import Simulation
from src.metrics_logger import MetricsLogger


def create_video_data(time, duration):
    return {'properties': {'time': time, 'Duration': duration}}


class TestSimulation(TestCase):

    def setUp(self) -> None:
        # Video with 16 frame.
        self.traffic = [create_video_data(0, 16 / 15)]
        MetricsLogger.reset()

    def test_1_video_1_worker(self):
        """
        Test that a single video is processed by a single worker with 16 frames.
        average VRT should be 16 frames * 8 seconds per frame
        WMU should be 16 frames * 8 seconds per frame + 1 second.
        The extra second is because first frame starts being processed at first second.
        """
        simulation = Simulation(traffic_json_arr=self.traffic,
                                load_balancer_class=MockLoadBalancer,
                                initial_worker_count=1)

        simulation.simulate_traffic()

        # self.assertEqual(MetricsLogger.queue_lengths, [16, 9, 2])
        # self.assertEqual(MetricsLogger.worker_counts, [1, 1, 1])
        self.assertEqual(MetricsLogger.average_video_ready_time, 16 * 8)  # 16 frames * 8 seconds per frame
        # self.assertEqual(MetricsLogger.cumulative_worker_usage_time, 16 * 8 + 1)  # 16 frames * 8 seconds per frame

    def test_1_video_2_workers(self):
        simulation = Simulation(traffic_json_arr=self.traffic,
                                load_balancer_class=MockLoadBalancer,
                                initial_worker_count=2)

        simulation.simulate_traffic()

        self.assertEqual(MetricsLogger.queue_lengths, [16, 2])
        self.assertEqual(MetricsLogger.worker_counts, [2, 2])
        self.assertEqual(MetricsLogger.average_video_ready_time, 16 * 8 / 2)  # 16 frames * 8 seconds per frame
        self.assertEqual(MetricsLogger.cumulative_worker_usage_time, 16 * 8 + 2)  # 16 frames * 8 seconds per frame

    def test_2_video_1_workers(self):
        video_2 = create_video_data(180, 16 / 15)
        self.traffic.insert(0, video_2)

        simulation = Simulation(traffic_json_arr=self.traffic,
                                load_balancer_class=MockLoadBalancer,
                                initial_worker_count=1)

        simulation.simulate_traffic()

        self.assertEqual(MetricsLogger.queue_lengths, [16, 9, 2, 16, 9, 2])
        self.assertEqual(MetricsLogger.worker_counts, [1, 1, 1, 1, 1, 1])
        self.assertEqual(MetricsLogger.average_video_ready_time, 16 * 8)  # 16 frames * 8 seconds per frame

        expected_wmu = 16 * 8 * 2 + (181 - 129) + 1
        self.assertEqual(MetricsLogger.cumulative_worker_usage_time, expected_wmu)

    def test_2_video_2_workers(self):
        video_2 = create_video_data(180, 16 / 15)
        self.traffic.insert(0, video_2)

        simulation = Simulation(traffic_json_arr=self.traffic,
                                load_balancer_class=MockLoadBalancer,
                                initial_worker_count=2)

        simulation.simulate_traffic()

        # self.assertEqual(MetricsLogger.queue_lengths, [16, 2, 0, 16, 2])
        # self.assertEqual(MetricsLogger.worker_counts, [2, 2, 2, 2, 2])
        self.assertEqual(MetricsLogger.average_video_ready_time, 16 * 8 / 2)

        expected_wmu = 16 * 8 * 2 + ((181 - 65) + 1) * 2
        # self.assertEqual(MetricsLogger.cumulative_worker_usage_time, expected_wmu)
