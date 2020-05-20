from collections import namedtuple

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QSplitter
from PyQt5.QtCore import Qt

from SpectrumWidget import SpectrumWidget
from ScanTableWidget import ScanTableWidget, ScanTableModel
from SequenceIonsWidget import SequenceIonsWidget
from TICWidget import TICWidget
from ErrorWidget import ErrorWidget

import pyopenms
import re
import numpy as np
import json

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


class ControllerWidget(QWidget):
    """
    Used to merge spectrum, table, TIC, error plot and sequenceIons widgets together.

    """

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.mainlayout = QHBoxLayout(self)
        self.isAnnoOn = True
        self.clickedRT = None
        self.seleTableRT = None
        self.mzs = np.array([])
        self.ppm = np.array([])
        self.colors = np.array([])
        self.scanIDDict = {}
        self.curr_table_index = None
        self.filteredIonFragments = []
        self.peakAnnoData = None

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

        # connected signals
        self.scan_widget.sigScanClicked.connect(self.updateWidgetDataFromRow)
        self.tic_widget.sigRTClicked.connect(self.ticToTable)

        self.msexperimentWidget.addWidget(self.tic_widget)
        self.msexperimentWidget.addWidget(self.seqIons_widget)
        self.msexperimentWidget.addWidget(self.spectrum_widget)
        self.msexperimentWidget.addWidget(self.error_widget)
        self.msexperimentWidget.addWidget(self.scan_widget)
        self.mainlayout.addWidget(self.msexperimentWidget)

        # set widget sizes, where error plot is set smaller
        widget_height = self.msexperimentWidget.sizeHint().height()
        size_list = [
            widget_height,
            widget_height,
            widget_height,
            widget_height * 0.5,
            widget_height,
        ]
        self.msexperimentWidget.setSizes(size_list)

        # default : first row selected.
        self.scan_widget.table_view.selectRow(0)

    def loadFileIdXML(self, file_path):
        prot_ids = []
        pep_ids = []
        pyopenms.IdXMLFile().load(file_path, prot_ids, pep_ids)
        Ions = {}

        # extract ID data from file
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
                    ion_label = anno.annotation.decode()

                    Ions[ion_label] = [ion_mz, ion_charge]

                self.scanIDDict[round(pep_rt, 3)] = {
                    "m/z": pep_mz,
                    "PepSeq": pep_seq,
                    "PepIons": Ions,
                }
                Ions = {}

        self.saveIdData()

    def saveIdData(self):  # save ID data in table (correct rows) for later usage
        rows = self.scan_widget.table_model.rowCount(self.scan_widget)

        for row in range(0, rows - 1):
            tableRT = round(
                self.scan_widget.table_model.index(row, 2).data(), 3)
            if tableRT in self.scanIDDict:
                index_seq = self.scan_widget.table_model.index(row, 6)
                self.scan_widget.table_model.setData(
                    index_seq, self.scanIDDict[tableRT]["PepSeq"], Qt.DisplayRole
                )

                index_ions = self.scan_widget.table_model.index(row, 7)
                # data needs to be a string, but reversible -> using json.dumps()
                self.scan_widget.table_model.setData(
                    index_ions,
                    json.dumps(self.scanIDDict[tableRT]["PepIons"]),
                    Qt.DisplayRole,
                )

    def readMS(self, file_path):
        # read MzML files
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load(file_path, exp)
        return exp

    def drawTic(self, scans):
        self.tic_widget.setTIC(scans.getTIC())

    def ticToTable(self, rt):  # connect Tic info to table, and select specific row
        self.clickedRT = round(rt * 60, 3)
        if self.clickedRT != self.seleTableRT:
            self.scan_widget.table_view.selectRow(self.findClickedRT())

    def findClickedRT(self):  # find clicked RT in the scan table
        rows = self.scan_widget.table_model.rowCount(self.scan_widget)

        for row in range(0, rows - 1):
            if self.clickedRT == round(
                self.scan_widget.table_model.index(row, 2).data(), 3
            ):
                index = self.scan_widget.table_model.index(row, 2)
                try:
                    self.curr_table_index = self.scan_widget.proxy.mapFromSource(
                        index
                    )  # use proxy to get from filtered model index
                    return self.curr_table_index.row()
                except ValueError:
                    print("could not found ModelIndex of row")

    # for the future calculate ppm and add it to the table
    def errorData(self, ions_data):
        if ions_data not in "-":
            ions_data_dict = json.loads(ions_data)
            if ions_data_dict != {}:
                self.colors, self.mzs = self.filterColorsMZIons(ions_data_dict)
                mzs_size = len(self.mzs)
                self.ppm = np.random.randint(0, 3, size=mzs_size)
                self.error_widget.setMassErrors(
                    self.mzs, self.ppm, self.colors
                )  # works for a static np.array
            else:
                self.error_widget.clear()
        else:
            self.error_widget.clear()

    def filterColorsMZIons(
        self, ions_data_dict
    ):  # create color/mz array by distinguishing between prefix & suffix ions
        self.peakAnnoData = (
            {}
        )  # key is ion annotation (e.g. b2): [mz, color distinguishing prefix, suffix]
        colors = []
        mzs = []
        col_red = (255, 0, 0)  # suffix
        col_blue = (0, 0, 255)  # prefix

        for fragData in self.filteredIonFragments:
            anno = fragData[0]
            if anno[0] in "abc":
                colors.append(col_blue)
                mzs.append(ions_data_dict[anno][0])
                self.peakAnnoData[fragData[1]] = [
                    ions_data_dict[anno][0], col_blue]
            elif anno[0] in "xyz":
                colors.append(col_red)
                mzs.append(ions_data_dict[anno][0])
                self.peakAnnoData[fragData[1]] = [
                    ions_data_dict[anno][0], col_red]
        return np.array(colors), np.array(mzs)

    def updateWidgetDataFromRow(
        self, index
    ):  # after clicking on a new row, update spectrum, error plot, peptideSeq
        # current row RT value
        self.seleTableRT = round(index.siblingAtColumn(2).data(), 3)

        # set new spectrum with setting that all peaks should be displayed
        self.spectrum_widget.setSpectrum(
            self.scan_widget.curr_spec, zoomToFullRange=True
        )

        # only draw sequence with given ions for MS2 and error plot
        if index.siblingAtColumn(0).data() == "MS2":
            self.drawSeqIons(
                index.siblingAtColumn(
                    6).data(), index.siblingAtColumn(7).data()
            )
            self.errorData(index.siblingAtColumn(7).data())
            if (
                self.peakAnnoData is not None
            ):  # peakAnnoData created with existing ions in errorData (bc of coloring)
                self.spectrum_widget.setPeakAnnotations(
                    self.createPeakAnnotation())
                self.spectrum_widget.redrawPlot()
            else:
                self.spectrum_widget._clear_peak_annotations()
                self.spectrum_widget.redrawPlot()

        # otherwise delete old data
        elif index.siblingAtColumn(0).data() == "MS1":
            self.seqIons_widget.clear()
            self.error_widget.clear()
            self.peakAnnoData = None
            self.spectrum_widget._clear_peak_annotations()
            self.spectrum_widget.redrawPlot()

    def createPeakAnnotation(self):
        pStructList = []
        # for the future -> check clashes like in the TIC widget and then add labels (should be done in SpectrumWidget)
        for anno, data in self.peakAnnoData.items():
            mz, anno_color = data[0], data[1]
            index = self.find_nearest_Index(self.spectrum_widget._mzs, mz)
            pStructList.append(
                PeakAnnoStruct(
                    mz=self.spectrum_widget._mzs[index],
                    intensity=self.spectrum_widget._ints[index],
                    text_label=anno,
                    symbol=None,
                    symbol_color=anno_color,
                )
            )
        return pStructList

    def find_nearest_Index(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    def drawSeqIons(self, seq, ions):  # generate provided peptide sequence
        seq = re.sub(
            r"\([^)]*\)", "", seq
        )  # remove content in brackets -> easier usage

        # only draw sequence for M2 with peptide and ion data
        if seq not in "-" and ions not in "-":
            self.seqIons_widget.setPeptide(seq)
            # transform string data back to a dict
            ions_dict = json.loads(ions)
            if ions_dict != {}:
                self.suffix, self.prefix = self.filterIonsPrefixSuffixData(
                    ions_dict)
                self.seqIons_widget.setPrefix(self.prefix)
                self.seqIons_widget.setSuffix(self.suffix)
            else:  # no ions data
                self.prefix, self.suffix = {}, {}
                self.seqIons_widget.setPrefix(self.prefix)
                self.seqIons_widget.setSuffix(self.suffix)
                self.peakAnnoData = None
        else:
            self.seqIons_widget.clear()
            self.peakAnnoData = None

    def filterIonsPrefixSuffixData(
        self, ions
    ):  # filter raw ion data and return suffix and prefix dicts
        suffix = {}
        prefix = {}

        ions_anno = list(ions.keys())
        # annotation(s) of raw ion data (used as key(s))
        self.filteredIonFragments = []

        for anno in ions_anno:
            if anno[1].isdigit() and anno[0] in "abcyxz":
                index, anno_short = self.filterAnnotationIon(anno)
                if (
                    (index in suffix)
                    and (anno[0] in "yxz")
                    and (anno_short not in suffix[index])
                ):  # avoid double annos e.g. y14
                    suffix[index].append(anno_short)
                elif (
                    (index in prefix)
                    and (anno[0] in "abc")
                    and (anno_short not in prefix[index])
                ):
                    prefix[index].append(anno_short)
                elif anno[0] in "yxz":  # non existing keys
                    suffix[index] = [anno_short]
                elif anno[0] in "abc":  # non existing keys
                    prefix[index] = [anno_short]
        return suffix, prefix

    def filterAnnotationIon(self, fragment_anno):
        # filter from raw ion data annotation index and filtered annotation name (e.g. y2)
        index = [s for s in re.findall(r"-?\d+\.?\d*", fragment_anno)][0]
        ion_anno = fragment_anno.split(index)[0] + index
        self.filteredIonFragments.append((fragment_anno, ion_anno))
        return int(index), ion_anno
