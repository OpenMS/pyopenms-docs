import sys

from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np

pg.setConfigOption('background', 'w') # white background
pg.setConfigOption('foreground', 'k') # black peaks


class ErrorWidget(PlotWidget):
    def __init__(self,  *args):
        PlotWidget.__init__(self)

        self.setLimits(xMin=0)
        self.setLabel('bottom', 'retention time')
        self.setLabel('left', 'intensity')
        self._retention_time = np.array([])
        self._intensity = np.array([])
        self._brushColor = ""
        self.color_lib = {}

    def setMassErrors(self, rt, intensity, colors):
        self._retention_time = rt
        self._intensity = intensity
        self.color_lib = colors
        self._redraw()

    def _redraw(self):
        self.plot(clear=True)
        self._plotMassErrors()

    def _plotMassErrors(self):
        scattergraph = pg.ScatterPlotItem(x=self._retention_time, y=self._intensity, brush=self._setBrushColor())
        self.addItem(scattergraph)

    def setColor(self, newColor):
        self._brushColor = newColor
        self._redraw()

    def _setBrushColor(self):
        if self._brushColor != "" and self.color_lib != {}:
            return self.color_lib[self._brushColor]
        else:
            return None


