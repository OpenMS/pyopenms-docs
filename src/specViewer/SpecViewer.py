import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, \
        QHBoxLayout, QWidget, QDesktopWidget, QMessageBox, QPushButton, \
        QLabel, QAction, QFileDialog, QTableView, QSplitter, \
        QDialog, QToolButton, QLineEdit, QRadioButton, QGroupBox, QMenu,\
        QFormLayout, QDialogButtonBox, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal, QItemSelectionModel, QSortFilterProxyModel, QSignalMapper, QPoint, QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPainter, QIcon, QBrush, QColor, QPen, QPixmap, QIntValidator

import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np
import pandas as pd
from collections import namedtuple

# define Constant locally until bug in pyOpenMS is fixed
def pyopenms():
    def Constants():
        PROTON_MASS_U = 1.0072764667710
import pyopenms 
#import pyopenms.Constants

# structure for each input masses
MassDataStruct = namedtuple('MassDataStruct', "mz_theo_arr \
                            color marker")
#                            isMono isAvg
TOL = 1e-5 # ppm
#colorset = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
pg.setConfigOption('background', 'w') # white background
pg.setConfigOption('foreground', 'k') # black peaks

SymbolSet = ('o', 's', 't', 't1', 't2', 't3','d', 'p', 'star')
RGBs = [[0,0,200], [0,128,0], [19,234,201], [195,46,212], [237,177,32],
    [54,55,55], [0,114,189],[217,83,25], [126,47,142], [119,172,48]]
Symbols = pg.graphicsItems.ScatterPlotItem.Symbols

class MassList():

    def __init__(self, file_path):
        df = pd.read_csv(file_path, sep='\t', header=0) # data with only one column and header is expected
        self.setMassList(df)

    def setMassList(self, df):
        if 'MonoisotopicMass' in df.columns: # parsing a result file from FLASHDeconv
            self.mass_list = df['MonoisotopicMass'].to_numpy().ravel().tolist()
        else :
            self.mass_list = df.to_numpy().ravel().tolist()

    def getMassStruct(self, cs_range=[2,100]):
        mds_dict = {}
        for mNum, mass in enumerate(self.mass_list):
            mds_dict[mass] = self.getMassDataStructItem(mNum, mass, cs_range)
        return mds_dict
    
    def getMassDataStructItem(self, index, mass, cs_range):
        marker = SymbolSet[index%len(SymbolSet)]
        color = RGBs[index%len(RGBs)]
        theo_mz = self.calculateTheoMzList(mass, cs_range)
        return MassDataStruct(mz_theo_arr=theo_mz, 
                    marker=marker, color=color)

    def calculateTheoMzList(self, mass, cs_range, mz_range=(0,0)):
        theo_mz_list = []
        for cs in range(cs_range[0], cs_range[1]+1):
            print(type(mass), "....", mass)
            mz = (mass + cs * pyopenms.Constants.PROTON_MASS_U) / cs
            ''' add if statement for mz_range '''
            theo_mz_list.append((cs,mz))
        return theo_mz_list
    
    def addNewMass(self, new_mass):
        index = len(self.mass_list)
        self.mass_list.append(new_mass)
        return self.getMassDataStructItem(index, new_mass)
        
class MassSpecData():

    def readMzML(self, mzML_path):
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load(mzML_path, exp)

        scan_list = []
        for spec in exp:
            scan_list.append(spec)
        
        return scan_list

class Spectrum():

    def __init__(self, spec):
        self.spectrum = spec
    
    def findNearestPeakWithTheoPos(self, theo_mz, tol=-1):
        nearest_p = self.spectrum[self.spectrum.findNearest(theo_mz)] # test purpose
        if tol == -1:
            tol = TOL * theo_mz # ppm
        if abs(theo_mz-nearest_p.getMZ()) > tol:
            return None;
        
        return nearest_p

