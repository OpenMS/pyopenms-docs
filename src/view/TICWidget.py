import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, \
    QHBoxLayout, QWidget, QDesktopWidget, \
    QAction, QFileDialog, QTableView, QSplitter, \
    QMenu, QAbstractItemView, QShortcut
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal, QItemSelectionModel, QSortFilterProxyModel, QSignalMapper, \
    QPoint, QRegExp, QRectF

import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np


import pyopenms

pg.setConfigOption('background', 'w')  # white background
pg.setConfigOption('foreground', 'k')  # black peaks


class TICWidget(PlotWidget):
    sigRTClicked = QtCore.pyqtSignal(float, name='sigRTClicked')
    #sigRTSelectionChanged = QtCore.pyqtSignal(float, float, name='sigRTSelectionChanged')

    def __init__(self, parent=None, dpi=100):
        PlotWidget.__init__(self)
        self.setLimits(yMin=0, xMin=0)
        self.setMouseEnabled(y=False)
        self.setLabel('bottom', 'RT (min)')
        self.setLabel('left', 'relative intensity (%)')
        self._peak_labels = {}
        # numpy arrays for fast look-up
        self._rts = np.array([])
        self._ints = np.array([])
        self._peak_indices = np.array([])
        self._currentIntensitiesInRange = np.array([])
        self._region = None
        self.getViewBox().sigXRangeChanged.connect(self._autoscaleYAxis)

        # define signal
        self.scene().sigMouseClicked.connect(self._clicked) # emits rt_clicked

        # to init the region
        self.shortcut1 = QShortcut(QKeySequence("Ctrl+r"), self)
        self.shortcut1.activated.connect(self._rgn_shortcut)

        # shortcut for mouseDrag
        self.shortcut2 = QShortcut(QKeySequence("right"), self)
        self.shortcut2.activated.connect(self._rgnDrag_shortcut)


    def setTIC(self, chromatogram):
        # delete old labels
        if self._peak_labels != {}:
            self._clear_labels()
            self._peak_labels = {}
        self._chrom = chromatogram
        self._rts, self._ints = self._chrom.get_peaks()
        self._rts_in_min()
        self._relative_ints()
        self._peak_indices = self._find_Peak()
        self._autoscaleYAxis()
        self._redrawPlot()


    def _rts_in_min(self):
        self._rts = np.array([x/60 for x in self._rts])

    def _relative_ints(self):
        maxInt = np.amax(self._ints)
        self._ints = np.array([((x/maxInt)*100) for x in self._ints])

    def _redrawPlot(self):
        self.plot(clear=True)
        self._plot_tic()
        self._plot_peak_label()

    def _autoscaleYAxis(self):
        x_range = self.getAxis('bottom').range
        if x_range == [0, 1]:  # workaround for axis sometimes not being set
            x_range = [np.amin(self._rts), np.amax(self._rts)]
        self.currMaxY = self._getMaxIntensityInRange(x_range)
        if self.currMaxY:
            self.setYRange(0, self.currMaxY, update=False)
            self._redrawLabels()

    def _getMaxIntensityInRange(self, xrange):
        left = np.searchsorted(self._rts, xrange[0], side='left')
        right = np.searchsorted(self._rts, xrange[1], side='right')
        self._currentIntensitiesInRange = self._ints[left:right]
        return np.amax(self._ints[left:right], initial=1)

    def _plot_tic(self):
        plotgraph = pg.PlotDataItem(self._rts, self._ints)
        self.addItem(plotgraph)

    def _find_Peak(self):
        data = self._ints
        maxIndex = np.zeros_like(data)
        peakValue = -np.inf
        for i in range(0, len(data), 1):
            if peakValue < data[i]:
                peakValue = data[i]
                for j in range(i, len(data)):
                    if peakValue < data[j]:
                        break
                    elif peakValue == data[j]:
                        continue
                    elif peakValue > data[j]:
                        peakIndex = i + np.floor(abs(i - j) / 2)
                        maxIndex[peakIndex.astype(int)] = 1
                        i = j
                        break
            peakValue = data[i]
        maxIndex = np.where(maxIndex)[0]

        # sort indices of high points from largest intensity to smallest
        maxIndex = sorted(maxIndex, key=lambda x: data[x], reverse=True)

        return maxIndex

    def _add_label(self, label_id, label_text, pos_x, pos_y):
        label = pg.TextItem(anchor=(0.5, 1))
        label.setText(text='{0:.2f}'.format(label_text), color=(100, 100, 100))
        label.setPos(pos_x, pos_y)
        self._peak_labels[label_id] = {'label': label}
        self.addItem(label, ignoreBounds=True)

        if self._label_clashes(label_id):
            self._remove_label(label_id)

    def _remove_label(self, label_id):
        self.removeItem(self._peak_labels[label_id]['label'])
        del self._peak_labels[label_id]


    def _clear_labels(self):
        for label_id in self._peak_labels.keys():
            self.removeItem(self._peak_labels[label_id]['label'])
        self._peak_labels = {}

    def _label_clashes(self, label_id):
        new_label = label_id
        clash = False

        # scaling the distance with the correct pixel size
        pixel_width = self.getViewBox().viewPixelSize()[0]
        limit_distance = 20.0 * pixel_width

        if self._peak_labels == {}:
            return False

        for exist_label in list(self._peak_labels):
            if exist_label != new_label:
                new_label_rect = self._peak_labels[new_label]["label"].mapRectToDevice(
                    self._peak_labels[new_label]["label"].boundingRect())
                exist_label_rect = self._peak_labels[exist_label]["label"].mapRectToDevice(
                    self._peak_labels[exist_label]["label"].boundingRect())

                if not new_label_rect.intersects(exist_label_rect):
                    exist_label_X = self._peak_labels[exist_label]['label'].x()
                    new_label_X = self._peak_labels[new_label]['label'].x()

                    distance = abs(new_label_X - exist_label_X)

                    if distance < limit_distance:
                        clash = True
                        break
                    else:
                        clash = False

                elif new_label_rect.intersects(exist_label_rect):
                    clash = True
                    break
            else:
                if len(self._peak_labels) == 1 and exist_label == new_label:
                    clash = False
        return clash

    def _plot_peak_label(self):
        if self._peak_labels == {}:
            for index in self._peak_indices:
                if self._ints[index] in self._currentIntensitiesInRange:
                    self._add_label(index, self._rts[index], self._rts[index], self._ints[index])

    def _redrawLabels(self):
        self._clear_labels()
        self._plot_peak_label()

    def _clicked(self, event):
        pos = event.scenePos()
        if self.sceneBoundingRect().contains(pos):
            mouse_point = self.getViewBox().mapSceneToView(pos)
            larger_idx = np.searchsorted(self._rts, mouse_point.x(), side='left')
            smaller_idx = 0
            if larger_idx > 0:
                smaller_idx = larger_idx - 1
            if abs(self._rts[larger_idx] - mouse_point.x()) < abs(self._rts[smaller_idx] - mouse_point.x()):
                closest_datapoint_idx = larger_idx
            else:
                closest_datapoint_idx = smaller_idx
            self.sigRTClicked.emit(self._rts[closest_datapoint_idx]) # notify observers


    def mouseDoubleClickEvent(self, event):
        super(TICWidget, self).mouseDoubleClickEvent(event)
        rgn_start = self.getViewBox().mapSceneToView(event.pos()).x()

        if self._region == None:
            region = pg.LinearRegionItem()
            region.setRegion((rgn_start, rgn_start))
            self._region = region
            self.addItem(region, ignoreBounds=True)

        # delete the region when hovering over the region per doubleClk
        self._delete_region()

    def _delete_region(self):
        if self._region.mouseHovering:
            self.removeItem(self._region)
            self._region = None

    def _rgn_shortcut(self):
        # click region, with following shortcut -> create region
        rgn_start = self.getViewBox().mapSceneToView(self.lastMousePos)

        if self._region == None:
            region = pg.LinearRegionItem()
            region.setRegion((rgn_start, rgn_start))
            self._region = region
            self.addItem(region, ignoreBounds=True)

    def _rgnDrag_shortcut(self):
        print('work on it')




