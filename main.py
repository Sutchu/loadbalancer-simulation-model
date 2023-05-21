import json

from src.metrics_logger import MetricsLogger
from src.simulation import Simulation
from src.load_balancers.load_balancer import LoadBalancer
from src.load_balancers.pid_load_balancer import PIDLoadBalancer

import sys


# Load traffic
with open('ExampleTraffic.json') as f:
    traffic_json = json.load(f)

# get kwargs of
if len(sys.argv) > 1:
    load_balancer_class_name = sys.argv[1]
    if load_balancer_class_name == "PIDLoadBalancer":
        load_balancer_class = PIDLoadBalancer

    elif load_balancer_class_name == "LoadBalancer":
        load_balancer_class = LoadBalancer

    else:
        raise Exception("Invalid load balancer class name")
else:
    load_balancer_class = LoadBalancer

# Simulation
simulation = Simulation(traffic_json_arr=traffic_json, load_balancer_class=load_balancer_class)
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