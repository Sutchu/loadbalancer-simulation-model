from enum import Enum

class SimulationEventEnum(Enum):
    """
    Enum class for simulation events.
    """
    VIDEO_ADDED_FROM_TRAFFIC = 1
    WORKER_FINISHED_PROCESSING = 2
    LOAD_BALANCER_CHECK = 3
    ADD_WORKERS = 4
    REMOVE_WORKERS = 5

    def __str__(self):
        return self.name