class SpectrumWidget(PlotWidget):
    
    def __init__(self, parent=None, dpi=100):
        PlotWidget.__init__(self)
        self.setLimits(yMin=0, xMin=0)
        # self.setMouseEnabled(y=False)
        self.setLabel('bottom', 'm/z')
        self.setLabel('left', 'intensity')
        self.getViewBox().sigRangeChangedManually.connect(self.modifyYAxis)
        self.highlighted_peak_label = None
        self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60, slot=self.onMouseMoved)
    
    def modifyYAxis(self):
        self.currMaxY = self.getMaxIntensityInRange(self.getAxis('bottom').range)
        if self.currMaxY:
            self.setYRange(0, self.currMaxY)

        try:
            if self._charge_visible:
                self.annotateChargeLadder(self._charge_visible)
        except (AttributeError, NameError):
            return

    def plot_func(self, spec):
        # plot spectrum
        self.plot(clear=True)
        self.spec = spec
        self.mz, self.ints = self.spec.spectrum.get_peaks()
        self.plot_spectrum(self.mz, self.ints)

    def plot_anno(self, masses):
        # initiation
        try:
            for p in self._charge_mark_on_peak:
                p.clear()
            for l in self._charge_mark_on_peak_label:
                l.setPos(0,0)
            for mass in self._charge_ladder_lines:
                for key, value in self._charge_ladder_lines[mass].items():
                    value.clear()
                for key, value in self._charge_ladder_labels[mass].items():
                    value.setPos(0,0)
            cur_visible = self._charge_visible
        except (AttributeError, NameError):
            cur_visible = []

        self._charge_mark_on_peak = []
        self._charge_mark_on_peak_label = []
        self._charge_ladder_lines = dict()
        self._charge_ladder_labels = dict()

        self.masses = masses
        # annotation        
        'anno: on expr. peak'
        self.annotateChargesOnPeak()
        
        'anno: charge ladder'
        self.currMaxY = self.getMaxIntensityInRange(self.getAxis('bottom').range) 
        self.annotateChargeLadder(cur_visible)
        
    def getMaxIntensityInRange(self, xrange):
        left = np.searchsorted(self.mz, xrange[0], side='left')
        right = np.searchsorted(self.mz, xrange[1], side='right')
        return np.amax(self.ints[left:right], initial = 1)        
        
    def plot_spectrum(self, data_x, data_y):
        bargraph = pg.BarGraphItem(x=data_x, height=data_y, width=0)
        self.addItem(bargraph)
        
    def annotateChargesOnPeak(self):
        for mass, mass_strc in self.masses.items():
            theo_list = mass_strc.mz_theo_arr
            
            for theo in theo_list:
                exp_p = self.spec.findNearestPeakWithTheoPos(theo[1])
                if exp_p==None or exp_p.getIntensity()==0:
                    continue
                x = exp_p.getMZ()
                y = exp_p.getIntensity()
                self._charge_mark_on_peak.append(self.plot([x], [y], symbol=mass_strc.marker, 
                          symbolBrush=pg.mkBrush(mass_strc.color), symbolSize=14))
                label = pg.TextItem(text='+'+str(theo[0]), color=(0,0,0), anchor=(0.5,1))
                self.addItem(label)
                label.setPos(x, y)
                self._charge_mark_on_peak_label.append(label)

    def annotateChargeLadder(self, charge_visible=[]):
        self._charge_visible = charge_visible

        for mass, mass_strc in self.masses.items():
            mass = str(mass)
            if mass in self._charge_visible:

                # calculating charge ladder....
                theo_list = mass_strc.mz_theo_arr 
                mzlist = []
                # xlimit = self.getAxis('bottom').range
                xlimit = [self.mz[0], self.mz[-1]]
                for theo in theo_list: # [0]charge [1]mz
                    if ( (theo[1] <= xlimit[0]) | (theo[1] >= xlimit[1]) ):
                        continue
                    mzlist.append(theo)

                if mass not in self._charge_ladder_lines: # should be visible, but not drawn before
                    pen = pg.mkPen(mass_strc.color, width=2, style=Qt.DotLine)
                    self._charge_ladder_lines[mass] = {}
                    self._charge_ladder_labels[mass] = {}
                    self._charge_ladder_lines[mass]['horizon'] = self.plot([xlimit[0], xlimit[1]],[self.currMaxY, self.currMaxY], pen=pen)
                    for th in mzlist:
                        self._charge_ladder_lines[mass][th[0]] = self.plot([th[1], th[1]], [0, self.currMaxY], pen=pen)
                        label = pg.TextItem(text='+'+str(th[0]), color=mass_strc.color, anchor=(1,-1))
                        label.setPos(th[1], self.currMaxY)
                        # self._charge_ladder_lines[mass][th[0]].addItem(label)
                        label.setParentItem(self._charge_ladder_lines[mass][th[0]])
                        self._charge_ladder_labels[mass][th[0]] = label
                    # self.addItem(pg.InfiniteLine(pos=self.currMaxY, angle=0))
                    # anno_vb.addItem(pg.InfiniteLine(pos=theo[1], angle=90))
                else:
                    self._charge_ladder_lines[mass]['horizon'].setData([xlimit[0], xlimit[1]],[self.currMaxY, self.currMaxY])
                    for th in mzlist:
                        self._charge_ladder_lines[mass][th[0]].setData([th[1], th[1]], [0, self.currMaxY])
                        self._charge_ladder_labels[mass][th[0]].setPos(th[1], self.currMaxY)
            else:
                if mass in self._charge_ladder_lines:
                    for key, value in self._charge_ladder_lines[mass].items():
                        value.clear()
                    for key, value in self._charge_ladder_labels[mass].items():
                        value.setPos(0,0)

    def onMouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.sceneBoundingRect().contains(pos):
            mouse_point = self.getViewBox().mapSceneToView(pos)
            pixel_width = self.getViewBox().viewPixelSize()[0]
            left = np.searchsorted(self.mz, mouse_point.x() - 4.0 * pixel_width, side='left')
            right = np.searchsorted(self.mz, mouse_point.x() + 4.0 * pixel_width, side='right')
            if (left == right): # none found -> remove text
                if self.highlighted_peak_label != None:
                    self.highlighted_peak_label.setText("")
                return            
            idx_max_int_in_range = np.argmax(self.ints[left:right])    
            x = self.mz[left + idx_max_int_in_range]
            y = self.ints[left + idx_max_int_in_range]
            if self.highlighted_peak_label == None:
                self.highlighted_peak_label = pg.TextItem(text='{0:.3f}'.format(x), color=(100,100,100), anchor=(0.5,1))
                self.addItem(self.highlighted_peak_label)            
            self.highlighted_peak_label.setText('{0:.3f}'.format(x))
            self.highlighted_peak_label.setPos(x, y)
        else:
            # mouse moved out of visible area: remove highlighting item
            if self.highlighted_peak_label != None:
                self.highlighted_peak_label.setText("")

