import sys
import re

import opentimelineio as otio
from PySide2 import QtGui, QtCore, QtWidgets

from app import matrix
import tracks, cells, slider


supported_formats = otio.adapters.suffixes_with_defined_adapters(read=True)
regex = re.compile(r'(\d+|\s+)')

class CompositionSceneSignals(QtCore.QObject):

    remove_track = QtCore.Signal(str)
    lock_track = QtCore.Signal(str)
    unlock_track = QtCore.Signal(str)
    enable_track = QtCore.Signal(str)
    disable_track = QtCore.Signal(str)

    def __init__(self):
        super(CompositionSceneSignals, self).__init__()


class CompositionScene(QtWidgets.QGraphicsScene):
    """ Composition scene widget.
    """
    def __init__(self, composition, *args, **kwargs):
        super(CompositionScene, self).__init__(*args, **kwargs)
        self.DEFAULT_SCENE_HEIGHT = 200
        self.DEFAULT_SCENE_WIDTH = 1000

        # Setting default CompositionScene geometry 1000x200. 
        self.setSceneRect(
              0, 0,
              self.DEFAULT_SCENE_WIDTH,
              self.DEFAULT_SCENE_HEIGHT
            )

        self.timeline_matrix = matrix.Matrix()
        self.scene_signals = CompositionSceneSignals()
        self.connect_signals()

        # Creating header for slider.
        slider_head_brush = QtGui.QBrush(QtGui.QColor(66, 66, 66, 255))
        self.addRect(
              0, 
              self.sceneRect().height() - slider.SLIDER_HEIGHT, 
              tracks.CELL_WIDTH, slider.SLIDER_HEIGHT, 
              brush=slider_head_brush
            )
        
        self._current_y_pos = slider.SLIDER_HEIGHT

        self.slider_rect = self.sceneRect()
        self.slider_rect.setWidth(tracks.CELL_WIDTH)
        self.slider_rect.setHeight(slider.SLIDER_HEIGHT)
        self.slider = slider.Slider(self.slider_rect)
        self.slider.setPos(
              slider.SLIDER_START, 
              self.sceneRect().height() - slider.SLIDER_HEIGHT
            )
        self.slider.setZValue(float('inf'))
        self.addItem(self.slider)

        self.playhead = slider.PlayHead(self._current_y_pos)
        self.playhead.setParentItem(self.slider)

        self._video_tracks_index = 0
        self._audio_tracks_index = 0
        self._data_tracks_index = 0

        self.track_mapping = {
            "V" : 'video',
            "A" : 'audio',
            "D" : 'data',
            "Context" : 'context'
        }

        # self.context_list and self.track_list will remember order of tracks and contexts.
        self.context_list = []
        self.track_list = []

        # self.track_dict will store track object againest tack name for future reference.
        self.track_dict = {}

        # Adding Context track
        self.add_track("Context")

        if composition:
            self.populate_compsition(composition)

    def connect_signals(self):
        """ Connecting timeline matrix signals.
        """
        #conneting scene_signals
        self.scene_signals.remove_track.connect(self.remove_track)
        self.scene_signals.lock_track.connect(self.lock_track)
        self.scene_signals.unlock_track.connect(self.unlock_track)
        self.scene_signals.disable_track.connect(self.disable_track)
        self.scene_signals.enable_track.connect(self.enable_track)

        #conneting matrix_signals
        self.timeline_matrix.matrix_signals.add_new_track.connect(self._add_track)
        self.timeline_matrix.matrix_signals.remove_track.connect(self._remove_track)
        self.timeline_matrix.matrix_signals.remove_context.connect(self._remove_context)
        self.timeline_matrix.matrix_signals.swap_track.connect(self._swap_track)
        self.timeline_matrix.matrix_signals.swap_context.connect(self._swap_context)
        self.timeline_matrix.matrix_signals.add_cell.connect(self._add_item_in_track)
        
    def populate_compsition(self, composition):
        """ Loading composition.
        """

        if isinstance(composition, otio.schema.Stack):
            for _track in composition:
                if _track.kind == otio.schema.TrackKind.Video and list(_track):
                    video_track = self.add_track("video")
                    
                    for index, item in enumerate(_track):
                        video_cell = cells.VideoCell(item)
                        context_name = "context_{}".format(index)
                        if not context_name in self.context_list:
                            self.add_context(context_name)
                        
                        self.add_item_in_track(video_cell,context_name, video_track)

                elif _track.kind == otio.schema.TrackKind.Audio and list(_track):
                    audio_track = self.add_track("audio")
                        
                    for index, item in enumerate(_track):
                        audio_cell = cells.AudioCell(item)
                        context_name = "context_{}".format(index)
                        if not context_name in self.context_list:
                            self.add_context(context_name)

                        self.add_item_in_track(audio_cell,context_name, audio_track)

                elif (
                    _track.kind not in (
                        otio.schema.TrackKind.Video,
                        otio.schema.TrackKind.Audio
                    ) and
                    list(_track)
                ):
                    data_track = self.add_track("data")
                    
                    for index, item in enumerate(_track):
                        data_cell = cells.DataCell(item)
                        context_name = "context_{}".format(index)
                        if not context_name in self.context_list:
                            self.add_context(context_name)

                        self.add_item_in_track(data_cell, context_name, data_track)

    def _adjust_scene_size(self):
        """ Adjust scene size according to number of tracks and contexts.
        """
        # TODO : Need to impliment.

    def update_track_position(self):
        """ Rearange track position after delete a track.
        """
        self._current_y_pos = slider.SLIDER_HEIGHT
        for index, track_name in enumerate(self.track_list):
            self.timeline_matrix.track_dict[track_name] = index - 1
            _track = self.track_dict[track_name]

            track_type = self.track_mapping[regex.split(track_name)[0]]
            _tarck_height = tracks.get_track_height(track_type)
            self._current_y_pos += _tarck_height + 1
            _track.setPos(0, self.sceneRect().height() - self._current_y_pos)

        self.playhead.update_playhead(self._current_y_pos)

    def add_track(self, track_name):
        """ Public method to create new track and add to scene.
            args:
                track_name(str): name of track.
            
            return: None
        """
        if track_name == "video":
            self._video_tracks_index += 1
            track_name = "V{}".format(self._video_tracks_index)

        elif track_name == "audio":
            self._audio_tracks_index += 1
            track_name = "A{}".format(self._audio_tracks_index)

        elif track_name == "data":
            self._data_tracks_index += 1
            track_name = "D{}".format(self._data_tracks_index)

        elif track_name == "Context":
            self._add_track(track_name)
            return  

        self.timeline_matrix.add_new_track(track_name)

        return track_name

    def _add_track(self, track_name):
        """ Private method to create new track and add to scene.
            args:
                track_name(str): name of track.
            
            return: _track(QtWidgets.QGraphicsRectItem)
        """
        track_type = self.track_mapping[regex.split(track_name)[0]]

        track_rect = self.sceneRect()

        if track_type == "video":
            track_rect.setWidth(tracks.CELL_WIDTH * 2)
            track_rect.setHeight(tracks.VIDEO_TRACK_HEIGHT)
            _track = tracks.VideoTrack(
                track_name, track_rect, self
            )

        elif track_type == "audio":
            track_rect.setWidth(tracks.CELL_WIDTH * 2)
            track_rect.setHeight(tracks.AUDIO_TRACK_HEIGHT)
            _track = tracks.AudioTrack(
                track_name, track_rect, self
            )

        elif track_type == "data":
            track_rect.setWidth(tracks.CELL_WIDTH * 2)
            track_rect.setHeight(tracks.DATA_TRACK_HEIGHT)
            _track = tracks.DataTrack(
                track_name, track_rect, self
            )

        elif track_type == "context":
            track_rect.setWidth(tracks.CELL_WIDTH * 2)
            track_rect.setHeight(tracks.CONTEXT_TRACK_HEIGHT)
            _track = tracks.ContextTrack(
                track_name, track_rect, self
            )

        _track.setPos(0, self.sceneRect().height() - self._current_y_pos)
        self.addItem(_track)
        self.track_list.append(track_name)

        self.track_dict[track_name] =  _track
        self.update_track_position()

    def add_context(self, context_name):
        """ Public function to add context.
            args:
                context_name(str): context name
        """
        self.timeline_matrix.add_new_context(context_name)
        self._add_context(context_name)

    def _add_context(self, context_name):
        """ Private function to add context. Slider also updating when a new context added.
            args:
                context_name(str): context name
        """
        context_item = cells.ContextCell(context_name)
        self.track_dict["Context"].add_cell_item(context_item)
        self.context_list.append(context_name)

        # Updating slider width.
        self.slider_rect.setWidth(self.slider_rect.width() + tracks.CELL_WIDTH)
        self.slider.setRect(self.slider_rect)
        # Setting slider width to limit playhead movement.
        self.slider.slider_width = self.slider_rect.width()

    def remove_track(self, track_name):
        """ Public function to remove track.
            args:
                track_name(str): track name
        """
        self.timeline_matrix.remove_track(track_name)

    def _remove_track(self, track_name):
        """ Private function to remove track.
            args:
                track_name(str): track name
        """
        _track = self.track_dict[track_name]
        self.removeItem(_track)
        del self.track_dict[track_name]
        self.track_list.pop(self.track_list.index(track_name))

        self.update_track_position()

    def lock_track(self, track_name):
        """ Locking the selected track.
            args:
                track_name(str): track name
        """
        self.timeline_matrix.lock_track(track_name)

    def unlock_track(self, track_name):
        """ Unocking the selected track.
            args:
                track_name(str): track name
        """
        self.timeline_matrix.unlock_track(track_name)

    def disable_track(self, track_name):
        """ Disabling the selected track.
            args:
                track_name(str): track name
        """
        self.timeline_matrix.disable_track(track_name)

    def enable_track(self, track_name):
        """ Enabling the selected track.
            args:
                track_name(str): track name
        """
        self.timeline_matrix.enable_track(track_name)

    def _remove_context(self):
        return

    def _swap_track(self):
        return

    def _swap_context(self):
        return

    def add_item_in_track(self, cell_item, context, track):
        """ Public function to add cell item to given track.
            args:
                arg_list(list): [item(QtWidgets.QGraphicsRectItem), track(str)]
        """
        self.timeline_matrix.add_cell(cell_item, context, track)

    def _add_item_in_track(self, arg_list):
        """ Private function to add cell item to given track.
            args:
                arg_list(list): [item(QtWidgets.QGraphicsRectItem), track(str)]
        """
        cell_item, track = arg_list
        self.track_dict[track].add_cell_item(cell_item)


