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

sys.path.insert(0, '../view')
from SpectrumWidget import *

# structure for annotation (here for reference)
PeakAnnoStruct = namedtuple('PeakAnnoStruct', "mz intensity text_label \
                            symbol symbol_color")
LadderAnnoStruct = namedtuple('LadderAnnoStruct', "mz_list \
                            text_label_list color")

pg.setConfigOption('background', 'w') # white background
pg.setConfigOption('foreground', 'k') # black peaks

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
