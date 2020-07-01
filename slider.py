from PySide2 import QtGui, QtCore, QtWidgets

SLIDER_HEIGHT = 20
SLIDER_START = 200
MARKER_SIZE = 10

class Slider(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(Slider, self).__init__(*args, **kwargs)
        self.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 100, 255)))
        pen = QtGui.QPen()
        pen.setWidth(1)
        self.setPen(pen)
        self._playhead = None
        self._slider_width = SLIDER_START

    def mousePressEvent(self, mouse_event):
        """ Overriding mousePressEvent of QtWidgets.QGraphicsRectItem.
        """
        return

    def mouseMoveEvent(self, mouse_event):
        """ Overriding mouseMoveEvent of QtWidgets.QGraphicsRectItem.
        """
        pos = self.mapToScene(mouse_event.pos())
        # Limiting playhead movement
        if pos.x() >= SLIDER_START and pos.x() <= self.slider_width:
            self._playhead.setX(pos.x() - SLIDER_START)

    @property
    def slider_width(self):
        """ Getter of slider_width.
        """
        return self._slider_width

    @slider_width.setter
    def slider_width(self, value):
        """ Setter of slider_width.
        """
        self._slider_width = value

    def add_playhead(self, play_head):
        """ Adding playhead to slider.
        """
        self._playhead = play_head
        self._playhead.setX(0)

RULER_SIZE = 10

class PlayHead(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, height, *args, **kwargs):
        self.playhead_foot = QtGui.QPolygonF()
        self.playhead_foot.append(QtCore.QPointF(0, 0 ))
        self.playhead_foot.append(QtCore.QPointF(0.5 * RULER_SIZE, 0.5 * RULER_SIZE))
        self.playhead_foot.append(QtCore.QPointF(0.5 * RULER_SIZE, 1.5 * RULER_SIZE))
        self.playhead_foot.append(QtCore.QPointF(-0.5 * RULER_SIZE, 1.5 * RULER_SIZE))
        self.playhead_foot.append(QtCore.QPointF(-0.5 * RULER_SIZE, 0.5 * RULER_SIZE))
        self.playhead_foot.append(QtCore.QPointF(0, 0))

        super(PlayHead, self).__init__(self.playhead_foot, *args, **kwargs)
        self.playhead_bar = QtWidgets.QGraphicsLineItem(0, 0, 0, -height, self)

        self.setBrush(
            QtGui.QBrush(QtGui.QColor(50, 255, 20, 255))
        )

    def update_playhead(self, height):
        """ Updating playhead bar with respect track height.
        """
        self.playhead_bar.setLine(0, 0, 0, -height)

    def setParentItem(self, slider):
        """ Subclass in order to add the rule to the slider item.
        """
        slider.add_playhead(self)
        super(PlayHead, self).setParentItem(slider)
