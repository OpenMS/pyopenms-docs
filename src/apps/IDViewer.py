import os
import sys
from collections import namedtuple

import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QDesktopWidget,
    QAction,
    QFileDialog,
)

sys.path.insert(0, "../view")
from ControllerWidget import ControllerWidget

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


class App(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(1000, 1000)  # window size
        self.initUI()

    def initUI(self):
        self.setWindowTitle("pyOpenMS ID Viewer")
        self.center()

        # layout
        self.setMainMenu()
        self.centerWidget = QWidget(self)
        self.setCentralWidget(self.centerWidget)
        self.windowLay = QVBoxLayout(self.centerWidget)

        # default widget
        self.setWidgets()

    def setWidgets(self):
        if self.windowLay.count() > 0:
            self.clearLayout(self.windowLay)
        self.widgets = ControllerWidget(self)
        self.windowLay.addWidget(self.widgets)

    def setMainMenu(self):
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)

        self.titleMenu = mainMenu.addMenu("PyOpenMS")
        self.fileMenu = mainMenu.addMenu("File")
        # helpMenu = mainMenu.addMenu('Help')
        self.toolMenu = mainMenu.addMenu("Tools")

        self.setTitleMenu()
        self.setFileMenu()
        self.setToolMenu()

    def setTitleMenu(self):
        self.setExitButton()

    def setFileMenu(self):
        # open mzml file
        mzmlOpenAct = QAction("Open file", self)
        mzmlOpenAct.setShortcut("Ctrl+O")
        mzmlOpenAct.setStatusTip("Open new file")
        mzmlOpenAct.triggered.connect(self.openFileDialog)
        self.fileMenu.addAction(mzmlOpenAct)

    def setToolMenu(self):
        # for overriding
        return

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File ", "", "idXML Files (*.idXML)"
        )
        if fileName:
            print("opening...", fileName)
            self.setWidgets()
            self.widgets.loadFileMzML(os.path.splitext(fileName)[0] + ".mzML")
            self.widgets.loadFileIdXML(fileName)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setExitButton(self):
        exitButton = QAction("Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(self.close)
        self.titleMenu.addAction(exitButton)

    def closeEvent(self, event):
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
