from collections import namedtuple

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from pyqtgraph import PlotWidget

# structure for annotation (here for reference)
PeakAnnoStruct = namedtuple(
    "PeakAnnoStruct",
    "mz intensity text_label \
                            symbol symbol_color",
)
LadderAnnoStruct = namedtuple(
    "LadderAnnoStruct",
    "mz_list \
                            text_label_list color",
)

pg.setConfigOption("background", "w")  # white background
pg.setConfigOption("foreground", "k")  # black peaks


class SpectrumWidget(PlotWidget):
    def __init__(self, parent=None, dpi=100):
        PlotWidget.__init__(self)
        self.setLimits(yMin=0, xMin=0)
        self.setMouseEnabled(y=False)
        self.setLabel("bottom", "m/z")
        self.setLabel("left", "intensity")
        self.highlighted_peak_label = None
        self.peak_annotations = None
        self.ladder_annotations = None
        # numpy arrays for fast look-up
        self._mzs = np.array([])
        self._ints = np.array([])
        self.getViewBox().sigXRangeChanged.connect(self._autoscaleYAxis)
        self.getViewBox().sigRangeChangedManually.connect(
            self.redrawLadderAnnotations
        )  # redraw anno
        self.proxy = pg.SignalProxy(
            self.scene().sigMouseMoved, rateLimit=60, slot=self._onMouseMoved
        )

    def setSpectrum(
            self, spectrum, zoomToFullRange=False
    ):  # add a default value for displaying all peaks
        self.plot(clear=True)
        self.zoomToFullRange = zoomToFullRange  # relevant in redrawPlot()
        # delete old highlighte "hover" peak
        """se_comment: changed != to is not"""
        if self.highlighted_peak_label is not None:
            self.removeItem(self.highlighted_peak_label)
            self.highlighted_peak_label = None
        self.spec = spectrum
        self._mzs, self._ints = self.spec.get_peaks()
        self._autoscaleYAxis()
        # for annotation in ControllerWidget
        self.minMZ = np.amin(self._mzs)
        self.maxMZ = np.amax(self._mzs)
        self.redrawPlot()

    def setPeakAnnotations(self, p_annotations):
        self.peak_annotation_list = p_annotations

    def setLadderAnnotations(self, ladder_visible=[]):
        self._ladder_visible = ladder_visible  # LadderAnnoStruct

    def clearLadderAnnotation(self, ladder_key_to_clear):
        try:
            if ladder_key_to_clear in self._ladder_anno_lines.keys():
                self._clear_ladder_item(ladder_key_to_clear)
        except (AttributeError, NameError):
            return

    def redrawPlot(self):
        self.plot(clear=True)
        if self.zoomToFullRange:
            self.setXRange(self.minMZ, self.maxMZ)
        self._plot_spectrum()
        self._clear_annotations()
        self._plot_peak_annotations()
        self._plot_ladder_annotations()

    def redrawLadderAnnotations(self):
        self._plot_ladder_annotations()

    def _autoscaleYAxis(self):
        x_range = self.getAxis("bottom").range
        if x_range == [
            0,
            1,
        ]:  # workaround for axis sometimes not being set
            # TODO: check if this is resovled
            x_range = [np.amin(self._mzs), np.amax(self._mzs)]
        self.currMaxY = self._getMaxIntensityInRange(x_range)
        if self.currMaxY:
            self.setYRange(0, self.currMaxY, update=False)

    def _plot_peak_annotations(self):
        try:
            self.peak_annotation_list
        except (AttributeError, NameError):
            return

        if self.peak_annotation_list is not None:
            for item in self.peak_annotation_list:  # item : PeakAnnoStruct
                self.plot(
                    [item.mz],
                    [item.intensity],
                    symbol=item.symbol,
                    symbolBrush=pg.mkBrush(item.symbol_color),
                    symbolSize=14,
                )
                if item.text_label:
                    label = pg.TextItem(
                        text=item.text_label, color=item.symbol_color, anchor=(
                            0.5, 1)
                    )
                    self.addItem(label)
                    label.setPos(item.mz, item.intensity)

    def _getMaxIntensityInRange(self, xrange):
        left = np.searchsorted(self._mzs, xrange[0], side="left")
        right = np.searchsorted(self._mzs, xrange[1], side="right")
        return np.amax(self._ints[left:right], initial=1)

    def _plot_spectrum(self):
        bargraph = pg.BarGraphItem(x=self._mzs, height=self._ints, width=0)
        self.addItem(bargraph)

    def _plot_ladder_annotations(self):
        try:
            self._ladder_visible
        except (AttributeError, NameError):
            return
        try:
            self.currMaxY
        except (AttributeError, NameError):
            self.currMaxY = self._getMaxIntensityInRange(
                self.getAxis("bottom").range)

        xlimit = [self._mzs[0], self._mzs[-1]]
        for ladder_key, lastruct in self._ladder_visible.items():
            if ladder_key in self._ladder_anno_lines.keys():  # update
                self._ladder_anno_lines[ladder_key][0].setData(
                    [xlimit[0], xlimit[1]], [self.currMaxY, self.currMaxY]
                )  # horizontal line
                cntr = 0
                for x in lastruct.mz_list:
                    self._ladder_anno_lines[ladder_key][cntr + 1].setData(
                        [x, x], [0, self.currMaxY]
                    )
                    self._ladder_anno_labels[ladder_key][cntr].setPos(
                        x, self.currMaxY
                    )  # horizon line doesn't have label
                    cntr += 1
            else:  # plot
                pen = pg.mkPen(lastruct.color, width=2, style=Qt.DotLine)
                self._ladder_anno_lines[ladder_key] = []
                self._ladder_anno_labels[ladder_key] = []

                self._ladder_anno_lines[ladder_key].append(
                    # horizon line. index 0
                    self.plot(
                        [xlimit[0], xlimit[1]], [
                            self.currMaxY, self.currMaxY], pen=pen
                    )
                )
                """se_comment: hard-refactor to comply to pep8"""
                z = zip(lastruct.mz_list, lastruct.text_label_list)
                for x, txt_label in z:
                    self._ladder_anno_lines[ladder_key].append(
                        self.plot([x, x], [0, self.currMaxY], pen=pen)
                    )
                    label = pg.TextItem(
                        text=txt_label, color=lastruct.color, anchor=(1, -1)
                    )
                    label.setPos(x, self.currMaxY)
                    label.setParentItem(
                        self._ladder_anno_lines[ladder_key][-1])
                    self._ladder_anno_labels[ladder_key].append(label)

    def _clear_annotations(self):
        self._ladder_visible = dict()
        self._ladder_anno_lines = dict()
        self._ladder_anno_labels = dict()

    def _clear_peak_annotations(self):
        self.peak_annotation_list = None

    def _clear_ladder_item(self, key):
        for anno in self._ladder_anno_lines[key]:
            anno.clear()
        for pos in self._ladder_anno_labels[key]:
            pos.setPos(0, 0)
        del self._ladder_anno_lines[key]
        del self._ladder_anno_labels[key]

    def _onMouseMoved(self, evt):
        pos = evt[0]  # using signal proxy
        # turns original arguments into a tuple
        if self.sceneBoundingRect().contains(pos):
            mouse_point = self.getViewBox().mapSceneToView(pos)
            pixel_width = self.getViewBox().viewPixelSize()[0]
            left = np.searchsorted(
                self._mzs, mouse_point.x() - 4.0 * pixel_width, side="left"
            )
            right = np.searchsorted(
                self._mzs, mouse_point.x() + 4.0 * pixel_width, side="right"
            )
            if left == right:  # none found -> remove text
                """se_comment: changed != to is not"""
                if self.highlighted_peak_label is not None:
                    self.highlighted_peak_label.setText("")
                return
            # get point in range with minimum squared distance
            dx = np.square(np.subtract(self._mzs[left:right], mouse_point.x()))
            dy = np.square(np.subtract(
                self._ints[left:right], mouse_point.y()))
            idx_max_int_in_range = np.argmin(np.add(dx, dy))
            x = self._mzs[left + idx_max_int_in_range]
            y = self._ints[left + idx_max_int_in_range]
            """se_comment: changed == to is"""
            if self.highlighted_peak_label is None:
                self.highlighted_peak_label = pg.TextItem(
                    text="{0:.3f}".format(x),
                    color=(100, 100, 100),
                    anchor=(0.5, 1.5)
                )
                self.addItem(
                    self.highlighted_peak_label, ignoreBounds=True
                )  # ignore bounds to prevent rescaling of axis
                # if the text item touches the border
            self.highlighted_peak_label.setText("{0:.3f}".format(x))
            self.highlighted_peak_label.setPos(x, y)
        else:
            # mouse moved out of visible area: remove highlighting item
            """se_comment: changed != to is not"""
            if self.highlighted_peak_label is not None:
                self.highlighted_peak_label.setText("")
