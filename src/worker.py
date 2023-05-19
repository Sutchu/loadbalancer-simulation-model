from .video import Video

class Worker:
    def __init__(self, video_queue):
        self._video: Video = None
        self._video_queue = video_queue

    def finish_processing_frame(self, current_simulation_time, vrt_arrray):
        if self._video:
            self._video.mark_frame_as_processed()

            if self._video.is_fully_processed:
                self._video.calculate_video_ready_time(current_simulation_time)
                vrt_arrray.append(self._video.video_ready_time)
        self._video = None

    def process_new_frame(self) -> bool:
        if self._video_queue:
            while self._video_queue:
                self._video = self._video_queue[0]  # Peek at the first video in the queue
                if not self._video.mark_frame_as_processing():
                    self._video_queue.popleft()
                    continue
                break

            return True
        return False
