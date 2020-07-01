import os
import sys
from PySide2 import QtGui, QtCore, QtWidgets

import timeline

class TimelineConsole(QtWidgets.QMainWindow):
    """ Timeline panel main window.
    """
    def __init__(self):
        super(TimelineConsole, self).__init__()
        self._current_file = None

        self.setup_ui()
        self.show()

    def setup_ui(self):
        """ UI setup
        """
        self.setWindowTitle('OpenTimelineIO Viewer')
        self.setStyleSheet(open('stylesheet.css').read())
        self.setup_menubar()

        self.timeline = timeline.Timeline(
            parent=self
        )

        root = QtWidgets.QWidget(parent=self)
        layout = QtWidgets.QVBoxLayout(root)
        layout.addWidget(self.timeline)
        self.setCentralWidget(root)

    def setup_menubar(self):
        """ Menubar setup.
        """
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        create_new_menu = file_menu.addMenu('&Create New')

        from_file_action = QtWidgets.QAction('From Editorial', create_new_menu)
        from_file_action.triggered.connect(self.load_timeline_from_file)

        from_clip_action = QtWidgets.QAction('From Clip', create_new_menu)
        from_clip_action.triggered.connect(self.load_timeline_from_clip)
        from_clip_action.setEnabled(False)

        create_new_menu.addAction(from_file_action)
        create_new_menu.addAction(from_clip_action)

        exit_action = QtWidgets.QAction('&Exit', menubar)
        exit_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(exit_action)

    def load_timeline_from_file(self):
        """ Open file browser and load timeline from selected edl/otio file.
        """
        start_folder = "/home/{user}".format(user=os.getenv("USER"))

        if self._current_file is not None:
            start_folder = os.path.dirname(self._current_file)

        extensions = timeline.supported_formats

        extensions_string = ' '.join('*.{}'.format(x) for x in extensions)

        path = QtWidgets.QFileDialog.getOpenFileName(
                self,
                'Open OpenTimelineIO',
                start_folder,
                'OTIO ({extensions})'.format(extensions=extensions_string)
            )[0]

        self.timeline.load_timeline(path)
        self._current_file = path

    def load_timeline_from_clip(self):
        """ Open file browser and load timeline from selected clip(s).
        """
        start_folder = "/home/{user}".format(user=os.getenv("USER"))

        if self._current_file is not None:
            start_folder = os.path.dirname(self._current_file)

        # TODO: Need to handle video_extensions in configuration.
        video_extensions = ("mov", "mp4")
        video_extensions_string = " ".join('*.{}'.format(x) for x in video_extensions)

        _path = QtWidgets.QFileDialog.getOpenFileNames(
                self,
                'Open Clips',
                start_folder,
                'Videos ({video_extensions})'.format(video_extensions=video_extensions_string)
            )[0]
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    timeline_console = TimelineConsole()
    sys.exit(app.exec_())
