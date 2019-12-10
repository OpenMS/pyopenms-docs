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
        self.setLabel('bottom', 'm/z')
        self.setLabel('left', 'ppm')
        self._mz = np.array([])
        self._intensity = np.array([])
        self._brushColor = None
        self.color_lib = np.array([])
        self.setMouseEnabled(x=True, y=False)

    def setMassErrors(self, mz, intensity, colors):
        self._mz = mz
        self._intensity = intensity
        self.color_lib = colors
        self._redraw()

    def _redraw(self):
        self.plot(clear=True)
        self._plotHorizontalLine()
        self._plotMassErrors()

    def _plotMassErrors(self):
        if self._mz.size == self._intensity.size:
            scattergraph = pg.ScatterPlotItem()
            points = []
            for i in range(0, self._intensity.size):
                points.append({'pos': (self._mz[i], self._intensity[i]), 'brush': pg.mkBrush(self.color_lib[i])})
                scattergraph.addPoints(points)
                self.addItem(scattergraph)

    def _plotHorizontalLine(self):
        horizontalLine = pg.InfiniteLine(pos=QPointF(0.0, 0.0), angle=0, pen=pg.mkColor('k'))
        self.addItem(horizontalLine)
