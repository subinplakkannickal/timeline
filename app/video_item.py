import os
import sys
import subprocess

from app import timeline_base_item

class VideoItem(timeline_base_item.TimelineBaseItem):
    def __init__(self, media_path):
        super(VideoItem, self).__init__()
        self.media_reference = media_path
        self.name = os.path.basename(
            self.media_reference
        )
        self.get_thumpnail()
        self.get_start_frame()
        self.get_end_frame()
        self.get_frame_rate()
        self.media_on_disk = True
        self.is_non_vfx = False
        self.has_audio = False


    @property
    def thumbnail(self):
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value):
        self._thumbnail = value

    def get_thumpnail(self):
        """ Get thumbnail of video.
        """
        _thumbnail_path = os.path.join(
            os.path.dirname(
                self.media_reference
            ), 
            "thumbnail_{}.png".format(
                os.path.splitext(
                    os.path.basename(
                        self.media_reference
                    )
                )[0], 
            )
        )
        self.thumbnail = _thumbnail_path
        if not  os.path.exists(_thumbnail_path):
            subprocess.call(['ffmpeg', '-i', self.media_reference, '-ss', '00:00:00.000', '-vframes', '1', '-s', '106x80', _thumbnail_path])

    @property
    def frame_rate(self):
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, value):
        self._frame_rate = value

    def get_frame_rate(self):
        """ Get framae rate of video.
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
        """ Get start frame of video.
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
        """Get end_frame of video.
        """
        # TODO : Need to implement.
        self.end_frame = 50
