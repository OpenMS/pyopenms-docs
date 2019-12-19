import sys

from PyQt5.QtGui import QColor, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, \
    QHBoxLayout, QWidget, QDesktopWidget, \
    QAction, QFileDialog, QTableView, QSplitter, \
    QMenu, QAbstractItemView, QTableWidgetItem
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal, QItemSelectionModel, QSortFilterProxyModel, QSignalMapper, \
    QPoint, QRegExp, QPersistentModelIndex, QModelIndex
from SpectrumWidget import *
from ScanTableWidget import ScanTableWidget, ScanTableModel
from SequenceIonsWidget import SequenceIonsWidget
from TICWidget import TICWidget
from ErrorWidget import ErrorWidget

import pyopenms
import numpy as np

class AllWidgets(QWidget): # mergingWidgets


    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.mainlayout = QHBoxLayout(self)
        self.isAnnoOn = False
        self.clickedRT = None
        self.seleTableRT = None
        self.mzs = np.array([])
        self.ppm = np.array([])
        self.colors = np.array([])
        self.scanIDDict = {}
        self.curr_table_index = None

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
        self.scan_widget.scanClickedRT.connect(self.getTableRT)
        self.scan_widget.scanClickedSeqIons.connect(self.drawSeqIons)
        self.tic_widget.sigRTClicked.connect(self.ticToTable)
        self.spectrum_widget.sigSpectrumMZs.connect(self.errorData)

        self.msexperimentWidget.addWidget(self.tic_widget)
        self.msexperimentWidget.addWidget(self.seqIons_widget)
        self.msexperimentWidget.addWidget(self.spectrum_widget)
        self.msexperimentWidget.addWidget(self.error_widget)
        self.msexperimentWidget.addWidget(self.scan_widget)
        self.mainlayout.addWidget(self.msexperimentWidget)

        # set widget sizes
        widget_height = self.msexperimentWidget.sizeHint().height()
        size_list = [widget_height, widget_height, widget_height, widget_height * 0.5, widget_height]
        self.msexperimentWidget.setSizes(size_list)

        # default : first row selected.
        self.scan_widget.table_view.selectRow(0)

    def loadFileIdXML(self, file_path):
        prot_ids = []; pep_ids = []
        pyopenms.IdXMLFile().load(file_path, prot_ids, pep_ids)
        Ions = {}

        ''' 
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
                print(" - Mapping to proteins:", [ev.getProteinAccession() for ev in hit.getPeptideEvidences() ])
                print(" - Fragment annotations:")

                for anno in hit.getPeakAnnotations():
                    print("Charge: " + str(anno.charge))
                    print("m/z:" + str(anno.mz))
                    print("intensity:" + str(anno.intensity))
                    print("label:" + anno.annotation.decode())
                    
                    Ions.append([anno.charge, anno.mz, anno.intensity,anno.annotation.decode()])

                self.scanIDDict[round(peptide_id.getRT(), 1)] = {'m/z': peptide_id.getMZ(), 'PepSeq': str(hit.getSequence().toString()), 'ions': Ions}
                Ions = []  
        '''

        for peptide_id in pep_ids:
            pep_mz = peptide_id.getMZ()
            pep_rt = peptide_id.getRT()

            for hit in peptide_id.getHits():
                pep_seq = str(hit.getSequence().toString())
                if "." in pep_seq:
                    pep_seq = pep_seq[3:-1]
                else:
                    pep_seq = pep_seq[2:-1]


                for anno in hit.getPeakAnnotations():
                    ion_charge = anno.charge
                    ion_mz = anno.mz
                    ion_int = anno.intensity
                    ion_label = anno.annotation.decode()

                    Ions[ion_label] = {ion_charge, ion_mz, ion_int}

                self.scanIDDict[round(pep_rt, 1)] = {'m/z': pep_mz, 'PepSeq': pep_seq, 'PepIons': Ions}
                Ions = {}

        self.saveIdData()


    def readMS(self, file_path):
        # Later: process other types of file
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load(file_path, exp)
        return exp

    def getTableRT(self, rt):
        self.seleTableRT = rt

    def drawTic(self, scans):
        self.tic_widget.setTIC(scans.getTIC())

    def ticToTable(self, rt): # connect Tic info to table, and select specific row
        self.clickedRT = round(rt * 60, 1)
        if self.clickedRT != self.seleTableRT:
            try:
                self.scan_widget.table_view.selectRow(self.findClickedRT())
            except:
                print(self.findClickedRT())

    def findClickedRT(self): # find clicked RT in the scan table
        rows = self.scan_widget.table_model.rowCount(self.scan_widget)

        for row in range(0, rows - 1):
            if self.clickedRT == round(self.scan_widget.table_model.index(row, 2).data(), 1):
                index = self.scan_widget.table_model.index(row, 2)
                self.curr_table_index = self.scan_widget.proxy.mapFromSource(index) # use proxy to get from filtered model index
                return self.curr_table_index.row()


    # TODO calculate ppm
    def errorData(self, mzs):
        self.mzs = mzs
        mzs_size = len(self.mzs)
        test = np.random.randint(0, 40, size=20)
        self.ppm = np.random.randint(-3.0, 3.0, size=20)
        #self.ppm = np.zeros(mzs_size)
        self.colors = np.random.randint(0, 255, size=(20, 3))
        self.error_widget.setMassErrors(test, self.ppm, self.colors)  # works for a static np.array

    def redrawPlot(self):
        # set new spectrum and redraw
        self.spectrum_widget.setSpectrum(self.scan_widget.curr_spec)
        if self.isAnnoOn:  # update annotation list
            self.updateController()
        self.spectrum_widget.redrawPlot()

    def updateController(self):
        # for overrriding
        return

    def saveIdData(self): # save ID data in table for later usage
        rows = self.scan_widget.table_model.rowCount(self.scan_widget)

        for row in range(0, rows - 1):
            tableRT = round(self.scan_widget.table_model.index(row, 2).data(), 1)
            if tableRT in self.scanIDDict:
                index_seq = self.scan_widget.table_model.index(row, 6)
                self.scan_widget.table_model.setData(index_seq, self.scanIDDict[tableRT]['PepSeq'], Qt.DisplayRole)

                index_ions = self.scan_widget.table_model.index(row, 7)
                self.scan_widget.table_model.setData(index_ions, str(self.scanIDDict[tableRT]['PepIons']), Qt.DisplayRole) # data needs to be a string, but reversible

    def drawSeqIons(self, seq, ions): # generate provided peptide sequence
        self.seqIons_widget.setPeptide(seq)
        # transform back to dict
        if ions != "-":
            ions_dict = eval(ions)
            suffix, prefix = self.filterIonsPrefixSuffix(ions_dict)
            self.seqIons_widget.setPrefix(prefix)
            self.seqIons_widget.setSuffix(suffix)


    def filterIonsPrefixSuffix(self, ions):
        suffix = {}
        prefix = {}
        ions_anno = list(ions.keys())
        for anno in ions_anno:
            if anno[0] in "yxz":
                suffix[int(anno[1])] = [anno[:2]]
            elif anno[0] in "abc":
                prefix[int(anno[1])] = [anno[:2]]
        return suffix, prefix



