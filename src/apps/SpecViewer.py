import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, \
        QHBoxLayout, QWidget, QDesktopWidget, \
        QAction, QFileDialog, QTableView, QSplitter, \
        QMenu, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal, QItemSelectionModel, QSortFilterProxyModel, QSignalMapper, QPoint, QRegExp

import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np
from collections import namedtuple

import pyopenms

sys.path.insert(0, '../view')
from SpectrumWidget import *
from ScanTableWidget import ScanTableWidget, ScanTableModel

# structure for annotation (here for reference)
PeakAnnoStruct = namedtuple('PeakAnnoStruct', "mz intensity text_label \
                            symbol symbol_color")
LadderAnnoStruct = namedtuple('LadderAnnoStruct', "mz_list \
                            text_label_list color")

pg.setConfigOption('background', 'w') # white background
pg.setConfigOption('foreground', 'k') # black peaks

class ScanBrowserWidget(QWidget):

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.mainlayout = QHBoxLayout(self)
        self.isAnnoOn = False
    
    def clearLayout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

    def loadFile(self, file_path):        
        self.isAnnoOn = False
        self.msexperimentWidget = QSplitter(Qt.Vertical)

        # data processing
        scans = self.readMS(file_path)
        
        # set Widgets
        self.spectrum_widget = SpectrumWidget()
        self.scan_widget = ScanTableWidget(scans)
        self.scan_widget.scanClicked.connect(self.redrawPlot)
        self.msexperimentWidget.addWidget(self.spectrum_widget)
        self.msexperimentWidget.addWidget(self.scan_widget)
        self.mainlayout.addWidget(self.msexperimentWidget)

        # default : first row selected.
        self.scan_widget.table_view.selectRow(0) 

    def readMS(self, file_path):
        # Later: process other types of file
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load(file_path, exp)
        return exp

    def redrawPlot(self):
        #set new spectrum and redraw
        self.spectrum_widget.setSpectrum(self.scan_widget.curr_spec)
        if self.isAnnoOn: # update annotation list
            self.updateController()
        self.spectrum_widget.redrawPlot()

    def updateController(self):
        # for overrriding
        return
        

class App(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(1000, 700) # window size
        self.initUI()

    def initUI(self):
        self.setWindowTitle('pyOpenMSViewer')
        # self.center()
        
        # layout
        self.setMainMenu()
        self.centerWidget =  QWidget(self)
        self.setCentralWidget(self.centerWidget)
        self.windowLay = QVBoxLayout(self.centerWidget)
        
        # default widget <- per spectrum
        self.setScanBrowserWidget()
        
    def setScanBrowserWidget(self):
        if self.windowLay.count() > 0 :
            self.clearLayout(self.windowLay)
        self.scanbrowser = ScanBrowserWidget(self)
        self.windowLay.addWidget(self.scanbrowser)

    def setMainMenu(self):
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        
        self.titleMenu = mainMenu.addMenu('PyOpenMS')
        self.fileMenu = mainMenu.addMenu('File')
        # helpMenu = mainMenu.addMenu('Help')
        self.toolMenu = mainMenu.addMenu('Tools')
        
        self.setTitleMenu()
        self.setFileMenu()
        self.setToolMenu()
        
    def setTitleMenu(self):
        self.setExitButton()
        
    def setFileMenu(self):
        # open mzml file
        mzmlOpenAct = QAction('Open file', self)
        mzmlOpenAct.setShortcut('Ctrl+O')
        mzmlOpenAct.setStatusTip('Open new file')
        mzmlOpenAct.triggered.connect(self.openFileDialog)
        self.fileMenu.addAction(mzmlOpenAct)
        
    def setToolMenu(self):
        # for overriding
        return
    
    def clearLayout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                "Open File ", "", "mzML Files (*.mzML)")
        if fileName:
            print('opening...', fileName)
            self.setScanBrowserWidget()
            self.scanbrowser.loadFile(fileName)

    def center(self):        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()  
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def setExitButton(self):
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
