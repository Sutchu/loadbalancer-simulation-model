class TrafficFinishedError(Exception):
    """
    Raised to indicate that the traffic has finished.
    """
    pass

class VideoNotFullyProcessedException(Exception):
    """
    Raised to indicate that a video is not fully processed.
    """
    pass