class ScanWidget(QWidget):
    
    scanClicked = pyqtSignal() # signal to connect SpectrumWidget
    header = ('MS level', 'Index', 'RT')
    def __init__(self, scanList, *args):
       QWidget.__init__(self, *args)
       self.scanList = scanList

       self.table_model = ScanTableModel(self, self.scanList, self.header)
       self.table_view = QTableView()

       # register a proxy class for filering and sorting the scan table
       self.proxy = QSortFilterProxyModel(self)
       self.proxy.setSourceModel(self.table_model)

       # setup selection model
       self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
       self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
       self.table_view.setModel(self.proxy)
       self.table_view.setSelectionModel(QItemSelectionModel(self.proxy))

       # header
       self.horizontalHeader = self.table_view.horizontalHeader()
       self.horizontalHeader.sectionClicked.connect(self.onHeaderClicked)

       # enable sorting
       self.table_view.setSortingEnabled(True)

       # connect signals to slots
       self.table_view.selectionModel().currentChanged.connect(self.onCurrentChanged) # keyboard moves to new row
       self.table_view.clicked.connect(self.onRowSelected)
       self.horizontalHeader.sectionClicked.connect(self.onHeaderClicked)
       
       layout = QVBoxLayout(self)
       layout.addWidget(self.table_view)
       self.setLayout(layout)
       
       # default : first row selected.
       self.table_view.selectRow(0)
       
    def onRowSelected(self, index):
        if index.siblingAtColumn(1).data() == None: return # prevents crash if row gets filtered out
        self.curr_spec = Spectrum(self.scanList[index.siblingAtColumn(1).data()])
        self.scanClicked.emit()
    
    def onCurrentChanged(self, new_index, old_index):
        self.onRowSelected(new_index)

    def onHeaderClicked(self, logicalIndex):
        if logicalIndex != 0: return # allow filter on first column only for now

        self.logicalIndex  = logicalIndex
        self.menuValues = QMenu(self)
        self.signalMapper = QSignalMapper(self)  

        # get unique values from (unfiltered) model
        valuesUnique = set([ self.table_model.index(row, self.logicalIndex).data()
                        for row in range(self.table_model.rowCount(self.table_model.index(-1, self.logicalIndex)))
                        ])

        if len(valuesUnique) == 1: return # no need to select anything

        actionAll = QAction("Show All", self)
        actionAll.triggered.connect(self.onShowAllRows)
        self.menuValues.addAction(actionAll)
        self.menuValues.addSeparator()

        for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):              
            action = QAction(actionName, self)
            self.signalMapper.setMapping(action, actionNumber)  
            action.triggered.connect(self.signalMapper.map)  
            self.menuValues.addAction(action)

        self.signalMapper.mapped.connect(self.onSignalMapper)  

        # get screen position of table header and open menu
        headerPos = self.table_view.mapToGlobal(self.horizontalHeader.pos())        
        posY = headerPos.y() + self.horizontalHeader.height()
        posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)
        self.menuValues.exec_(QPoint(posX, posY))

    def onShowAllRows(self):
        filterColumn = self.logicalIndex
        filterString = QRegExp( "", Qt.CaseInsensitive, QRegExp.RegExp )
        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    def onSignalMapper(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        filterString = QRegExp(stringAction, Qt.CaseSensitive, QRegExp.FixedString)

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)


