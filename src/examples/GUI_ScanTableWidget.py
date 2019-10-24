import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QAction

import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np

import time
import pyopenms

sys.path.insert(0, '../view')
from ScanTableWidget import *

pg.setConfigOption('background', 'w') # white background
pg.setConfigOption('foreground', 'k') # black peaks

class App(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(800, 600) 
        self._initUI()

    def _initUI(self):
        self.setWindowTitle('MS1MapWidget')
        self.centerWidget = QWidget(self)
        self.setCentralWidget(self.centerWidget)
        self.layout = QVBoxLayout(self.centerWidget)

        # load spectra and display first spectrum
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load("../data/190509_Ova_native_25ngul_R.mzML", exp)
        self.widget = ScanTableWidget(exp)
        self.layout.addWidget(self.widget)
        self._setMainMenu()
        self._setExitButton()

    def _setMainMenu(self):
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        self.titleMenu = mainMenu.addMenu('PyOpenMS')

    def _setExitButton(self):
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        self.titleMenu.addAction(exitButton)
        
    def closeEvent(self, event):
        self.close
        sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
