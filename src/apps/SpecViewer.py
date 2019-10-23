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

#import pyopenms.Constants
# define Constant locally until bug in pyOpenMS is fixed
PROTON_MASS_U = 1.0072764667710
C13C12_MASSDIFF_U = 1.0033548378

# structure for annotation (here for reference)
PeakAnnoStruct = namedtuple('PeakAnnoStruct', "mz intensity text_label \
                            symbol symbol_color")
LadderAnnoStruct = namedtuple('LadderAnnoStruct', "mz_list \
                            text_label_list color")

pg.setConfigOption('background', 'w') # white background
pg.setConfigOption('foreground', 'k') # black peaks

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
        self.setOpenMSWidget()
        
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