class ScanTableModel(QAbstractTableModel):
    '''
       keep the method names
       they are an integral part of the model
    '''
    def __init__(self, parent, scanlist, header, *args):
       QAbstractTableModel.__init__(self, parent, *args)
       self.scanlist = scanlist # data type: MSSpectrum
       self.header = header
       
       # create array with MSSpectrum (only MS level=1)
       self.scanRows = self.getScanListAsArray(scanlist) # data type: list

    def getScanListAsArray(self, scanlist):
        scanArr = []
        for index, spec in enumerate(scanlist):
            MSlevel = 'MS' + str(spec.getMSLevel())
            RT = spec.getRT()
            scanArr.append([MSlevel, index ,RT])
        return scanArr
        
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
           return self.header[col]
        return None
    
    def rowCount(self, parent):
        return len(self.scanRows)
    
    def columnCount(self, parent):
        return len(self.header)
    
    def setData(self, index, value, role):
        if not index.isValid():
           return False
       
        self.dataChanged.emit(index, index)
        return True
    
    def flags(self, index):
        if not index.isValid():
           return None
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        
    def data(self, index, role):
        if not index.isValid():
           return None
        value = self.scanRows[index.row()][index.column()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

class ControllerWidget(QWidget):

    def __init__(self, mass_path, plot, *args):
        QWidget.__init__(self, *args)
        hbox = QVBoxLayout()
        self.setMaximumWidth(350)
        self.spectrum = plot

        # data processing
        self.mlc = MassList(mass_path)
        self.masses = self.mlc.getMassStruct()

        self.setMassTableView()
        self.setMassLineEdit()
        self.setParameterBox()

        self.spectrum.plot_anno(self.masses) # plotting

        hbox.addWidget(self.massTable)
        hbox.addLayout(self.massLineEditLayout)
        hbox.addWidget(self.paramBox)
        # hbox.addWidget(self.paramButton)
        self.setLayout(hbox)

    def setMassTableView(self):
        # set controller widgets
        self.massTable = QTableView()
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(["Masses"])
        self.model.itemChanged.connect(self.check_check_state)
        for mass, mStruct in self.masses.items():
            self.setListViewWithMass(mass, mStruct)
        self.massTable.setModel(self.model)
        self.massTable.resizeColumnToContents(0)
        self._data_visible = []

    def setMassLineEdit(self):
        self.massLineEditLayout = QHBoxLayout()
        self.massLineEdit = QLineEdit()
        self.massLineEditButton = QToolButton()
        self.massLineEditButton.setText("Add")
        self.massLineEditLabel = QLabel('Add mass to list')
        self.massLineEditLabel.setBuddy(self.massLineEdit)
        self.massLineEditLayout.addWidget(self.massLineEditLabel)
        self.massLineEditLayout.addWidget(self.massLineEdit)
        self.massLineEditLayout.addWidget(self.massLineEditButton)
        self.massLineEditButton.clicked.connect(self.addMassToListView)     

    def setParameterBox(self):
        self.paramBox = QGroupBox('Parameter')
        paramLayout = QVBoxLayout(self.paramBox)

        paramLayout.addLayout(self.setChargeRangeLineEdit())

        self.paramButton = QPushButton()
        self.paramButton.setText('Reload')
        self.paramButton.clicked.connect(self.reloadSpecWithParam)
        paramLayout.addWidget(self.paramButton)

    def setChargeRangeLineEdit(self):
        self.cs_range = [2, 100]

        csRangeEditLayout = QHBoxLayout()
        self.csMinLineEdit = QLineEdit()
        self.csMaxLineEdit = QLineEdit()
        csMinLineEditLabel = QLabel('min')
        csMaxLineEditLabel = QLabel('max')
        self.csMinLineEdit.setText('2')
        self.csMaxLineEdit.setText('100')
        csMinLineEditLabel.setBuddy(self.csMinLineEdit)
        csMaxLineEditLabel.setBuddy(self.csMaxLineEdit)

        csRangeEditLabel = QLabel('Charge range:')
        csRangeEditLabel.setToolTip("Minimum Charge should be equal to or larger than 2")
        csRangeEditLayout.addWidget(csRangeEditLabel)
        csRangeEditLayout.addWidget(csMinLineEditLabel)
        csRangeEditLayout.addWidget(self.csMinLineEdit)
        csRangeEditLayout.addWidget(csMaxLineEditLabel)
        csRangeEditLayout.addWidget(self.csMaxLineEdit)

        return csRangeEditLayout

    def setMassListExportButton(self):
        self.setmassbutton = ''

    def reloadSpecWithParam(self):
        minCs = self.csMinLineEdit.text()
        maxCs = self.csMaxLineEdit.text()
        
        if self.isError_reloadSpecWithParam(minCs, maxCs):
            self.csMinLineEdit.setText('2')
            self.csMaxLineEdit.setText('100')
            return
        
        # redraw
        self.cs_range = [int(minCs), int(maxCs)]
        self.masses = self.mlc.getMassStruct(self.cs_range)
        self.spectrum.plot_anno(self.masses)


    def isError_reloadSpecWithParam(self, minCs, maxCs):
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
        qp.translate(10,10)
        qp.scale(20,20)
        qp.drawPath(Symbols[symbol])
        qp.end()

        return QIcon(px)

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
                self._data_visible.remove(mass)
                self.spectrum.annotateChargeLadder(self._data_visible)
        else:
            if checked:
                self._data_visible.append(mass)
                self.spectrum.annotateChargeLadder(self._data_visible)
    
    def addMassToListView(self):
        new_mass = self.massLineEdit.text()
        self.massLineEdit.clear()
        try:
            new_mass = float(new_mass)
        except:
            return
        new_mass_str = self.mlc.addNewMass(new_mass)
        self.masses[new_mass] = new_mass_str

        # redraw
        self.spectrum.plot_anno(self.masses)
        self.setListViewWithMass(new_mass, new_mass_str)

class OpenMSWidgets(QWidget):

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
        scans = MassSpecData().readMzML(file_path)
        
        # set Widgets
        self.spectrum = SpectrumWidget()
        self.scan = ScanWidget(scans)
        self.scan.scanClicked.connect(self.redrawPlot)
        self.msexperimentWidget.addWidget(self.spectrum)
        self.msexperimentWidget.addWidget(self.scan)
        self.mainlayout.addWidget(self.msexperimentWidget)

        # default : first row selected.
        self.scan.table_view.selectRow(0)
        self.scan.onRowSelected(self.scan.table_view.selectedIndexes()[0])

    def redrawPlot(self):
        self.spectrum.plot_func(self.scan.curr_spec)
        if self.isAnnoOn:
            self.spectrum.plot_anno(self.controller.masses)
            self.spectrum.annotateChargeLadder(self.controller._data_visible) # update with current visibility

    def annotation_FLASHDeconv(self, mass_path):
        
        self.controller = ControllerWidget(mass_path, self.spectrum)
        self.isAnnoOn = True

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
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
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
        fileName, _ = QFileDialog.getOpenFileName(self,
                                "Open File ", "", "mzML Files (*.mzML)")
        if fileName:
            self.mzmlFileLineEdit.setText(fileName)
        
    def openMassFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                            "Open File ", "", "Text Files (*.csv, *tsv)")
        if fileName:
            self.massFileLineEdit.setText(fileName)
    
    def setErrorMessageBox(self):
        self.errorDlg = QMessageBox()
        self.errorDlg.setIcon(QMessageBox.Critical)
        self.errorDlg.setWindowTitle("ERROR")
    
    def handleException(self):        
        
        if not os.path.exists(self.mzmlFileLineEdit.text()):
            self.errorDlg.setText('Input mzML file doesn\'t exist.')
            self.errorDlg.exec_()
            return
        
        if not os.path.exists(self.massFileLineEdit.text()):
            self.errorDlg.setText('Input mass file doesn\'t exist.')
            self.errorDlg.exec_()
            return

        try:
            float(self.tolerance.text())
        except:
            self.errorDlg.setText('Tolerance is not a number.')
            self.errorDlg.exec_()
            return
        
        self.accept()
        
