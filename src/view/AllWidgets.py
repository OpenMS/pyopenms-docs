import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, \
    QHBoxLayout, QWidget, QDesktopWidget, \
    QAction, QFileDialog, QTableView, QSplitter, \
    QMenu, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal, QItemSelectionModel, QSortFilterProxyModel, QSignalMapper, \
    QPoint, QRegExp
from SpectrumWidget import *
from ScanTableWidget import ScanTableWidget, ScanTableModel
from SequenceIonsWidget import SequenceIonsWidget
from TICWidget import TICWidget
from ErrorWidget import ErrorWidget

import pyopenms

class AllWidgets(QWidget):

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.mainlayout = QHBoxLayout(self)
        self.isAnnoOn = False

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def loadFileMzML(self, file_path):
        self.isAnnoOn = False
        self.msexperimentWidget = QSplitter(Qt.Vertical)

        # data processing
        scans = self.readMS(file_path)

        # set Widgets
        self.spectrum_widget = SpectrumWidget()
        self.scan_widget = ScanTableWidget(scans)
        self.seqIons_widget = SequenceIonsWidget()
        self.error_widget = ErrorWidget()
        self.tic_widget = TICWidget()
        self.drawTic(scans)

        self.scan_widget.scanClicked.connect(self.redrawPlot)
        self.msexperimentWidget.addWidget(self.tic_widget)
        self.msexperimentWidget.addWidget(self.seqIons_widget)
        self.msexperimentWidget.addWidget(self.spectrum_widget)
        self.msexperimentWidget.addWidget(self.error_widget)
        self.msexperimentWidget.addWidget(self.scan_widget)
        self.mainlayout.addWidget(self.msexperimentWidget)

        # default : first row selected.
        self.scan_widget.table_view.selectRow(0)

    def loadFileIdXML(self, file_path):
        prot_ids = []; pep_ids = []
        pyopenms.IdXMLFile().load(file_path, prot_ids, pep_ids)
        # Iterate over PeptideIdentification
        for peptide_id in pep_ids:
            # Peptide identification values
            print ("Peptide ID m/z:", peptide_id.getMZ())
            print ("Peptide ID rt:", peptide_id.getRT())
            print ("Peptide ID score type:", peptide_id.getScoreType())
            # PeptideHits
            for hit in peptide_id.getHits():
                print(" - Peptide hit rank:", hit.getRank())
                print(" - Peptide hit sequence:", hit.getSequence().toString())
                print(" - Peptide hit score:", hit.getScore())
                print(" - Mapping to proteins:", [ev.getProteinAccession() for ev in hit.getPeptideEvidences() ] )
                print(" - Fragment annotations:")
                for anno in hit.getPeakAnnotations():
                    print("Charge: " + str(anno.charge))
                    print("m/z:" + str(anno.mz))
                    print("intensity:" + str(anno.intensity))
                    print("label:" + anno.annotation.decode())

    def readMS(self, file_path):
        # Later: process other types of file
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load(file_path, exp)
        return exp

    def drawTic(self, scans):
        self.tic_widget.setTIC(scans.getTIC())

    def redrawPlot(self):
        # set new spectrum and redraw
        self.spectrum_widget.setSpectrum(self.scan_widget.curr_spec)
        if self.isAnnoOn:  # update annotation list
            self.updateController()
        self.spectrum_widget.redrawPlot()

    def updateController(self):
        # for overrriding
        return
