from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtCore import pyqtSignal

import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np


pg.setConfigOption("background", "w")  # white background
pg.setConfigOption("foreground", "k")  # black peaks


class TICWidget(PlotWidget):
    """
    Used for creating a TIC plot with dynamic zooming to avoid label collisions.

    ===============================  =============================================================================
    **Signals:**
    sigRTClicked                     Emitted when the user has clicked on TIC plot and returns the clicked RT value.

    sigSeleRTRegionChangeFinished    Emitted while the user is double clicking on a region in TIC plot and creates a
                                     region by dragging a horizontal line. The signal returns the start and end
                                     RT values within the region.
    ===============================  =============================================================================
    """

    sigRTClicked = pyqtSignal(float, name="sigRTClicked")
    sigSeleRTRegionChangeFinished = pyqtSignal(
        float, float, name="sigRTRegionChangeFinished"
    )

    def __init__(self, parent=None, dpi=100):
        PlotWidget.__init__(self)
        self.setLimits(yMin=0, xMin=0)
        self.setMouseEnabled(y=False)
        self.setLabel("bottom", "RT (min)")
        self.setLabel("left", "relative intensity (%)")
        self._peak_labels = {}
        # numpy arrays for fast look-up
        self._rts = np.array([])
        self._ints = np.array([])
        self._peak_indices = np.array([])
        self._currentIntensitiesInRange = np.array([])
        self._region = None
        self.getViewBox().sigXRangeChanged.connect(self._autoscaleYAxis)

        self.scene().sigMouseClicked.connect(self._clicked)  # emits rt_clicked

        # shortcut to init region
        self.shortcut1 = QShortcut(QKeySequence("Ctrl+r"), self)
        self.shortcut1.activated.connect(self._rgn_shortcut)

    def setTIC(self, chromatogram):
        """
        Used to set new TIC and with given Information (rts, ints)

        :param chromatogram: data from the MSExperiment
        """
        if self._peak_labels != {}:
            self._clear_labels()
            self._peak_labels = {}
        self._chrom = chromatogram
        self._rts, self._ints = self._chrom.get_peaks()
        try:
            self._rts_in_min()
            self._relative_ints()
            self._peak_indices = self._find_Peak()
            self._autoscaleYAxis()
            self.redrawPlot()
        except ValueError:
            print("No TIC values in spectrum")

    def _rts_in_min(self):
        self._rts = np.array([x / 60 for x in self._rts])

    def _relative_ints(self):
        maxInt = np.amax(self._ints)
        self._ints = np.array([((x / maxInt) * 100) for x in self._ints])

    def redrawPlot(self):
        self.plot(clear=True)
        self._plot_tic()
        self._draw_peak_label()

    def _autoscaleYAxis(self):
        """
        Used to adjust y axis with the maximal y value from the current RT values. Also, redraws peak labels
        depending on the current displayed RT values.

        """
        x_range = self.getAxis("bottom").range
        if x_range == [0, 1]:  # workaround for axis sometimes not being set
            x_range = [np.amin(self._rts), np.amax(self._rts)]
        self.currMaxY = self._getMaxIntensityInRange(x_range)
        if self.currMaxY:
            self.setYRange(0, self.currMaxY, update=False)
            self._redrawLabels()

    def _getMaxIntensityInRange(self, xrange):
        """
        :param xrange: A list of [min, max] bounding RT values.
        :return: An float value representing the maximal intensity current x range.
        """
        left = np.searchsorted(self._rts, xrange[0], side="left")
        right = np.searchsorted(self._rts, xrange[1], side="right")
        self._currentIntensitiesInRange = self._ints[left:right]

        return np.amax(self._ints[left:right], initial=1)

    def _plot_tic(self):
        plotgraph = pg.PlotDataItem(self._rts, self._ints)
        self.addItem(plotgraph)

    def _find_Peak(self):
        """
        Calculates all indices from the intensity values to locate peaks. This function operates on the principle that
        it compares peak values against each other until it founds a maximal turning point.

        :return: A numpy array containing all peak indices, sorted descending (max first -> min last).
        """
        data = self._ints
        maxIndices = np.zeros_like(data)
        peakValue = -np.inf
        for indx in range(0, len(data), 1):
            if peakValue < data[indx]:
                peakValue = data[indx]
                for j in range(indx, len(data)):
                    if peakValue < data[j]:
                        break
                    elif peakValue == data[j]:
                        continue
                    elif peakValue > data[j]:
                        peakIndex = indx + np.floor(abs(indx - j) / 2)
                        # marking found index
                        maxIndices[peakIndex.astype(int)] = 1
                        indx = j
                        break
            peakValue = data[indx]
        maxIndices = np.where(maxIndices)[0]

        # sort indices of high points from largest intensity to smallest
        maxIndices = sorted(maxIndices, key=lambda x: data[x], reverse=True)

        return maxIndices

    def _add_label(self, label_id, label_text, pos_x, pos_y):
        label = pg.TextItem(anchor=(0.5, 1))
        label.setText(text="{0:.2f}".format(label_text), color=(0, 0, 0))
        label.setPos(pos_x, pos_y)
        self._peak_labels[label_id] = {"label": label}
        self.addItem(label, ignoreBounds=True)

        if self._label_clashes(label_id):
            self._remove_label(label_id)

    def _remove_label(self, label_id):
        self.removeItem(self._peak_labels[label_id]["label"])
        del self._peak_labels[label_id]

    def _clear_labels(self):
        for label_id in self._peak_labels.keys():
            self.removeItem(self._peak_labels[label_id]["label"])
        self._peak_labels = {}

    def _label_clashes(self, label_id):
        """
        Calculates possible clash of new added label to other existing labels. The clash is measured by the
        collision of the label boundingRects, which are representing displayed scene positions.

        :param label_id: Represents index of peak position in peak_indices.
        :return: A boolean indicating if there is a clash or not.
        """
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
                    self._peak_labels[new_label]["label"].boundingRect()
                )
                exist_label_rect = self._peak_labels[exist_label][
                    "label"
                ].mapRectToDevice(
                    self._peak_labels[exist_label]["label"].boundingRect()
                )

                if not new_label_rect.intersects(exist_label_rect):
                    exist_label_X = self._peak_labels[exist_label]["label"].x()
                    new_label_X = self._peak_labels[new_label]["label"].x()

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

    def _draw_peak_label(self):
        """
        Function draws peak labels, starting with the maximal peak to the minimal peak. In each addition possible
        label clashes will be calculated, if so then delete label.

        """
        if self._peak_labels == {}:
            for index in self._peak_indices:
                if self._ints[index] in self._currentIntensitiesInRange:
                    self._add_label(
                        index, self._rts[index], self._rts[index], self._ints[index]
                    )

    def _redrawLabels(self):
        self._clear_labels()
        self._draw_peak_label()

    def _clicked(self, event):
        try:
            pos = event.scenePos()
            if self.sceneBoundingRect().contains(pos):
                mouse_point = self.getViewBox().mapSceneToView(pos)
                closest_datapoint_idx = self._calculate_closest_datapoint(
                    mouse_point.x()
                )
                self.sigRTClicked.emit(
                    self._rts[closest_datapoint_idx]
                )  # notify observers

            # check the selected rt region and return the bounds
            if self._region is not None:
                self._region.sigRegionChangeFinished.connect(
                    self._rtRegionBounds)

        except ValueError:
            print("No TIC values to click on")

    def mouseDoubleClickEvent(self, event):
        super(TICWidget, self).mouseDoubleClickEvent(event)
        try:
            mouse_point = self.getViewBox().mapSceneToView(event.pos())
            closest_datapoint_idx = self._calculate_closest_datapoint(
                mouse_point.x())
            rgn_start = self._rts[closest_datapoint_idx]

            if self._region is None:
                region = pg.LinearRegionItem()
                region.setRegion((rgn_start, rgn_start))
                self._region = region
                self.addItem(region, ignoreBounds=True)

            # delete the region when hovering over the region per doubleClk
            self._delete_region()
        except ValueError:
            print("No TIC values to click on")

    def _calculate_closest_datapoint(self, point_x):
        """
        :param point_x: mouse clicked position
        :return: closest data point near a peak

        """
        larger_idx = np.searchsorted(self._rts, point_x, side="left")
        smaller_idx = 0
        if larger_idx >= self._rts.size:  # to avoid array out of bounds
            larger_idx -= 1
        if larger_idx > 0:
            smaller_idx = larger_idx - 1
        if abs(self._rts[larger_idx] - point_x) < abs(self._rts[smaller_idx] - point_x):
            closest_datapoint_idx = larger_idx

        else:
            closest_datapoint_idx = smaller_idx

        return closest_datapoint_idx

    def _rtRegionBounds(self):
        region_bounds = self._region.getRegion()
        start_rg = region_bounds[0]

        stop_rg_idx = self._calculate_closest_datapoint(region_bounds[1])
        stop_rg = self._rts[stop_rg_idx]

        # set the new region of interest
        self._region.setRegion((start_rg, stop_rg))

        self.sigSeleRTRegionChangeFinished.emit(
            start_rg, stop_rg)  # notify observers

    def _delete_region(self):
        if self._region.mouseHovering:
            self.removeItem(self._region)
            self._region = None

    def _rgn_shortcut(self):
        # click region, with following shortcut -> create region
        rgn_start = self.getViewBox().mapSceneToView(self.lastMousePos)

        if self._region is None:
            region = pg.LinearRegionItem()
            region.setRegion((rgn_start, rgn_start))
            self._region = region
            self.addItem(region, ignoreBounds=True)
