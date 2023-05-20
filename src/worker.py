from .video import Video


class Worker:
    def __init__(self):
        self._video: Video = None

    def finish_processing_frame(self, current_simulation_time):
        if self._video:
            self._video.mark_frame_as_processed(current_simulation_time)

        self._video = None

    def assign_video(self, video: Video):
        video.mark_frame_as_processing()
        self._video = video

    @property
    def is_busy(self):
        return self._video is not None
