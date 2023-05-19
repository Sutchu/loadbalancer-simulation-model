from src.video import Video
from src.loadbalancer import LoadBalancer

import json

with open('ExampleTraffic.json') as f:
    traffic_json = json.load(f)

# def data(time, dur):
#     return {'properties': {'time': time, 'Duration': dur}}
# traffic_json = []
# for i in range(10,-1,-1):
#     seconds = 120
#     traffic_json.append(data(i*seconds, 10))

initial_video_timestamp = traffic_json[-1]['properties']['time']
traffic = [Video(data, initial_video_timestamp) for data in traffic_json]

del traffic_json # Free memory as we don't need it anymore

# Simulation
from src.simulation import Simulaion
simulation = Simulaion(traffic, LoadBalancer)
queue_sizes, worker_counts = simulation.simulate_traffic()


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
