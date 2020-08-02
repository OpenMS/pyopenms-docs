import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, \
        QHBoxLayout, QWidget, QDesktopWidget, \
        QAction, QFileDialog, QTableView, QSplitter, \
        QMenu, QAbstractItemView, QPushButton
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal, \
     QItemSelectionModel, QSortFilterProxyModel, QSignalMapper, QPoint, QRegExp

import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np
from collections import namedtuple

import pyopenms

sys.path.insert(0, '../view')
from ScanBrowserWidget import ScanBrowserWidget

# structure for annotation (here for reference)
PeakAnnoStruct = namedtuple('PeakAnnoStruct', "mz intensity text_label \
                            symbol symbol_color")
LadderAnnoStruct = namedtuple('LadderAnnoStruct', "mz_list \
                            text_label_list color")

pg.setConfigOption('background', 'w')  # white background
pg.setConfigOption('foreground', 'k')  # black peaks


class Specviewer(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(1000, 700)  # window size
        self.initUI()

    def initUI(self):
        self.setWindowTitle('pyOpenMSViewer')
        # self.center()

        self.centerWidget = QWidget(self)
        self.setCentralWidget(self.centerWidget)
        # main
        mainLayout = QVBoxLayout(self.centerWidget)

        # buttons
        buttons = QVBoxLayout()
        loadbtn = QPushButton('Load')
        loadbtn.setMaximumWidth(80)
        loadbtn.clicked.connect(self.openFileDialog)
        buttons.addWidget(loadbtn)

        mainLayout.addLayout(buttons)

        # graph
        self.windowLay = QVBoxLayout()
        mainLayout.addLayout(self.windowLay)

        # default widget <- per spectrum
        self.setScanBrowserWidget()

    def setScanBrowserWidget(self):
        if self.windowLay.count() > 0:
            self.clearLayout(self.windowLay)
        self.scanbrowser = ScanBrowserWidget(self)
        self.windowLay.addWidget(self.scanbrowser)

    # def setMainMenu(self):
    #    mainMenu = self.menuBar()
    #    mainMenu.setNativeMenuBar(False)
    #
    #    self.titleMenu = mainMenu.addMenu('PyOpenMS')
    #    self.fileMenu = mainMenu.addMenu('File')
    #    # helpMenu = mainMenu.addMenu('Help')
    #    self.toolMenu = mainMenu.addMenu('Tools')
    #
    #    self.setTitleMenu()
    #    self.setFileMenu()
    #    self.setToolMenu()
    #
    # def setTitleMenu(self):
    #    self.setExitButton()
    #
    # def setFileMenu(self):
    #    # open mzml file
    #    mzmlOpenAct = QAction('Open file', self)
    #    mzmlOpenAct.setShortcut('Ctrl+O')
    #    mzmlOpenAct.setStatusTip('Open new file')
    #    mzmlOpenAct.triggered.connect(self.openFileDialog)
    #    self.fileMenu.addAction(mzmlOpenAct)
    #
    # def setToolMenu(self):
    #    # for overriding
    #    return

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def openFileDialog(self, fileName: str = ""):
        if not fileName:
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
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
