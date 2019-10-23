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
from matplotlib import cm

import pyopenms 

#import pyopenms.Constants
# define Constant locally until bug in pyOpenMS is fixed
PROTON_MASS_U = 1.0072764667710
C13C12_MASSDIFF_U = 1.0033548378

# structure for each input masses
MassDataStruct = namedtuple('MassDataStruct', "mz_theo_arr \
                            startRT endRT maxIntensity scanCount \
                            color marker")
#                            isMono isAvg
PeakAnnoStruct = namedtuple('PeakAnnoStruct', "mz intensity text_label \
                            symbol symbol_color")
LadderAnnoStruct = namedtuple('LadderAnnoStruct', "mz_list \
                            text_label_list color")

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
        self.data = pd.read_csv(file_path, sep='\t', header=0)
        self.isFDresult = self.isValidFLASHDeconvFile()
        self.setRTMassDict()
        self.setMassList(self.data)

    def setMassList(self, df):
        if self.isFDresult: # parsing a result file from FLASHDeconv
            self.mass_list = df['MonoisotopicMass'].to_numpy().ravel().tolist()
        else :
            self.mass_list = df.to_numpy().ravel().tolist()

    def setMassStruct(self, cs_range=[2,100]):
        mds_dict = {}

        for mNum, mass in enumerate(self.mass_list):
            mds_dict[mass] = self.setMassDataStructItem(mNum, mass, cs_range)
        return mds_dict

    def getMassStruct(self, masslist, cs_range=[2,100]):
        mds_dict = {}

        for mass in masslist:
            mNum = self.mass_list.index(mass)
            mds_dict[mass] = self.setMassDataStructItem(mNum, mass, cs_range)
        return mds_dict

    def setMassDataStructItem(self, index, mass, cs_range):
        marker = SymbolSet[index%len(SymbolSet)]
        color = RGBs[index%len(RGBs)]
        theo_mz = self.calculateTheoMzList(mass, cs_range)
        rt_s = 0
        rt_e = sys.maxsize
        mi = 0
        c = 0
        if mass in self.RTMassDict.keys():
            rt_s = float(self.RTMassDict[mass]['StartRetentionTime'])
            rt_e = float(self.RTMassDict[mass]['EndRetentionTime'])
            mi = float(self.RTMassDict[mass]['MaxIntensity'])
            c = int(self.RTMassDict[mass]['MassCount'])
        return MassDataStruct(mz_theo_arr=theo_mz, 
                    startRT=rt_s, endRT=rt_e, maxIntensity=mi, scanCount=c,
                    marker=marker, color=color)

    def calculateTheoMzList(self, mass, cs_range, mz_range=(0,0)):
        theo_mz_list = []
        for cs in range(cs_range[0], cs_range[1]+1):
            mz = (mass + cs * PROTON_MASS_U) / cs
            ''' add if statement for mz_range '''
            iso = [C13C12_MASSDIFF_U/cs*i + mz for i in range(10)]  # 10 should be changed based on the mass, later.
            theo_mz_list.append((cs,np.array(iso)))
        return theo_mz_list
    
    def addNewMass(self, new_mass, cs_range):
        index = len(self.mass_list)
        return self.setMassDataStructItem(index, new_mass, cs_range)

    def isValidFLASHDeconvFile(self):
        col_needed = ['MonoisotopicMass', 'AverageMass', 'StartRetentionTime', 'EndRetentionTime']
        result = all(elem in list(self.data) for elem in col_needed)
        if result:
            return True
        return False

    def setRTMassDict(self):
        self.RTMassDict = dict()
        if self.isFDresult:
            self.RTMassDict = self.data.set_index('MonoisotopicMass').to_dict('index')
        
class FeatureMapPlotWidget(PlotWidget):
    def __init__(self, mass_data , parent=None, dpi=100):
       PlotWidget.__init__(self)
       self.data = mass_data
       self.setLabel('bottom', 'Retension Time (sec)')
       self.setLabel('left', 'Mass (Da)')
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
            spi = pg.ScatterPlotItem(size=10, # pen=pg.mkPen(None), 
                brush=pg.mkBrush(cmap.mapToQColor(mds.maxIntensity)))
            self.addItem(spi)
            spots = [{'pos': [i, mass]} for i in np.arange(mds.startRT, mds.endRT, 1)]
            # print([i for i in np.arange(mds.startRT, mds.endRT, 1)])
            spi.addPoints(spots)

    def getColorMap(self):
        miList = self.getMassIntensityDict()
        colormap = cm.get_cmap("plasma")
        colormap._init()
        lut = (colormap._lut * 255).view(np.ndarray)[:colormap.N] # Convert matplotlib colormap from 0-1 to 0 -255 for Qt
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
        self.setWindowTitle('Feature map')
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
        self.img.setFields([
            ('MaxIntensity', {})
            ])
        self.img.map(mlc.data)
        # self.img.setLookupTable(self.colormap.getLookupTable)
        # https://groups.google.com/forum/#!searchin/pyqtgraph/color$20scale$20plotwidget/pyqtgraph/N4ysAIhPBgo/JO36xjz1BwAJ
        # imgV = pg.ImageView(view=pg.PlotItem())
        self.layout.addWidget(self.img)


