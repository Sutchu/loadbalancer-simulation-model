import matplotlib.pyplot as plt

from ..metrics_logger import MetricsLogger


class SimulationGraphPlotter:
    def __init__(self, metrics_logger: MetricsLogger):
        self._metrics_logger = metrics_logger

        self.queue_sizes = self._metrics_logger.queue_lengths
        self.worker_counts = self._metrics_logger.worker_counts

    def plot(self):
        print("Plotting...")
        print("If running from the command line, close the plot window to stop the program.")
        # Generate timepoints
        timepoints = range(len(self.queue_sizes))

        # Initialize a new figure
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot number of images in the processing queue vs time
        ax1.plot(timepoints, self.queue_sizes, label='Number of Images in Queue', linewidth=0.8)
        ax1.set_xlabel('Time (minutes)')
        ax1.set_ylabel('Number of Images in Queue')

        # Create a secondary y-axis
        ax2 = ax1.twinx()

        # Plot number of operating worker machines vs time
        ax2.plot(timepoints, self.worker_counts, label='Number of Operating Workers', color='orange', linewidth=0.8)
        ax2.set_ylabel('Number of Operating Workers', color='orange')

        # Set title and legend
        ax1.set_title('Number of Images in the Processing Queue and Number of Operating Workers Over Time')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Gridlines
        ax1.grid(True)
        # Show the figure
        plt.show()