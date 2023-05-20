from src.loadbalancer import LoadBalancer
from src.simulation import Simulation
from src.metrics_logger import MetricsLogger

import json

with open('ExampleTraffic.json') as f:
    traffic_json = json.load(f)

# Simulation
simulation = Simulation(traffic_json_arr=traffic_json, load_balancer_class=LoadBalancer)
simulation.simulate_traffic()
simulation_metrics: MetricsLogger = simulation.metrics_logger

print("Average VRT: %s" % simulation_metrics.average_video_ready_time)
print("WMU: %s" % simulation_metrics.cumulative_worker_usage_time)
queue_sizes = simulation_metrics.queue_lengths
worker_counts = simulation_metrics.worker_counts
# Plot Graphs
import matplotlib.pyplot as plt

# Generate timepoints
timepoints = range(len(queue_sizes))

# Initialize a new figure
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot number of images in the processing queue vs time
ax1.plot(timepoints, queue_sizes, label='Number of Images in Queue', linewidth=0.8)
ax1.set_xlabel('Time (minutes)')
ax1.set_ylabel('Number of Images in Queue')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot number of operating worker machines vs time
ax2.plot(timepoints, worker_counts, label='Number of Operating Workers', color='orange', linewidth=0.8)
ax2.set_ylabel('Number of Operating Workers', color='orange')

# Set title and legend
ax1.set_title('Number of Images in the Processing Queue and Number of Operating Workers Over Time')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Gridlines
ax1.grid(True)
# Show the figure
plt.show()
