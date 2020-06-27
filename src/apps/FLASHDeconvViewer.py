import os
import sys
from collections import namedtuple

import numpy as np
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QPainter,
    QIcon,
    QBrush,
    QColor,
    QPen,
    QPixmap,
    QIntValidator,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QMessageBox,
    QPushButton,
    QLabel,
    QAction,
    QFileDialog,
    QTableView,
    QSplitter,
    QDialog,
    QToolButton,
    QLineEdit,
    QRadioButton,
    QGroupBox,
    QFormLayout,
    QDialogButtonBox,
)
from matplotlib import cm
from pyqtgraph import PlotWidget

sys.path.insert(0, "../view")
from SpecViewer import ScanBrowserWidget, App

# import pyopenms.Constants
# define Constant locally until bug in pyOpenMS is fixed
PROTON_MASS_U = 1.0072764667710
C13C12_MASSDIFF_U = 1.0033548378

# structure for each input masses
MassDataStruct = namedtuple(
    "MassDataStruct",
    "mz_theo_arr \
                            startRT endRT maxIntensity scanCount \
                            color marker",
)
#                            isMono isAvg
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
TOL = 1e-5  # ppm

SymbolSet = ("o", "s", "t", "t1", "t2", "t3", "d", "p", "star")
RGBs = [
    [0, 0, 200],
    [0, 128, 0],
    [19, 234, 201],
    [195, 46, 212],
    [237, 177, 32],
    [54, 55, 55],
    [0, 114, 189],
    [217, 83, 25],
    [126, 47, 142],
    [119, 172, 48],
]
Symbols = pg.graphicsItems.ScatterPlotItem.Symbols


class MassList:
    def __init__(self, file_path):
        if not file_path:
            self.mass_list = []
            return

        self.data = pd.read_csv(file_path, sep="\t", header=0)
        self.isFDresult = self.isValidFLASHDeconvFile()
        self.setRTMassDict()
        self.setMassList(self.data)

    def setMassList(self, df):
        if self.isFDresult:  # parsing a result file from FLASHDeconv
            self.mass_list = df["MonoisotopicMass"].to_numpy().ravel().tolist()
        else:
            self.mass_list = df.to_numpy().ravel().tolist()

    def setMassStruct(self, cs_range=[2, 100]):
        mds_dict = {}

        for mNum, mass in enumerate(self.mass_list):
            mds_dict[mass] = self.setMassDataStructItem(mNum, mass, cs_range)
        return mds_dict

    def getMassStruct(self, masslist, cs_range=[2, 100]):
        mds_dict = {}

        for mass in masslist:
            mNum = self.mass_list.index(mass)
            mds_dict[mass] = self.setMassDataStructItem(mNum, mass, cs_range)
        return mds_dict

    def setMassDataStructItem(self, index, mass, cs_range):
        marker = SymbolSet[index % len(SymbolSet)]
        color = RGBs[index % len(RGBs)]
        theo_mz = self.calculateTheoMzList(mass, cs_range)
        rt_s = 0
        rt_e = sys.maxsize
        mi = 0
        c = 0
        try:
            if mass in self.RTMassDict.keys():
                rt_s = float(self.RTMassDict[mass]["StartRetentionTime"])
                rt_e = float(self.RTMassDict[mass]["EndRetentionTime"])
                mi = float(self.RTMassDict[mass]["MaxIntensity"])
                c = int(self.RTMassDict[mass]["MassCount"])
        except (AttributeError, NameError):  # no input mass file
            pass

        return MassDataStruct(
            mz_theo_arr=theo_mz,
            startRT=rt_s,
            endRT=rt_e,
            maxIntensity=mi,
            scanCount=c,
            marker=marker,
            color=color,
        )

    def calculateTheoMzList(self, mass, cs_range, mz_range=(0, 0)):
        theo_mz_list = []
        for cs in range(cs_range[0], cs_range[1] + 1):
            mz = (mass + cs * PROTON_MASS_U) / cs
            iso = [
                C13C12_MASSDIFF_U / cs * i + mz for i in range(10)
            ]  # 10 should be changed based on the mass, later.
            theo_mz_list.append((cs, np.array(iso)))
        return theo_mz_list

    def addNewMass(self, new_mass, index, cs_range):
        return self.setMassDataStructItem(index, new_mass, cs_range)

    def isValidFLASHDeconvFile(self):
        col_needed = [
            "MonoisotopicMass",
            "AverageMass",
            "StartRetentionTime",
            "EndRetentionTime",
        ]
        result = all(elem in list(self.data) for elem in col_needed)
        if result:
            return True
        return False

    def setRTMassDict(self):
        self.RTMassDict = dict()
        if self.isFDresult:
            self.RTMassDict = self.data.set_index(
                "MonoisotopicMass").to_dict("index")


