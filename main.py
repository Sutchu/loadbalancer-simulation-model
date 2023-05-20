from src.load_balancers.load_balancer import LoadBalancer
from src.simulation import Simulation
from src.metrics_logger import MetricsLogger

import json

# Load traffic
with open('ExampleTraffic.json') as f:
    traffic_json = json.load(f)


# Simulation
simulation = Simulation(traffic_json_arr=traffic_json, load_balancer_class=LoadBalancer)
simulation.simulate_traffic()
simulation_metrics: MetricsLogger = simulation.metrics_logger


# Metrics
print("Average VRT: %s" % simulation_metrics.average_video_ready_time)
print("WMU: %s" % simulation_metrics.cumulative_worker_usage_time)
queue_sizes = simulation_metrics.queue_lengths
worker_counts = simulation_metrics.worker_counts


# Plotting
from src.helpers.simulation_graph_plotter import SimulationGraphPlotter

plotter = SimulationGraphPlotter(metrics_logger=simulation_metrics)
plotter.plot()