class SpectrumWidget(PlotWidget):

    def __init__(self, parent=None, dpi=100):
        PlotWidget.__init__(self)
        self.setLimits(yMin=0, xMin=0)
        self.setMouseEnabled(y=False)
        self.setLabel('bottom', 'm/z')
        self.setLabel('left', 'intensity')
        self.highlighted_peak_label = None
        self.peak_annotations = None
        self.ladder_annotations = None
         # numpy arrays for fast look-up
        self._mzs = np.array([])
        self._ints = np.array([])      
        self.getViewBox().sigRangeChangedManually.connect(self._autoscaleYAxis)  # why sigXRangeChanged?
        self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60, slot=self._onMouseMoved)

    def setSpectrum(self, spectrum):
        # delete old highlighte "hover" peak
        if self.highlighted_peak_label != None:
            self.removeItem(self.highlighted_peak_label)     
            self.highlighted_peak_label = None
        self.spec = spectrum
        self._mzs, self._ints = self.spec.get_peaks()
        # self._autoscaleYAxis() why?
        # for annotation in ControllerWidget
        self.minMZ = np.amin(self._mzs)
        self.maxMZ = np.amax(self._mzs)

    def setPeakAnnotations(self, p_annotations):
        self.peak_annotation_list = p_annotations

    def setLadderAnnotations(self, ladder_visible=[]):
        self._ladder_visible = ladder_visible # LadderAnnoStruct

    def clearLadderAnnotation(self, ladder_key_to_clear):
        try:
            if ladder_key_to_clear in self._ladder_anno_lines.keys():
                self._clear_ladder_item(ladder_key_to_clear)
        except (AttributeError, NameError):
            return    

    def redrawPlot(self):
        self.plot(clear=True)
        self._plot_spectrum()
        self._clear_annotations()
        self._plot_peak_annotations()
        self._plot_ladder_annotations()

    def redrawLadderAnnotations(self):
        self._plot_ladder_annotations()

    def _autoscaleYAxis(self):
        x_range = self.getAxis('bottom').range
        if x_range == [0, 1]: # workaround for axis sometimes not being set TODO: check if this is resovled
            x_range = [self.minMZ, self.maxMZ]
        self.currMaxY = self._getMaxIntensityInRange(x_range)
        if self.currMaxY:
            self.setYRange(0, self.currMaxY, update=False)
        self._plot_ladder_annotations()

    def _plot_peak_annotations(self):
        try:
            self.peak_annotation_list
        except (AttributeError, NameError):
            return 

        for item in self.peak_annotation_list: # item : PeakAnnoStruct
            self.plot([item.mz], [item.intensity], symbol=item.symbol,
                symbolBrush=pg.mkBrush(item.symbol_color), symbolSize=14)
            if item.text_label:
                label = pg.TextItem(text=item.text_label, color=(0,0,0), anchor=(0.5,1.5))
                self.addItem(label)
                label.setPos(item.mz, item.intensity)
        
    def _getMaxIntensityInRange(self, xrange):
        left = np.searchsorted(self._mzs, xrange[0], side='left')
        right = np.searchsorted(self._mzs, xrange[1], side='right')
        return np.amax(self._ints[left:right], initial = 1)        
        
    def _plot_spectrum(self):
        bargraph = pg.BarGraphItem(x=self._mzs, height=self._ints, width=0)
        self.addItem(bargraph)
        
    def _plot_ladder_annotations(self):
        try:
            self._ladder_visible
        except (AttributeError, NameError):
            return
        try:
            self.currMaxY
        except (AttributeError, NameError):
            self.currMaxY = self._getMaxIntensityInRange(self.getAxis('bottom').range) 

        ### why? np.amin(self._mzs), np.amax(self._mzs)
        xlimit = [self._mzs[0], self._mzs[-1]]
        for ladder_key, lastruct in self._ladder_visible.items():
            if ladder_key in self._ladder_anno_lines.keys(): # update    
                self._ladder_anno_lines[ladder_key][0].setData([xlimit[0], xlimit[1]],[self.currMaxY, self.currMaxY]) # horizontal line 
                cntr=0
                for x in lastruct.mz_list:
                    self._ladder_anno_lines[ladder_key][cntr+1].setData([x, x], [0, self.currMaxY])
                    self._ladder_anno_labels[ladder_key][cntr].setPos(x, self.currMaxY) # horizon line doesn't have label
                    cntr += 1
            else : # plot
                pen = pg.mkPen(lastruct.color, width=2, style=Qt.DotLine)
                self._ladder_anno_lines[ladder_key] = []
                self._ladder_anno_labels[ladder_key] = []

                self._ladder_anno_lines[ladder_key].append( # horizon line. index 0
                    self.plot([xlimit[0], xlimit[1]],[self.currMaxY, self.currMaxY], pen=pen))
                for x, txt_label in zip(lastruct.mz_list, lastruct.text_label_list):
                    self._ladder_anno_lines[ladder_key].append(self.plot([x, x], [0, self.currMaxY], pen=pen))
                    label = pg.TextItem(text=txt_label, color=lastruct.color, anchor=(1,-1))
                    label.setPos(x, self.currMaxY)
                    label.setParentItem(self._ladder_anno_lines[ladder_key][-1])
                    self._ladder_anno_labels[ladder_key].append(label)

    def _clear_annotations(self):
        self._ladder_visible = dict()
        self._ladder_anno_lines = dict()
        self._ladder_anno_labels = dict()

    def _clear_ladder_item(self, key):
        for p in self._ladder_anno_lines[key]:
            p.clear()         
        for l in self._ladder_anno_labels[key]:
            l.setPos(0,0)
        del self._ladder_anno_lines[key]
        del self._ladder_anno_labels[key]

    def _onMouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.sceneBoundingRect().contains(pos):
            mouse_point = self.getViewBox().mapSceneToView(pos)
            pixel_width = self.getViewBox().viewPixelSize()[0]
            left = np.searchsorted(self._mzs, mouse_point.x() - 4.0 * pixel_width, side='left')
            right = np.searchsorted(self._mzs, mouse_point.x() + 4.0 * pixel_width, side='right')
            if (left == right): # none found -> remove text
                if self.highlighted_peak_label != None:
                    self.highlighted_peak_label.setText("")
                return
            # get point in range with minimum squared distance
            dx = np.square(np.subtract(self._mzs[left:right], mouse_point.x()))
            dy = np.square(np.subtract(self._ints[left:right], mouse_point.y()))
            idx_max_int_in_range = np.argmin(np.add(dx, dy))
            x = self._mzs[left + idx_max_int_in_range]
            y = self._ints[left + idx_max_int_in_range]
            if self.highlighted_peak_label == None:
                self.highlighted_peak_label = pg.TextItem(text='{0:.3f}'.format(x), color=(100,100,100), anchor=(0.5,1))
                self.addItem(self.highlighted_peak_label)            
            self.highlighted_peak_label.setText('{0:.3f}'.format(x))
            self.highlighted_peak_label.setPos(x, y)
        else:
            # mouse moved out of visible area: remove highlighting item
            if self.highlighted_peak_label != None:
                self.highlighted_peak_label.setText("")

