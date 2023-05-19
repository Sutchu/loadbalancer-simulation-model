from typing import Callable


class Video:
    def __init__(self, video_json, initial_video_timestamp, on_fully_processed: Callable):
        self.on_fully_processed = on_fully_processed
        # Timestamp in seconds starting from 0 to simplify calculations
        self.timestamp = int(video_json['properties']['time'] - initial_video_timestamp) + 1

        self._unprocessed_frame_count = int(video_json['properties']['Duration'] * 15)
        self._processing_frame_count = 0
        self._processed_frame_count = 0

        # VRT, time it took to process this video. Calculation is finished when self.frames is 0
        self.video_ready_time = 0

    def calculate_video_ready_time(self, finished_time):
        self.video_ready_time = finished_time - self.timestamp

    def mark_frame_as_processing(self) -> bool:
        if self._unprocessed_frame_count == 0:
            return False

        self._unprocessed_frame_count -= 1
        self._processing_frame_count += 1
        return True

    def mark_frame_as_processed(self, current_simulation_time):
        self._processing_frame_count -= 1
        self._processed_frame_count += 1

        if self.is_fully_processed:
            self.calculate_video_ready_time(current_simulation_time)
            self.on_fully_processed(self)

    @property
    def is_fully_processed(self):
        return self._unprocessed_frame_count == 0 and self._processing_frame_count == 0

    @property
    def has_unprocessed_frames(self):
        return self._unprocessed_frame_count > 0