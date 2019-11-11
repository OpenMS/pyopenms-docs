import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, \
    QHBoxLayout, QWidget, QDesktopWidget, \
    QAction, QFileDialog, QTableView, QSplitter, \
    QMenu, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal, QItemSelectionModel, QSortFilterProxyModel, QSignalMapper, \
    QPoint, QRegExp

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
        self.highlighted_peak_label = None
        self.peak_labels = None
        self.peak_annotations = None
        # numpy arrays for fast look-up
        self._mzs = np.array([])
        self._ints = np.array([])
        self.getViewBox().sigXRangeChanged.connect(self._autoscaleYAxis)
        self.getViewBox().sigXRangeChanged.connect(self._redrawPeaks)
        #self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60, slot=self._onMouseMoved)

    def setSpectrum(self, spectrum):
        # delete old highlighte "hover" peak
        if self.highlighted_peak_label != None:
            self.removeItem(self.highlighted_peak_label)
            self.highlighted_peak_label = None
        self.spec = spectrum
        self._mzs, self._ints = self.spec.get_peaks()
        self._autoscaleYAxis()
        # for annotation in ControllerWidget
        self.minMZ = np.amin(self._mzs)
        self.maxMZ = np.amax(self._mzs)

        self.redrawPlot()


    def redrawPlot(self):
        self.plot(clear=True)
        self._plot_tic()
        self._plot_peak_label()


    def _autoscaleYAxis(self):
        x_range = self.getAxis('bottom').range
        if x_range == [0, 1]:  # workaround for axis sometimes not being set TODO: check if this is resovled
            x_range = [np.amin(self._mzs), np.amax(self._mzs)]
        self.currMaxY = self._getMaxIntensityInRange(x_range)
        if self.currMaxY:
            self.setYRange(0, self.currMaxY, update=False)


    def _getMaxIntensityInRange(self, xrange):
        left = np.searchsorted(self._mzs, xrange[0], side='left')
        right = np.searchsorted(self._mzs, xrange[1], side='right')
        return np.amax(self._ints[left:right], initial=1)

    def _plot_tic(self):
        plotgraph = pg.PlotDataItem(self._mzs,self._ints)
        self.addItem(plotgraph)

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



    # TODO:
    # 1) search for the labels without intersections.
    # 2) use a prioritized function remove the lesser prioritized labels (only maxima remain)

    def _plot_peak_label(self):
        # alternative finding peak with scipy
        peakIndex = find_peaks(self._ints, distance=100)[0]

        # alternative with finding the local maxima (slower)
        #peakIndex = self._find_Peak()


        for i in peakIndex:
            self.peak_labels = pg.TextItem(text='{0:.3f}'.format(self._mzs[i]), color=(100, 100, 100), anchor=(0.5, 1))
            self.peak_labels.setPos(self._mzs[i], self._ints[i])
            self.addItem(self.peak_labels, ignoreBounds=True)  # ignore bounds to prevent rescaling of axis if the text item touches the border



    def _redrawPeaks(self):
        # TODO: clear the previous annotations for every zoom
        self._plot_peak_label()



    def _onMouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.sceneBoundingRect().contains(pos):
            mouse_point = self.getViewBox().mapSceneToView(pos)
            pixel_width = self.getViewBox().viewPixelSize()[0]
            left = np.searchsorted(self._mzs, mouse_point.x() - 4.0 * pixel_width, side='left')
            right = np.searchsorted(self._mzs, mouse_point.x() + 4.0 * pixel_width, side='right')
            if (left == right):  # none found -> remove text
                if self.highlighted_peak_label != None:
                    self.highlighted_peak_label.setText("")
                return
            # get point in range with minimum squared distance
            dx = np.square(np.subtract(self._mzs[left:right], mouse_point.x()))
            dy = np.square(np.subtract(self._ints[left:right], mouse_point.y()))
            idx_max_int_in_range = np.argmin(np.add(dx, dy))
            x = self._mzs[left + idx_max_int_in_range]
            y = self._ints[left + idx_max_int_in_range]
            if self.highlighted_peak_label == None:
                self.highlighted_peak_label = pg.TextItem(text='{0:.3f}'.format(x), color=(100, 100, 100),
                                                          anchor=(0.5, 1))
                self.addItem(self.highlighted_peak_label,
                             ignoreBounds=True)  # ignore bounds to prevent rescaling of axis if the text item touches the border
            self.highlighted_peak_label.setText('{0:.3f}'.format(x))
            self.highlighted_peak_label.setPos(x, y)
        else:
            # mouse moved out of visible area: remove highlighting item
            if self.highlighted_peak_label != None:
                self.highlighted_peak_label.setText("")