import numpy as np
from PySide2 import QtCore


class MatrixSignals(QtCore.QObject):

    add_new_track = QtCore.Signal(str)
    add_new_context = QtCore.Signal(str)
    remove_track = QtCore.Signal(str)
    remove_context = QtCore.Signal(str)
    swap_track = QtCore.Signal()
    swap_context = QtCore.Signal()
    add_cell = QtCore.Signal(object)
    resolve_matrix = QtCore.Signal()

    def __init__(self):
        super(MatrixSignals, self).__init__()


class Matrix(object):
    def __init__(self): 
        self.matrix_signals = MatrixSignals()
        self.matrix = np.empty((0,0), object)
        self._context_dict = {}
        self.track_dict = {}

    def add_new_track(self, track):
        """ Add a new row at the end.
            args:
                track(str): track name.
        """
        if track in self.track_dict:
            raise Exception("Sorry, {} is already present in timeline matrix".format(track))

        current_shape = self.matrix.shape
        self.matrix = np.insert(self.matrix, current_shape[1], None, axis=1)
        self.track_dict[track] = current_shape[1]
        self.matrix_signals.add_new_track.emit(track)
        # TODO: Need to resolve matrix

    def add_new_context(self, context):
        """ Add a new column at the end.
            args:
                context(str): context name.
        """
        if context in self._context_dict:
            raise Exception("Sorry, {} is already present in timeline matrix".format(context))

        current_shape = self.matrix.shape
        self.matrix = np.insert(self.matrix, current_shape[0], None, axis=0)
        self._context_dict[context] = current_shape[0]
        self.matrix_signals.add_new_context.emit(context)
        # TODO: Need to resolve matrix

    def remove_track(self, track):
        """ remove a row at the given index.
            args:
                track(str): name of track to be removed.
        """
        if not track in self.track_dict:
            raise Exception("Sorry, {} is not present in timeline matrix".format(track))

        self.matrix = np.delete(self.matrix, self.track_dict[track], axis=1)
        del self.track_dict[track]
        self.matrix_signals.remove_track.emit(track)
        # TODO: Need to resolve matrix

    def remove_context(self, context):
        """ remove a column at the given index.
            args:
                context(str): name of context to be removed.
        """
        if not context in self._context_dict:
            raise Exception("Sorry, {} is not present in timeline matrix".format(context))

        self.matrix = np.delete(self.matrix, self._context_dict[context], axis=0)
        del self._context_dict[context]
        self.matrix_signals.remove_context.emit(context)
        # TODO: Need to resolve matrix

    def lock_track(self, track):
        """ Lock the given track.
            args:
                track(str): name of track to be locked.
        """
        for item in self.get_track_items(track):
            item.active = False

    def unlock_track(self, track):
        """ Unock the given track.
            args:
                track(str): name of track to be unlocked.
        """
        for item in self.get_track_items(track):
            item.active = True

    def disable_track(self, track):
        """ Disable the given track.
            args:
                track(str): name of track to be disabled.
        """
        for item in self.get_track_items(track):
            item.enable = False

        # TODO: Need to resolve matrix

    def enable_track(self, track):
        """ Enable the given track.
            args:
                track(str): name of track to be enabled.
        """
        for item in self.get_track_items(track):
            item.enable = True

        # TODO: Need to resolve matrix

    def swap_track(self, track, new_index):
        """ remove a row at the given index.
            args:
                track(str): name of track to be swapped.
                new_index(int): new position of row.
        """
        if not track in self.track_dict:
            raise Exception("Sorry, {} is not present in timeline matrix".format(track))

        _track = self.matrix[:, self.track_dict[track]]
        self.matrix = np.delete(self.matrix, self.track_dict[track], axis=1)
        self.matrix = np.insert(self.matrix, new_index, _track, axis=1)
        self.matrix_signals.swap_track.emit()
        # TODO: Need to resolve matrix

    def swap_context(self, context, new_index):
        """ remove a column at the given index.
            args:
                context(str): name of context to be swapped.
                new_index(int): new position of context.
        """
        if not context in self._context_dict:
            raise Exception("Sorry, {} is not present in timeline matrix".format(context))

        _context = self.matrix[self._context_dict[context], :]
        self.matrix = np.delete(self.matrix, self._context_dict[context], axis=0)
        self.matrix = np.insert(self.matrix, new_index, _context, axis=0)
        self.matrix_signals.swap_context.emit()
        # TODO: Need to resolve matrix

    def add_cell(self, cell, context, track):
        """ Add cell to given context and track.
        args:
            cell(QtWidgets.QGraphicsRectItem): Cell item to be added to timeline.
            context(str): Track name
            track(str): Context name
        """
        if not context in self._context_dict:
            raise Exception("Sorry, {} is not present in timeline matrix".format(context))

        if not track in self.track_dict:
            raise Exception("Sorry, {} is not present in timeline matrix".format(track))

        track_index = self.track_dict[track]
        context_index = self._context_dict[context]
        self.matrix[context_index, track_index] = cell
        self.matrix_signals.add_cell.emit([cell, track])
        # TODO: Need to resolve matrix

    def get_track_items(self, track):
        """ Get items in track.
            args:
                track(str): Track name.
        """
        if not track in self.track_dict:
            raise Exception("Sorry, {} is not present in timeline matrix".format(track))

        return self.matrix[:, self.track_dict[track]]

    def get_context_items(self, context):
        """ Get items in context.
            args:
                context(str): context name.
        """
        if not context in self._context_dict:
            raise Exception("Sorry, {} is not present in timeline matrix".format(context))

        return self.matrix[self._context_dict[context], :]

    def resolve_matrix(self):
        """ Resolve the matrix.
        """
        self.matrix_signals.resolve_matrix.emit()
