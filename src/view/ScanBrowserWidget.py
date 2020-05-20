import pyopenms
from PyQt5.QtCore import (
    Qt,
)
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QSplitter,
)
from ScanTableWidget import ScanTableWidget

from src.view.SpectrumWidget import SpectrumWidget


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
        # set new spectrum and redraw
        self.spectrum_widget.setSpectrum(self.scan_widget.curr_spec)
        if self.isAnnoOn:  # update annotation list
            self.updateController()
        self.spectrum_widget.redrawPlot()

    def updateController(self):
        # for overrriding
        return
