from abc import ABCMeta, abstractmethod

from PySide2 import QtGui, QtCore, QtWidgets


class BaseIconItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, parent, icon_pixmap, alt=None):
        super(BaseIconItem, self).__init__(icon_pixmap, parent)
        self.alt = alt
        self.icon_pixmap = icon_pixmap
        self.state = True
        self.connection = None

    @abstractmethod
    def execute_connection(self):
        raise NotImplementedError("Must override execute_connection")
    
    def mousePressEvent(self, mouseEvent):
        """ Overriding mousePressEvent of QtWidgets.QGraphicsPixmapItem.
        """
        if mouseEvent.button() == QtCore.Qt.LeftButton:
            # Toggling icon
            if self.alt:
                self.setPixmap(self.alt)
                self.alt, self.icon_pixmap = self.icon_pixmap, self.alt

            # Toggling the state.
            self.state = not self.state
            self.execute_connection()


        super(BaseIconItem, self).mousePressEvent(mouseEvent)

    def connet_to(self, slot):
        """ Setting callable as connection.
        """
        # Checking whether slot is callable.
        if callable(slot):
            self.connection = slot



class HideIconItem(BaseIconItem):
    """ Implementation of Hide/show icon
    """
    def __init__(self, parent):
        super(HideIconItem, self).__init__(parent, "images/hide.png", "images/show.png")

    def execute_connection(self):
        """ Implimentation of BaseIconItem.execute_connection.
        """
        if self.connection:
            self.connection(self.state)



class MuteIconItem(BaseIconItem):
    """ Implementation of mute/audio icon
    """
    def __init__(self, parent):
        super(MuteIconItem, self).__init__(parent, "images/mute.png", "images/audio.png")

    def execute_connection(self):
        """ Implimentation of BaseIconItem.execute_connection.
        """
        if self.connection:
            self.connection(self.state)



class LockIconItem(BaseIconItem):
    """ Implementation of Lock/unlock icon
    """
    def __init__(self, parent):
        super(LockIconItem, self).__init__(parent, "images/unlock.png", "images/lock.png")

    def execute_connection(self):
        """ Implimentation of BaseIconItem.execute_connection.
        """
        if self.connection:
            self.connection(self.state)



class DeleteIconItem(BaseIconItem):
    """ Implementation of bin icon
    """
    def __init__(self, parent):
        super(DeleteIconItem, self).__init__(parent, "images/bin.png")

    def execute_connection(self):
        """ Implimentation of BaseIconItem.execute_connection.
        """
        if self.connection:
            self.connection()

