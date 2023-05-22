import json

from src.metrics_logger import MetricsLogger
from src.simulation import Simulation

from src.load_balancers.part1_load_balancer import Part1LoadBalancer
from src.load_balancers.part2_load_balancer import Part2LoadBalancer
from src.load_balancers.pd_load_balancer import PDLoadBalancer

import sys

def read_json_run_sim_plot_results(input_json, load_balancer_class):
    # Load traffic
    with open(input_json) as f:
        traffic_json = json.load(f)

    # Simulation
    simulation = Simulation(traffic_json_arr=traffic_json, load_balancer_class=load_balancer_class)
    simulation.simulate_traffic()

    # Metrics
    print("Average VRT: %s" % MetricsLogger.average_video_ready_time)
    print("WMU: %s" % MetricsLogger.cumulative_worker_usage_time)

    # Plotting
    from src.helpers.simulation_graph_plotter import SimulationGraphPlotter

    plotter = SimulationGraphPlotter()
    plotter.plot()

if __name__ == "__main__":
    # get kwargs of
    try:
        load_balancer_class_name = sys.argv[1]
        if load_balancer_class_name == "PDLoadBalancer":
            load_balancer_class = PDLoadBalancer
        elif load_balancer_class_name == "Part1LoadBalancer":
            load_balancer_class = Part1LoadBalancer
        elif load_balancer_class_name == "Part2LoadBalancer":
            load_balancer_class = Part2LoadBalancer
        else:
            raise Exception("Invalid load balancer class name")

        if len(sys.argv) > 2:
            input_json_path = sys.argv[2]
        else:
            input_json_path = 'ExampleTraffic.json'

    except IndexError:
        raise Exception("Invalid run command, must be of form: python main.py <load_balancer_class_name> <input_json_path>")

    read_json_run_sim_plot_results(input_json_path, load_balancer_class)