class ScanTableWidget(QWidget):
    
    scanClicked = pyqtSignal() # signal to connect SpectrumWidget
    header = ('MS level', 'Index', 'RT')
    def __init__(self, ms_experiment, *args):
       QWidget.__init__(self, *args)
       self.ms_experiment = ms_experiment

       self.table_model = ScanTableModel(self, self.ms_experiment, self.header)
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
       self.horizontalHeader.sectionClicked.connect(self.onHeaderClicked)
       
       layout = QVBoxLayout(self)
       layout.addWidget(self.table_view)
       self.setLayout(layout)
       
       # default : first row selected. in OpenMSWidgets
       
    def onRowSelected(self, index):
        if index.siblingAtColumn(1).data() == None: return # prevents crash if row gets filtered out
        self.curr_spec = self.ms_experiment.getSpectrum(index.siblingAtColumn(1).data())
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
    def __init__(self, parent, ms_experiment, header, *args):
       QAbstractTableModel.__init__(self, parent, *args)
       self.header = header
       
       # create array with MSSpectrum (only MS level=1)
       self.scanRows = self.getScanListAsArray(ms_experiment) # data type: list

    def getScanListAsArray(self, ms_experiment):
        scanArr = []
        for index, spec in enumerate(ms_experiment):
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
        self.mass_path = mass_path
        hbox = QVBoxLayout()
        self.setMaximumWidth(350)
        self.spectrum_widget = plot

        # data processing
        self.mlc = MassList(mass_path)
        self.total_masses = self.mlc.setMassStruct()
        self.masses = dict() # initialization

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
        self.spectrum_widget.setPeakAnnotations(self.getPeakAnnoStruct())
        self.spectrum_widget.setLadderAnnotations(self.getLadderAnnoStruct())
        # uncheck all checkboxes
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            if item.isCheckable():
                item.setCheckState(Qt.Unchecked)

        # reset parameter default value
        self.csMinLineEdit.setText('2')
        self.csMaxLineEdit.setText('100')

        self.spectrum_widget.redrawPlot()

    def setFeatureMapButton(self):
        self.fmButton = QPushButton()
        self.fmButton.setText('Draw feature map')
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
        self.paramButton.clicked.connect(self.redrawAnnotationsWithParam)
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

    def loadFeatureMapPlot(self):
        if not self.mlc.isFDresult:
            self.errorDlg = QMessageBox()
            self.errorDlg.setIcon(QMessageBox.Critical)
            self.errorDlg.setWindowTitle("ERROR")
            self.errorDlg.setText('Input mass file is not formatted as FLASHDeconv result file.')
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
        self.spectrum_widget.setPeakAnnotations(self.getPeakAnnoStruct())
        self.spectrum_widget.setLadderAnnotations(self.getLadderAnnoStruct())

    def getMassStructWithRT(self, scan_rt):
        new_dict = dict()
        for mass, mds in self.total_masses.items():
            if scan_rt >= mds.startRT and scan_rt <= mds.endRT:
                new_dict[mass] = mds
        return new_dict

    def redrawAnnotationsWithParam(self):
        minCs = self.csMinLineEdit.text()
        maxCs = self.csMaxLineEdit.text()
        
        if self.isError_redrawAnnotationsWithParam(minCs, maxCs):
            self.csMinLineEdit.setText('2')
            self.csMaxLineEdit.setText('100')
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
        qp.translate(10,10)
        qp.scale(20,20)
        qp.drawPath(Symbols[symbol])
        qp.end()

        return QIcon(px)

    def getPeakAnnoStruct(self):
        pStructList = []
        for mass, mass_strc in self.masses.items():
            theo_list = mass_strc.mz_theo_arr
            
            for theo in theo_list: # theo : [0] cs [1] iso mz list
                exp_p = self.findNearestPeakWithTheoPos(theo[1][0]) # Monoisotopic only
                if exp_p==None:
                    continue
                pStructList.append(PeakAnnoStruct(mz=exp_p.getMZ(), 
                    intensity=exp_p.getIntensity(), text_label='+'+str(theo[0]),
                    symbol=mass_strc.marker, symbol_color=mass_strc.color))

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

                for theo in theo_list: # theo : [0] cs [1] iso mz list
                    # plotting only theoretical mz valule within experimental mz range
                    if ( (theo[1][0] <= xlimit[0]) | (theo[1][-1] >= xlimit[1]) ):
                        continue

                    for index, mz in enumerate(theo[1]):
                        t_mz_list.append(mz)
                        txt_list.append('+%d[%d]' %(theo[0], index))
                lStructDict[mass] = LadderAnnoStruct(mz_list=np.array(t_mz_list),
                    text_label_list=np.array(txt_list) ,color=mass_strc.color)
            else:
                self.spectrum_widget.clearLadderAnnotation(mass)
        return lStructDict

    def findNearestPeakWithTheoPos(self, theo_mz, tol=-1):
        nearest_p = self.spectrum_widget.spec[self.spectrum_widget.spec.findNearest(theo_mz)]
        if tol == -1:
            tol = TOL * theo_mz # ppm
        if abs(theo_mz-nearest_p.getMZ()) > tol:
            return None;
        if nearest_p.getIntensity()==0:
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
                self.spectrum_widget.setLadderAnnotations(self.getLadderAnnoStruct())
                self.spectrum_widget.redrawLadderAnnotations()
        else:
            if checked:
                self._data_visible.append(str(mass))
                self.spectrum_widget.setLadderAnnotations(self.getLadderAnnoStruct())
                self.spectrum_widget.redrawLadderAnnotations()
    
    def addMassToListView(self):
        new_mass = self.massLineEdit.text()
        self.massLineEdit.clear()
        try:
            new_mass = float(new_mass)
        except:
            return
        new_mass_str = self.mlc.addNewMass(new_mass, self.cs_range)
        self.masses[new_mass] = new_mass_str

        # redraw
        self._updatePlot()
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
            self.controller.updateMassTableView(self.scan_widget.curr_spec.getRT())
        self.spectrum_widget.redrawPlot()

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