class App(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(1000, 700) # window size
        self.initUI()

    def initUI(self):
        self.setWindowTitle('FLASHDeconvView')
        # self.center()
        
        # layout
        self.setMainMenu()
        self.centerWidget =  QWidget(self)
        self.setCentralWidget(self.centerWidget)
        self.windowLay = QVBoxLayout(self.centerWidget)
        
        # default widget <- per spectrum
        self.setOpenMSWidget()
        
        ## test purpose
        # massPath = "/Users/jeek/Documents/A4B_UKE/FIA_Ova/190509_Ova_native_25ngul_R.tsv"
        # mzmlPath = "/Users/jeek/Documents/A4B_UKE/FIA_Ova/190509_Ova_native_25ngul_R.mzML"
        # self.openmsWidget.loadFile(mzmlPath)
        # self.openmsWidget.annotation_FLASHDeconv(massPath)

    def setOpenMSWidget(self):
        if self.windowLay.count() > 0 :
            self.clearLayout(self.windowLay)
        self.openmsWidget = OpenMSWidgets(self)
        self.windowLay.addWidget(self.openmsWidget)

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
        # FLASHDeconv Viewer
        fdAct = QAction('FLASHDeconvV', self)
        fdAct.triggered.connect(self.startFLASHDeconvV)
        self.toolMenu.addAction(fdAct)
        
    def startFLASHDeconvV(self):
        
        inputDlg = FDInputDialog()
        if inputDlg.exec_(): # data accepted
            self.mzmlPath = inputDlg.mzmlFileLineEdit.text()
            self.massPath = inputDlg.massFileLineEdit.text()
            self.tol = inputDlg.tolerance.text()
            self.isAvg = inputDlg.mTypeButton2.isChecked()
            
            if self.isAvg:
                print("Calculate with AVG mass")

            self.setOpenMSWidget()
            self.openmsWidget.loadFile(self.mzmlPath)
            self.openmsWidget.annotation_FLASHDeconv(self.massPath)
    
    def clearLayout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                "Open File ", "", "mzML Files (*.mzML)")
        if fileName:
            print('opening...', fileName)
            self.setOpenMSWidget()
            self.openmsWidget.loadFile(fileName)

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