class FeatureMapPlotWidget(PlotWidget):
    def __init__(self, mass_data, parent=None, dpi=100):
        PlotWidget.__init__(self)
        self.data = mass_data
        self.setLabel("bottom", "Retension Time (sec)")
        self.setLabel("left", "Mass (Da)")
        self.setLimits(yMin=0, xMin=0)
        self.showGrid(True, True)
        # self.setBackground('k')
        self.drawPlot()
        # self.setColorbar()

    # def setColorbar(self):
    #     self.img = pg.ImageItem()
    #     self.getPlotItem().addItem(self.img)
    #     self.img.setLookupTable(self.pg_cmap.getLookupTable)
    #     self.hist = pg.HistogramLUTItem()
    #     self.hist.setImageItem(self.img)
    #     # self.addItem(self.hist)

    def drawPlot(self):
        cmap = self.getColorMap()

        for mass, mds in self.data.items():
            spi = pg.ScatterPlotItem(
                size=10,  # pen=pg.mkPen(None),
                brush=pg.mkBrush(cmap.mapToQColor(mds.maxIntensity)),
            )
            self.addItem(spi)
            spots = [{"pos": [i, mass]}
                     for i in np.arange(mds.startRT, mds.endRT, 1)]
            # print([i for i in np.arange(mds.startRT, mds.endRT, 1)])
            spi.addPoints(spots)

    def getColorMap(self):
        miList = self.getMassIntensityDict()
        colormap = cm.get_cmap("plasma")
        colormap._init()
        lut = \
            (colormap._lut * 255).view(np.ndarray)[: colormap.N]
        # Convert matplotlib colormap from 0-1 to 0 -255 for Qt
        self.pg_cmap = pg.ColorMap(pos=miList, color=lut)
        return self.pg_cmap

    def getMassIntensityDict(self):
        # miDict = dict()
        miList = list()
        for m, mds in self.data.items():
            # miDict[m] = mds.maxIntensity
            miList.append(mds.maxIntensity)
        return miList


