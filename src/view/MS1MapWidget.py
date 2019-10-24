import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QAction

import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np

import time

MODULE_PATH = "/media/sachsenb/Samsung_T5/OpenMS/pyOpenMS/pyopenms/__init__.py"
MODULE_NAME = "pyopenms"
import importlib
import sys
spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
print(spec)
pyopenms = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = pyopenms
spec.loader.exec_module(pyopenms)

#import pyopenms

class MS1MapWidget(PlotWidget):

    def __init__(self, parent=None, dpi=100):
        PlotWidget.__init__(self)
        self.setLabel('bottom', 'm/z')
        self.setLabel('left', 'RT')

    def setSpectra(self, msexperiment):
        msexperiment.updateRanges()

        # resolution: mz_res Da in m/z, rt_res seconds in RT dimension 
        mz_res = 1.0 
        rt_res = 1.0

        # size of image
        cols = 1.0/mz_res * msexperiment.getMaxMZ()
        rows = 1.0/rt_res * msexperiment.getMaxRT()

        # create regular spaced data to turn spectra into an image
        max_intensity = msexperiment.getMaxInt()

        ## Set a custom color map
        pos = np.array([0., 0.01, 0.05, 0.1, 1.])
        color = np.array([(255,255,255,0), (255,255,0,255), (255, 0, 0, 255), (0, 0, 255, 255), (0, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        img = pg.ImageItem(autoDownsample=True)
        self.addItem(img)

        img.setLookupTable(cmap.getLookupTable(0.0, 1.0, 256))
        print(dir(msexperiment.getGriddedData(200, 200,0.0, 200.0, 0.0, 3000.0)))
        img.setImage(msexperiment.getGriddedData(200, 200,0.0, 200.0, 0.0, 3000.0).get_matrix())

