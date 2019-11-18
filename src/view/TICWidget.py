import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, \
    QHBoxLayout, QWidget, QDesktopWidget, \
    QAction, QFileDialog, QTableView, QSplitter, \
    QMenu, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal, QItemSelectionModel, QSortFilterProxyModel, QSignalMapper, \
    QPoint, QRegExp, QRectF

import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np
from collections import namedtuple

from scipy.signal import find_peaks

import pyopenms


pg.setConfigOption('background', 'w')  # white background
pg.setConfigOption('foreground', 'k')  # black peaks


class TICWidget(PlotWidget):

    def __init__(self, parent=None, dpi=100):
        PlotWidget.__init__(self)
        self.setLimits(yMin=0, xMin=0)
        self.setMouseEnabled(y=False)
        self.setLabel('bottom', 'RT')
        self.setLabel('left', 'intensity')
        self._peak_labels = {}
        # numpy arrays for fast look-up
        self._rts = np.array([])
        self._ints = np.array([])
        self.getViewBox().sigXRangeChanged.connect(self._autoscaleYAxis)
        self.getViewBox().sigXRangeChanged.connect(self._redrawLabels)

    def setTIC(self, chromatogram):
        # delete old highlighte "hover" peak
        if self._peak_labels != {}:
            self.removeItem(self._peak_labels)
            self._peak_labels = {}
        self.chrom = chromatogram
        self._rts, self._ints = self.chrom.get_peaks()
        self._autoscaleYAxis()
        # for annotation in ControllerWidget
        self.minRT = np.amin(self._rts)
        self.maxRT = np.amax(self._rts)

        self._redrawPlot()


    def _redrawPlot(self):
        self.plot(clear=True)
        self._plot_tic()
        self._plot_peak_label()



    def _autoscaleYAxis(self):
        x_range = self.getAxis('bottom').range
        if x_range == [0, 1]:  # workaround for axis sometimes not being set TODO: check if this is resovled
            x_range = [np.amin(self._rts), np.amax(self._rts)]
        self.currMaxY = self._getMaxIntensityInRange(x_range)
        if self.currMaxY:
            self.setYRange(0, self.currMaxY, update=False)


    def _getMaxIntensityInRange(self, xrange):
        left = np.searchsorted(self._rts, xrange[0], side='left')
        right = np.searchsorted(self._rts, xrange[1], side='right')
        return np.amax(self._ints[left:right], initial=1)

    def _plot_tic(self):
        plotgraph = pg.PlotDataItem(self._rts,self._ints)
        self.addItem(plotgraph)


    def _currentIntensitiesInRange(self):
        x_range = self.getAxis('bottom').range
        #print(x_range, "\n", self._rts)
        left = np.searchsorted(self._rts, x_range[0], side='left')
        right = np.searchsorted(self._rts, x_range[1], side='right')
        #print(left, right, self._rts[left], self._rts[right - 1])
        current_ints = self._ints[left:right+1]
        return current_ints


    def _find_Peak(self):
        array = self._ints
        maxIndex = np.zeros_like(array)
        peakValue = -np.inf
        for i in range(0, len(array), 1):
            if peakValue < array[i]:
                peakValue = array[i]
                for j in range(i, len(array)):
                    if peakValue < array[j]:
                        break
                    elif peakValue == array[j]:
                        continue
                    elif peakValue > array[j]:
                        peakIndex = i + np.floor(abs(i - j) / 2)
                        maxIndex[peakIndex.astype(int)] = 1
                        i = j
                        break
            peakValue = array[i]
        maxIndex = np.where(maxIndex)[0]

        return maxIndex

    def _add_label(self, label_id, label_text, pos_x, pos_y):

        label = pg.TextItem(anchor=(0.5, 1))
        label.setText(text='{0:.3f}'.format(label_text), color=(100, 100, 100))
        label.setPos(pos_x, pos_y)
        self._peak_labels[label_id] = {'label': label}

        if self._label_clashes(label_id):
            self.addItem(label)
        else:
            del self._peak_labels[label_id]



    def _remove_label(self, label_id):
        if label_id in self._peak_labels:
            self.removeItem(self._peak_labels[label_id]['label'])
            del self._peak_labels[label_id]


    # TODO:
    # 1) search for the labels without intersections.
    # 2) use a prioritized function remove the lesser prioritized labels (only maxima remain)

    def _label_priorities(self, label_id):
        #print(self._peak_labels)
        rect1 = self.getViewBox().itemBoundingRect(self._peak_labels[label_id]['label'])

        for item in list(self._peak_labels):
            if item != label_id:
                rect2 = self.getViewBox().itemBoundingRect(self._peak_labels[item]['label'])
                if rect1.intersects(rect2):
                    self._remove_label(item)



    def _label_clashes(self, label_id):
        new_label = label_id
        # TODO change distance with real intersections of labels
        # overlapping of labels -> will not be added
        limit_distance = 10
        noclash = False

        if self._peak_labels == {}:
            noclash = True

        else:
            if self._peak_labels != {}:
                for ex_label in list(self._peak_labels):
                    if ex_label != new_label:
                        new_label_X = self._peak_labels[new_label]['label'].x()
                        ex_label_X = self._peak_labels[ex_label]['label'].x()

                        distance = abs(new_label_X - ex_label_X)

                        if distance < limit_distance:
                            noclash = False
                            break
                        elif distance > limit_distance:
                            noclash = True
                    else:
                        if len(self._peak_labels) == 1 and ex_label == new_label:
                            noclash = True

        return noclash



    def _plot_peak_label(self):
        # alternative finding peak with scipy
        #peak_index = find_peaks(self._ints, distance=10)[0]

        # alternative with finding the local maxima (slower)
        peak_index = self._find_Peak()

        if self._peak_labels == {}:
            for index in peak_index:
                if self._ints[index] in self._currentIntensitiesInRange():
                    self._add_label(index, self._ints[index], self._rts[index], self._ints[index])

        else:
            if self._peak_labels != {}:
                # check existing labels within x_range
                for id in list(self._peak_labels):
                    if self._ints[id] in self._currentIntensitiesInRange():
                        pass
                    else:
                        self._remove_label(id)

            # re-add labels zooming out
            for index in peak_index:
                if index not in self._peak_labels:
                    if self._ints[index] in self._currentIntensitiesInRange():
                        self._add_label(index, self._ints[index], self._rts[index], self._ints[index])



    def _redrawLabels(self):
        self._plot_peak_label()