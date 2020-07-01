import os
import sys
import subprocess

from app import timeline_base_item

class AudioItem(timeline_base_item.TimelineBaseItem):
    def __init__(self, audio_path):
        super(AudioItem, self).__init__()
        self.media_reference = audio_path
        self.name = os.path.basename(
            self.media_reference
        )
        self.get_start_frame()
        self.get_end_frame()
        self.get_frame_rate()
        self.media_on_disk = True

    @property
    def frame_rate(self):
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, value):
        self._frame_rate = value

    def get_frame_rate(self):
        """ Get frame rate from media.
        """
        # TODO : Need to implement.
        self.frame_rate = 24.0

    @property
    def start_frame(self):
        return self._start_frame

    @start_frame.setter
    def start_frame(self, value):
        self._start_frame = value

    def get_start_frame(self):
        """ Get start frame from media.
        """
        # TODO : Need to implement.
        self.start_frame = 0

    @property
    def end_frame(self):
        return self._end_frame

    @end_frame.setter
    def end_frame(self, value):
        self._end_frame = value

    def get_end_frame(self):
        """ Get end frame from media.
        """
        # TODO : Need to implement.
        self.end_frame = 50