class TimelineCompositionView(QtWidgets.QGraphicsView):
    """ Individual view for composition.
    """
    def __init__(self, composition, *args, **kwargs):
        """ Create new composition view and add a new tab.
            args:
                composition: opentimelineio._otio.Stack
        """
        super(TimelineCompositionView, self).__init__(*args, **kwargs)
        self.setAlignment((QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
        self.composition_scene = CompositionScene(composition, parent=self)
        self.setScene(self.composition_scene)


class Timeline(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        """ Create new timeline widget.
        """
        super(Timeline, self).__init__(*args, **kwargs)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(lambda index: self.removeTab(index))

        self._set_timeline()

    def setup_tool_widget(self):
        """ Settin up buttons.
        """
        tool_widget = QtWidgets.QWidget(self)

        tool_widget_horizontal_layout = QtWidgets.QHBoxLayout(tool_widget)

        self.add_track_button = QtWidgets.QPushButton("Add new track", tool_widget)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        tool_widget_horizontal_layout.addWidget(self.add_track_button)
        tool_widget_horizontal_layout.addItem(spacerItem)

        tool_widget.setLayout(tool_widget_horizontal_layout)

        return tool_widget

    def _set_timeline(self, composition=None):
        """ Create new composition view and add a new tab.
            args:
                composition: opentimelineio._otio.Timeline
        """
        tab_name = composition.name if composition else "New"
        stack = composition.tracks if composition else None
        new_tab = QtWidgets.QWidget(self)
        vertical_layout = QtWidgets.QVBoxLayout(new_tab)

        composition_view = TimelineCompositionView(stack, parent=self)
        tool_widget = self.setup_tool_widget()

        # Connecting actions in "add_track_button" to add_track functionality in CompositionScene.
        add_track_menu = QtWidgets.QMenu(self)

        add_track_menu.addAction('Video Track', lambda : composition_view.composition_scene.add_track("video"))
        add_track_menu.addAction('Audio Track', lambda : composition_view.composition_scene.add_track("audio"))
        add_track_menu.addAction('Data Track', lambda : composition_view.composition_scene.add_track("data"))

        self.add_track_button.setMenu(add_track_menu)

        vertical_layout.addWidget(tool_widget)
        vertical_layout.addWidget(composition_view)

        new_tab.setLayout(vertical_layout)
        index = self.addTab(new_tab, tab_name)
        self.setCurrentIndex(index)

    def load_timeline(self, path):
        """ Load timeline.
            args:
                path: str
        """

        file_contents = otio.adapters.read_from_file(
            path
        )
        if isinstance(file_contents, otio.schema.Timeline):
            self._set_timeline(file_contents)

        elif isinstance(file_contents, otio.schema.SerializableCollection):
            # TODO: Need to implement this functionality.
            pass



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    timeline = Timeline()
    timeline.show()
    sys.exit(app.exec_())
