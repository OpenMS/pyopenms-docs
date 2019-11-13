import sys

from PyQt5.QtCore import QPointF
import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np

pg.setConfigOption('background', 'w') # white background
pg.setConfigOption('foreground', 'k') # black peaks


class ErrorWidget(PlotWidget):
    def __init__(self,  *args):
        PlotWidget.__init__(self)

        self.setLimits(xMin=0)
        self.setLabel('bottom', 'RT')
        self.setLabel('left', 'Intensity')
        self._retention_time = np.array([])
        self._intensity = np.array([])
        self._brushColor = None
        self.color_lib = np.array([])
        self.getViewBox().sigXRangeChanged.connect(self._autoscaleYAxis)

    def setMassErrors(self, rt, intensity, colors):
        self._retention_time = rt
        self._intensity = intensity
        self.color_lib = colors
        self._redraw()

    def _redraw(self):
        self.plot(clear=True)
        self._autoscaleYAxis()
        self._plotHorizontalLine()
        self._plotMassErrors()

    def _plotMassErrors(self):
        if self._retention_time.size == self._intensity.size:
            scattergraph = pg.ScatterPlotItem()
            points = []
            for i in range(0, self._intensity.size):
                points.append({'pos': (self._retention_time[i], self._intensity[i]), 'brush': pg.mkBrush(self.color_lib[i])})
                scattergraph.addPoints(points)
                self.addItem(scattergraph)


    def _plotHorizontalLine(self):
        horizontalLine = pg.InfiniteLine(pos=QPointF(0.0, 0.0), angle=0, pen=pg.mkColor('k'))
        self.addItem(horizontalLine)

    def _autoscaleYAxis(self):
        x_range = self.getAxis('bottom').range
        if x_range == [0, 1]:  # workaround for axis sometimes not being set
            x_range = [np.amin(self._retention_time), np.amax(self._retention_time)]
        self.currMaxY = self._getMaxIntensityInRange(x_range)
        if self.currMaxY:
            self.setYRange(self.currMaxY * (-1), self.currMaxY, update=False)

    def _getMaxIntensityInRange(self, xrange):
        left = np.searchsorted(self._retention_time, xrange[0], side='left')
        right = np.searchsorted(self._retention_time, xrange[1], side='right')
        return np.amax(abs(self._intensity[left:right]), initial=1)




