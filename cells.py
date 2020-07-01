from abc import ABCMeta, abstractmethod

from PySide2 import QtGui, QtCore, QtWidgets

from app import video_item, audio_item, data_item, context_item
import icon_items

VIDEO_CELL_HEIGHT = 80
AUDIO_CELL_HEIGHT = 50
DATA_CELL_HEIGHT = 40
CONTEXT_CELL_HEIGHT = 40
CELL_WIDTH = 200

class AbstractBaseCell(QtWidgets.QGraphicsRectItem):
    """ Abstract class for cells.
    """
    def __init__(self, *args, **kwargs):
        super(AbstractBaseCell, self).__init__(*args, **kwargs)
        self.source_name_label = QtWidgets.QGraphicsSimpleTextItem(self)

        self._enable = True
        self._active = True

    @property
    def enable(self):
        return self._enable

    @property
    def active(self):
        return self._active

    @enable.setter
    def enable(self, value):
        self._enable = value
        if value:
            self.enabled_style()

        else:
            self.disabled_style()

    @active.setter
    def active(self, value):
        self._active = value

    @abstractmethod
    def disabled_style(self):
        raise NotImplementedError("Must override disabled_style")

    @abstractmethod
    def enabled_style(self):
        raise NotImplementedError("Must override enabled_style")



class AudioCell(AbstractBaseCell):
    """ Class for audio item.
    """
    def __init__(self, item, *args, **kwargs):
        rect = QtCore.QRectF(0, 0, CELL_WIDTH, AUDIO_CELL_HEIGHT)
        super(AudioCell, self).__init__(rect, *args, **kwargs)
        self.item = item
        self.enabled_style()
        self.source_name_label.setText(self.item.name)
        self.source_name_label.setX(20)
        self.source_name_label.setY(
            (rect.height() -
              self.source_name_label.boundingRect().height()) / 2.0
        )

    def disabled_style(self):
        """ Implementation of AbstractBaseCell.disabled_style
        """
        self.setBrush(
            QtGui.QBrush(
                QtGui.QColor(108, 135, 161, 255)
            )
        )

    def enabled_style(self):
        """ Implementation of AbstractBaseCell.enabled_style
        """
        self.setBrush(
            QtGui.QBrush(
                QtGui.QColor(175, 215, 255, 255)
            )
        )


class VideoCell(AbstractBaseCell):
    """ Class for video item.
    """
    def __init__(self, item, *args, **kwargs):
        rect = QtCore.QRectF( 0, 0, CELL_WIDTH, VIDEO_CELL_HEIGHT)
        super(VideoCell, self).__init__(rect, *args, **kwargs)
        self.item = item
        self.enabled_style()
        self.source_name_label.setText(self.item.name)
        self.source_name_label.setX(20)
        self.source_name_label.setY(
            (rect.height() -
              self.source_name_label.boundingRect().height()) / 2.0
        )

    def disabled_style(self):
        """ Implementation of AbstractBaseCell.disabled_style
        """
        self.setBrush(
            QtGui.QBrush(
                QtGui.QColor(129, 163, 96, 255)
            )
        )

    def enabled_style(self):
        """ Implementation of AbstractBaseCell.enabled_style
        """
        self.setBrush(
            QtGui.QBrush(
                QtGui.QColor(200, 255, 150, 255)
            )
        )


class DataCell(AbstractBaseCell):
    """ Class for data item.
    """
    def __init__(self, *args, **kwargs):
        rect = QtCore.QRectF(0, 0, CELL_WIDTH, DATA_CELL_HEIGHT)
        super(DataCell, self).__init__(rect, *args, **kwargs)
        self.enabled_style()
    
    def disabled_style(self):
        """ Implementation of AbstractBaseCell.disabled_style
        """
        self.setBrush(
            QtGui.QBrush(
                QtGui.QColor(190, 190, 190, 255)
            )
        )

    def enabled_style(self):
        """ Implementation of AbstractBaseCell.enabled_style
        """
        self.setBrush(
            QtGui.QBrush(
                QtGui.QColor(170, 170, 170, 255)
            )
        )


class ContextCell(AbstractBaseCell):
    """ Class for contect item.
    """
    def __init__(self, name, *args, **kwargs):
        rect = QtCore.QRectF(0, 0, CELL_WIDTH, CONTEXT_CELL_HEIGHT)
        super(ContextCell, self).__init__(rect, *args, **kwargs)
        self.enabled_style()
        self.source_name_label.setText(name)
        self.source_name_label.setX(20)
        self.source_name_label.setY(
            (rect.height() -
              self.source_name_label.boundingRect().height()) / 2.0
        )

    def disabled_style(self):
        """ Implementation of AbstractBaseCell.disabled_style
        """
        self.setBrush(
            QtGui.QBrush(
                QtGui.QColor(190, 190, 190, 255)
            )
        )

    def enabled_style(self):
        """ Implementation of AbstractBaseCell.enabled_style
        """
        self.setBrush(
            QtGui.QBrush(
                QtGui.QColor(170, 170, 170, 255)
            )
        )

class TrackHeaderCell(AbstractBaseCell):
    """ Class for header cell item.
    """
    def __init__(self, parent, rect, *args, **kwargs):
        super(TrackHeaderCell, self).__init__(rect, *args, **kwargs)
        self.parent = parent
        self.rect = rect
        self._track_name = parent.track_name
        self.kind = parent.kind
        self.track_name = "{} Track".format(self._track_name)
        self.enabled_style()
        self.set_track_label()
        self.set_icons()

    def set_track_label(self):
        """ Set track label on header cell.
        """
        self.source_name_label.setText(self.track_name)
        self.source_name_label.setX(20)
        self.source_name_label.setY(
            (self.rect.height() -
              self.source_name_label.boundingRect().height()) / 2.0
        )

    def set_icons(self):
        """ Set icons on track header cell.
        """

        if self.kind == "context":
            return

        elif self.kind == "audio":
            mute_icon = icon_items.MuteIconItem(self)
            mute_icon.connet_to(self.parent.toggle_disable_or_enable_track)
            mute_icon.setX(130)
            mute_icon.setY(
                (self.rect.height() -
                self.source_name_label.boundingRect().height()) / 2.0
            )
            mute_icon.show()

        elif self.kind == 'video' or self.kind == "data":

            hide_icon = icon_items.HideIconItem(self)
            hide_icon.connet_to(self.parent.toggle_disable_or_enable_track)
            hide_icon.setX(130)
            hide_icon.setY(
                (self.rect.height() -
                self.source_name_label.boundingRect().height()) / 2.0
            )
            hide_icon.show()

        lock_icon = icon_items.LockIconItem(self)
        lock_icon.connet_to(self.parent.toggle_lock_track)
        lock_icon.setX(150)
        lock_icon.setY(
            (self.rect.height() -
              self.source_name_label.boundingRect().height()) / 2.0
        )
        lock_icon.show()

        delete_icon = icon_items.DeleteIconItem(self)
        delete_icon.connet_to(self.parent.remove_track)
        delete_icon.setX(170)
        delete_icon.setY(
            (self.rect.height() -
              self.source_name_label.boundingRect().height()) / 2.0
        )
        delete_icon.show()

    def disabled_style(self):
        """ Implementation of AbstractBaseCell.disabled_style
        """
        # No need to implement here. Disable option is not applicable for header items
        return

    def enabled_style(self):
        """ Implementation of AbstractBaseCell.enabled_style
        """
        self.setBrush(
            self.parent.header_brush
        )