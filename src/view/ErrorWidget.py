import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QPointF
from pyqtgraph import PlotWidget

pg.setConfigOption("background", "w")  # white background
pg.setConfigOption("foreground", "k")  # black peaks


class ErrorWidget(PlotWidget):
    """
    Used to plot a error plot to display the derivation
        between exact mass and theoretical mass.
    """

    def __init__(self, *args):
        PlotWidget.__init__(self)

        self.setLimits(xMin=0)
        self.setLabel("bottom", "m/z")
        self.setLabel("left", "ppm")
        self._mzs = np.array([])
        self._ppm = np.array([])
        self._color_lib = np.array([])
        self.getViewBox().sigXRangeChanged.connect(self._autoscaleYAxis)
        self.setMouseEnabled(x=True, y=False)

    def setMassErrors(self, mz, ppm, colors):
        """
        Used for creating new error plot
            with the m/z of the peptides fragments.
        :param mz: An numpy array of m/z
            (mass divided by charge number) of the ions
            (starting with xyz or abc)
        :param ppm: An numpy array of random numbers,
            ppm needs to be calculated
        :param colors: An numpy array of colors consisting of red and blue
            (representing prefix -> blue and suffix -> red ions)

        """
        self._mzs = mz
        self._ppm = ppm
        self._color_lib = colors
        self.redraw()

    def redraw(self):
        self.plot(clear=True)
        self.setXRange(np.amin(self._mzs), np.amax(self._mzs))
        self._autoscaleYAxis()
        self._plotHorizontalLine()
        self._plotMassErrors()

    def _plotMassErrors(self):
        scattergraph = pg.ScatterPlotItem()
        points = []
        for i in range(0, self._ppm.size):
            points.append(
                {
                    "pos": (self._mzs[i], self._ppm[i]),
                    "brush": pg.mkBrush(self._color_lib[i]),
                }
            )
            scattergraph.addPoints(points)
            self.addItem(scattergraph)

    def _plotHorizontalLine(self):
        horizontalLine = pg.InfiniteLine(
            pos=QPointF(0.0, 0.0), angle=0, pen=pg.mkColor("k")
        )
        self.addItem(horizontalLine)

    def _autoscaleYAxis(self):
        x_range = self.getAxis("bottom").range
        if x_range == [0, 1]:  # workaround for axis sometimes not being set
            x_range = [np.amin(self._mzs), np.amax(self._mzs)]
        self.currMaxY = self._getMaxMassErrorInRange(x_range)
        if self.currMaxY:
            self.setYRange(self.currMaxY * (-1), self.currMaxY, update=False)

    def _getMaxMassErrorInRange(self, xrange):
        left = np.searchsorted(self._mzs, xrange[0], side="left")
        right = np.searchsorted(self._mzs, xrange[1], side="right")
        return np.amax(abs(self._ppm[left:right]), initial=1)
