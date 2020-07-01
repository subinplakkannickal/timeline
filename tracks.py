from PySide2 import QtGui, QtCore, QtWidgets

import opentimelineio as otio

import cells


VIDEO_TRACK_HEIGHT = cells.VIDEO_CELL_HEIGHT
AUDIO_TRACK_HEIGHT = cells.AUDIO_CELL_HEIGHT
DATA_TRACK_HEIGHT = cells.DATA_CELL_HEIGHT
CONTEXT_TRACK_HEIGHT = cells.CONTEXT_CELL_HEIGHT
CELL_WIDTH = cells.CELL_WIDTH

def get_track_height(track_type):
    if track_type == "video": return VIDEO_TRACK_HEIGHT
    elif track_type == "audio": return AUDIO_TRACK_HEIGHT
    elif track_type == "data": return DATA_TRACK_HEIGHT
    elif track_type == "context": return CONTEXT_TRACK_HEIGHT


class AbstractBaseTrack(QtWidgets.QGraphicsRectItem):
    """ Abstract base class for tracks.
    """
    def __init__(self, item, parent, *args, **kwargs):
        super(AbstractBaseTrack, self).__init__(*args, **kwargs)
        self.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        self.track_name = None
        self.scene = parent
        self.acvtive = True
        self.enable = True

    def remove_track(self):
        """ Base function to delete a track.
        """
        self.scene.scene_signals.remove_track.emit(self.track_name)

    def toggle_lock_track(self, state):
        """ Base function to lock or unlock a track.
            args:
                state(bool): True for lock and False for unlock.
        """
        self.active = state
        if self.active:
            self.scene.scene_signals.unlock_track.emit(self.track_name)
            
        else:
            self.scene.scene_signals.lock_track.emit(self.track_name)

    def toggle_disable_or_enable_track(self, state):
        """ Base function to disable or enable track.
            args:
                state(bool): True for disable and False for enable.
        """
        self.enable = state
        if self.enable:
            self.scene.scene_signals.enable_track.emit(self.track_name)
            
        else:
            self.scene.scene_signals.disable_track.emit(self.track_name)

class AudioTrack(AbstractBaseTrack):
    """ Implementation of Audio track.
    """
    def __init__(self, track_name, rect, parent, *args, **kwargs):
        super(AudioTrack, self).__init__(rect, parent, *args, **kwargs)
        self.kind = "audio"
        self.track_name = track_name
        rect.setWidth(CELL_WIDTH)
        rect.setHeight(AUDIO_TRACK_HEIGHT)
        self.header_brush = QtGui.QBrush(
              QtGui.QColor(150, 200, 255, 255)
            )
        self.header_cell = cells.TrackHeaderCell(self, rect)
        self.header_cell.setParentItem(self)
        self.cell_start_position = 0
    
    def add_cell_item(self, audio_cell):
        self.cell_start_position += 200
        audio_cell.setPos(self.cell_start_position, 0)
        audio_cell.setParentItem(self)


class VideoTrack(AbstractBaseTrack):
    """ Implementation of Video track.
    """
    def __init__(self, track_name, rect, parent, *args, **kwargs):
        super(VideoTrack, self).__init__(rect, parent, *args, **kwargs)
        self.kind = "video"
        self.track_name = track_name
        rect.setWidth(CELL_WIDTH)
        rect.setHeight(VIDEO_TRACK_HEIGHT)
        self.header_brush = QtGui.QBrush(
              QtGui.QColor(165, 255, 100, 255)
            )
        self.header_cell = cells.TrackHeaderCell(self, rect)
        self.header_cell.setParentItem(self)
        self.cell_start_position = 0

    def add_cell_item(self, video_cell):
        self.cell_start_position += 200
        video_cell.setPos(self.cell_start_position, 0)
        video_cell.setParentItem(self)


class DataTrack(AbstractBaseTrack):
    """ Implementation of Data track.
    """
    def __init__(self, track_name, rect, parent, *args, **kwargs):
        super(DataTrack, self).__init__(rect, parent, *args, **kwargs)
        self.kind = "data"
        self.track_name = track_name
        rect.setWidth(CELL_WIDTH)
        rect.setHeight(DATA_TRACK_HEIGHT)
        self.header_brush = QtGui.QBrush(
              QtGui.QColor(176, 102, 255, 255)
            )
        self.header_cell = cells.TrackHeaderCell(self, rect)
        self.header_cell.setParentItem(self)


class ContextTrack(AbstractBaseTrack):
    """ Implementation of Context track.
    """
    def __init__(self, track_name, rect, parent, *args, **kwargs):
        super(ContextTrack, self).__init__(rect, parent, *args, **kwargs)
        self.kind = "context"
        self.track_name = track_name
        rect.setWidth(CELL_WIDTH)
        rect.setHeight(CONTEXT_TRACK_HEIGHT)
        self.header_brush = QtGui.QBrush(
              QtGui.QColor(120, 120, 120, 255)
            )    
        header_cell = cells.TrackHeaderCell(self, rect)
        header_cell.setParentItem(self)
        self.cell_start_position = 0

    def add_cell_item(self, context_cell):
        self.cell_start_position += 200
        context_cell.setPos(self.cell_start_position, 0)
        context_cell.setParentItem(self)