class PlotWindow(QMainWindow):
    def __init__(self, mlc, mass_data, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("Feature map")
        cWidget = QWidget()
        self.setCentralWidget(cWidget)
        self.layout = QHBoxLayout(cWidget)

        fmWidget = FeatureMapPlotWidget(mass_data)
        self.colormap = fmWidget.pg_cmap

        self.layout.addWidget(fmWidget)
        # cWidget.addItem(fmWidget.hist)

        # self.addColorBar(mlc)

    def addColorBar(self, mlc):
        self.img = pg.ColorMapWidget()
        self.img.setFields([("MaxIntensity", {})])
        self.img.map(mlc.data)
        # self.img.setLookupTable(self.colormap.getLookupTable)
        # https://groups.google.com/forum/#!searchin/pyqtgraph/color$20scale$20plotwidget/pyqtgraph/N4ysAIhPBgo/JO36xjz1BwAJ
        # imgV = pg.ImageView(view=pg.PlotItem())
        self.layout.addWidget(self.img)


class ControllerWidget(QWidget):
    def __init__(self, mass_path, plot, *args):
        QWidget.__init__(self, *args)
        self.mass_path = mass_path
        hbox = QVBoxLayout()
        self.setMaximumWidth(350)
        self.spectrum_widget = plot

        # data processing
        self.mlc = MassList(mass_path)
        self.total_masses = self.mlc.setMassStruct()
        self.masses = dict()  # initialization

        self.setFeatureMapButton()
        self.setMassTableView()
        self.setMassLineEdit()
        self.setParameterBox()

        hbox.addWidget(self.fmButton)
        hbox.addWidget(self.massTable)
        hbox.addLayout(self.massLineEditLayout)
        hbox.addWidget(self.paramBox)
        # hbox.addWidget(self.paramButton)
        self.setLayout(hbox)

    def _updatePlot(self):
        # uncheck all checkboxes
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            if item.isCheckable():
                item.setCheckState(Qt.Unchecked)

        # reset parameter default value
        self.csMinLineEdit.setText("2")
        self.csMaxLineEdit.setText("100")

        self._data_visible = []
        self.spectrum_widget.setPeakAnnotations(self.getPeakAnnoStruct())
        self.spectrum_widget.setLadderAnnotations(self.getLadderAnnoStruct())

        self.spectrum_widget.redrawPlot()

    def setFeatureMapButton(self):
        self.fmButton = QPushButton()
        self.fmButton.setText("Draw feature map")
        self.fmButton.clicked.connect(self.loadFeatureMapPlot)

    def setMassTableView(self):
        # set controller widgets
        self.massTable = QTableView()
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(["Masses"])
        self.model.itemChanged.connect(self.check_check_state)
        self.massTable.setModel(self.model)
        self.massTable.setColumnWidth(0, 300)
        self._data_visible = []

    def setMassLineEdit(self):
        self.massLineEditLayout = QHBoxLayout()
        self.massLineEdit = QLineEdit()
        self.massLineEditButton = QToolButton()
        self.massLineEditButton.setText("Add")
        self.massLineEditLabel = QLabel("Add mass to list")
        self.massLineEditLabel.setBuddy(self.massLineEdit)
        self.massLineEditLayout.addWidget(self.massLineEditLabel)
        self.massLineEditLayout.addWidget(self.massLineEdit)
        self.massLineEditLayout.addWidget(self.massLineEditButton)
        self.massLineEditButton.clicked.connect(self.addMassToListView)

    def setParameterBox(self):
        self.paramBox = QGroupBox("Parameter")
        paramLayout = QVBoxLayout(self.paramBox)

        paramLayout.addLayout(self.setChargeRangeLineEdit())

        self.paramButton = QPushButton()
        self.paramButton.setText("Reload")
        self.paramButton.clicked.connect(self.redrawAnnotationsWithParam)
        paramLayout.addWidget(self.paramButton)

    def setChargeRangeLineEdit(self):
        self.cs_range = [2, 100]

        csRangeEditLayout = QHBoxLayout()
        self.csMinLineEdit = QLineEdit()
        self.csMaxLineEdit = QLineEdit()
        csMinLineEditLabel = QLabel("min")
        csMaxLineEditLabel = QLabel("max")
        self.csMinLineEdit.setText("2")
        self.csMaxLineEdit.setText("100")
        csMinLineEditLabel.setBuddy(self.csMinLineEdit)
        csMaxLineEditLabel.setBuddy(self.csMaxLineEdit)

        csRangeEditLabel = QLabel("Charge range:")
        csRangeEditLabel.setToolTip(
            "Minimum Charge should be equal to or larger than 2"
        )
        csRangeEditLayout.addWidget(csRangeEditLabel)
        csRangeEditLayout.addWidget(csMinLineEditLabel)
        csRangeEditLayout.addWidget(self.csMinLineEdit)
        csRangeEditLayout.addWidget(csMaxLineEditLabel)
        csRangeEditLayout.addWidget(self.csMaxLineEdit)

        return csRangeEditLayout

    def setMassListExportButton(self):
        self.setmassbutton = ""

    def loadFeatureMapPlot(self):
        if not self.mlc.isFDresult:
            self.errorDlg = QMessageBox()
            self.errorDlg.setIcon(QMessageBox.Critical)
            self.errorDlg.setWindowTitle("ERROR")
            self.errorDlg.setText(
                "Input mass file is not formatted as FLASHDeconv result file."
            )
            self.errorDlg.exec_()
            return
        self.fm_window = PlotWindow(self.mlc, self.total_masses)
        self.fm_window.show()

    def updateMassTableView(self, scan_rt):

        self.masses = self.getMassStructWithRT(scan_rt)
        self.model.removeRows(0, self.model.rowCount())
        self.model.setHorizontalHeaderLabels(["Masses"])
        for mass, mStruct in self.masses.items():
            self.setListViewWithMass(mass, mStruct)
        self.massTable.setColumnWidth(0, 300)
        # update annotation lists
        self._data_visible = []
        self.spectrum_widget.setPeakAnnotations(self.getPeakAnnoStruct())
        self.spectrum_widget.setLadderAnnotations(self.getLadderAnnoStruct())

    def getMassStructWithRT(self, scan_rt):
        new_dict = dict()
        for mass, mds in self.total_masses.items():
            if (mds.startRT == 0 and mds.endRT == sys.maxsize) or (
                    scan_rt >= mds.startRT and scan_rt <= mds.endRT
            ):
                new_dict[mass] = mds
        return new_dict

    def redrawAnnotationsWithParam(self):
        minCs = self.csMinLineEdit.text()
        maxCs = self.csMaxLineEdit.text()

        if self.isError_redrawAnnotationsWithParam(minCs, maxCs):
            self.csMinLineEdit.setText("2")
            self.csMaxLineEdit.setText("100")
            return

        # redraw
        self.cs_range = [int(minCs), int(maxCs)]
        self.masses = self.mlc.getMassStruct(self.masses, self.cs_range)
        self._updatePlot()

    def isError_redrawAnnotationsWithParam(self, minCs, maxCs):
        v = QIntValidator()
        v.setBottom(2)
        self.csMinLineEdit.setValidator(v)
        self.csMaxLineEdit.setValidator(v)

        if int(minCs) > int(maxCs):
            return True

        return False

    def getSymbolIcon(self, symbol, color):

        px = QPixmap(20, 20)
        px.fill(Qt.transparent)
        qp = QPainter(px)
        qpen = QPen(Qt.black, 0.05)
        qc = QColor()
        qc.setRgb(color[0], color[1], color[2])

        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(qpen)
        qp.setBrush(QBrush(qc))
        qp.translate(10, 10)
        qp.scale(20, 20)
        qp.drawPath(Symbols[symbol])
        qp.end()

        return QIcon(px)

    def getPeakAnnoStruct(self):
        pStructList = []
        for mass, mass_strc in self.masses.items():
            theo_list = mass_strc.mz_theo_arr

            for theo in theo_list:  # theo : [0] cs [1] iso mz list
                exp_p = self.findNearestPeakWithTheoPos(
                    theo[1][0])  # Monoisotopic only
                if exp_p is None:
                    continue
                pStructList.append(
                    PeakAnnoStruct(
                        mz=exp_p.getMZ(),
                        intensity=exp_p.getIntensity(),
                        text_label="+" + str(theo[0]),
                        symbol=mass_strc.marker,
                        symbol_color=mass_strc.color,
                    )
                )

        return pStructList

    def getLadderAnnoStruct(self):
        lStructDict = dict()
        xlimit = [self.spectrum_widget.minMZ, self.spectrum_widget.maxMZ]

        for mass, mass_strc in self.masses.items():
            mass = str(mass)
            if mass in self._data_visible:
                # calculating charge ladder
                theo_list = mass_strc.mz_theo_arr
                t_mz_list = []
                txt_list = []

                for theo in theo_list:  # theo : [0] cs [1] iso mz list
                    # plotting only theoretical mz valule
                    # within experimental mz range
                    if (theo[1][0] <= xlimit[0]) | (theo[1][-1] >= xlimit[1]):
                        continue

                    for index, mz in enumerate(theo[1]):
                        t_mz_list.append(mz)
                        txt_list.append("+%d[%d]" % (theo[0], index))
                lStructDict[mass] = LadderAnnoStruct(
                    mz_list=np.array(t_mz_list),
                    text_label_list=np.array(txt_list),
                    color=mass_strc.color,
                )
            else:
                self.spectrum_widget.clearLadderAnnotation(mass)
        return lStructDict

    def findNearestPeakWithTheoPos(self, theo_mz, tol=-1):
        nearest_p = self.spectrum_widget.spec[
            self.spectrum_widget.spec.findNearest(theo_mz)
        ]
        if tol == -1:
            tol = TOL * theo_mz  # ppm
        if abs(theo_mz - nearest_p.getMZ()) > tol:
            return None
        if nearest_p.getIntensity() == 0:
            return None
        return nearest_p

    def setListViewWithMass(self, mass, mStruct):

        icon = self.getSymbolIcon(mStruct.marker, mStruct.color)
        item = QStandardItem(icon, str(mass))
        item.setCheckable(True)

        self.model.appendRow([item])

    def check_check_state(self, i):
        if not i.isCheckable():  # Skip data columns.
            return

        mass = i.text()
        checked = i.checkState() == Qt.Checked

        if mass in self._data_visible:
            if not checked:
                self._data_visible.remove(str(mass))
                self.spectrum_widget.setLadderAnnotations(
                    self.getLadderAnnoStruct())
                self.spectrum_widget.redrawLadderAnnotations()
        else:
            if checked:
                self._data_visible.append(str(mass))
                self.spectrum_widget.setLadderAnnotations(
                    self.getLadderAnnoStruct())
                self.spectrum_widget.redrawLadderAnnotations()

    def addMassToListView(self):
        new_mass = self.massLineEdit.text()
        self.massLineEdit.clear()
        try:
            new_mass = float(new_mass)
        except Exception:
            return
        new_mass_str = self.mlc.addNewMass(
            new_mass, len(self.masses), self.cs_range)
        self.masses[new_mass] = new_mass_str

        # redraw
        self._updatePlot()
        self.setListViewWithMass(new_mass, new_mass_str)


class ScanBrowserWidget_FDV(ScanBrowserWidget):
    def updateController(self):  # overriding from ScanBrowserWidget
        self.controller.updateMassTableView(self.scan_widget.curr_spec.getRT())

    def annotation_FLASHDeconv(self, mass_path):
        self.controller = ControllerWidget(mass_path, self.spectrum_widget)
        self.isAnnoOn = True
        # annotate first scan
        self.redrawPlot()

        # Adding Splitter
        self.splitter_spec_contr = QSplitter(Qt.Horizontal)
        self.splitter_spec_contr.addWidget(self.msexperimentWidget)
        self.splitter_spec_contr.addWidget(self.controller)
        self.mainlayout.addWidget(self.splitter_spec_contr)


class FDInputDialog(QDialog):
    def __init__(self):
        super(FDInputDialog, self).__init__()

        self.setWindowTitle("Starting FLASHDeconv Visualization")
        self.setupUI()

    def setupUI(self):
        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)
        self.setErrorMessageBox()

        # widgets
        self.mzmlFileLineEdit = QLineEdit()
        self.mzmlFileButton = QToolButton()
        self.mzmlFileButton.setText("...")
        self.massFileButton = QToolButton()
        self.massFileLineEdit = QLineEdit()
        self.massFileButton.setText("...")
        self.mTypeButton1 = QRadioButton("Monoisotopic")
        self.mTypeButton2 = QRadioButton("Average")
        self.mTypeButton1.setChecked(True)
        self.tolerance = QLineEdit()
        self.tolerance.setText("10")

        self.setFormGroupBox()

        # connection
        self.mzmlFileButton.clicked.connect(self.openMzMLFileDialog)
        self.massFileButton.clicked.connect(self.openMassFileDialog)

        # from group box - ok/cancel
        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.handleException)
        buttonBox.rejected.connect(self.reject)

        # layout
        mainlayout.addWidget(self.formGroupBox)
        mainlayout.addWidget(buttonBox)

    def setFormGroupBox(self):
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()

        mzmlLyt = QHBoxLayout()
        mzmlLyt.addWidget(self.mzmlFileLineEdit)
        mzmlLyt.addWidget(self.mzmlFileButton)
        massLyt = QHBoxLayout()
        massLyt.addWidget(self.massFileLineEdit)
        massLyt.addWidget(self.massFileButton)
        mTypeLyt = QHBoxLayout()
        mTypeLyt.addWidget(self.mTypeButton1)
        mTypeLyt.addWidget(self.mTypeButton2)
        tolLyt = QHBoxLayout()
        tolLyt.addWidget(self.tolerance)

        layout.addRow(QLabel("Input mzML File:"), mzmlLyt)
        layout.addRow(QLabel("Input Mass File:"), massLyt)
        layout.addRow(QLabel("Input Mass Type:"), mTypeLyt)
        layout.addRow(QLabel("Tolerance(ppm):"), tolLyt)
        self.formGroupBox.setLayout(layout)

    def openMzMLFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File ", "", "mzML Files (*.mzML)"
        )
        if fileName:
            self.mzmlFileLineEdit.setText(fileName)

    def openMassFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File ", "", "Text Files (*.csv, *tsv)"
        )
        if fileName:
            self.massFileLineEdit.setText(fileName)

    def setErrorMessageBox(self):
        self.errorDlg = QMessageBox()
        self.errorDlg.setIcon(QMessageBox.Critical)
        self.errorDlg.setWindowTitle("ERROR")

    def handleException(self):

        if not os.path.exists(self.mzmlFileLineEdit.text()):
            self.errorDlg.setText("Input mzML file doesn't exist.")
            self.errorDlg.exec_()
            return

        if self.massFileLineEdit.text() and not os.path.exists(
                self.massFileLineEdit.text()
        ):
            self.errorDlg.setText("Input mass file doesn't exist.")
            self.errorDlg.exec_()
            return

        try:
            float(self.tolerance.text())
        except Exception:
            self.errorDlg.setText("Tolerance is not a number.")
            self.errorDlg.exec_()
            return

        self.accept()


class App_FDV(App):
    def setOpenMSWidget(self):  # overriding from App
        if self.windowLay.count() > 0:
            self.clearLayout(self.windowLay)
        self.scanbrowser = ScanBrowserWidget_FDV(self)
        self.windowLay.addWidget(self.scanbrowser)

    def setToolMenu(self):  # overriding from App
        # FLASHDeconv Viewer
        fdAct = QAction("FLASHDeconvV", self)
        fdAct.triggered.connect(self.startFLASHDeconvV)
        self.toolMenu.addAction(fdAct)

    def startFLASHDeconvV(self):

        inputDlg = FDInputDialog()
        if inputDlg.exec_():  # data accepted
            self.mzmlPath = inputDlg.mzmlFileLineEdit.text()
            self.massPath = inputDlg.massFileLineEdit.text()
            self.tol = inputDlg.tolerance.text()
            self.isAvg = inputDlg.mTypeButton2.isChecked()

            if self.isAvg:
                print("Calculate with AVG mass")

            self.setOpenMSWidget()
            self.scanbrowser.loadFile(self.mzmlPath)
            self.scanbrowser.annotation_FLASHDeconv(self.massPath)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App_FDV()
    ex.show()
    sys.exit(app.exec_())
