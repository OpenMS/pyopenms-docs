from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QAction,
    QTableView,
    QMenu,
    QAbstractItemView,
    QItemDelegate,
)
from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel,
    pyqtSignal,
    QItemSelectionModel,
    QSortFilterProxyModel,
    QSignalMapper,
    QPoint,
    QRegExp,
    QModelIndex,
)


class RTUnitDelegate(QItemDelegate):
    """
    Displays the minute values of the RT besides the RT values given in seconds. Through the delegate the RT values in
    the table are not changed, only difference is the display of the data in table_view. s

    """

    def __init__(self, parent, *args):
        super(RTUnitDelegate, self).__init__(parent, *args)

    def paint(self, painter, option, index):
        painter.save()
        painter.setPen(QPen(Qt.black))
        if index.isValid():
            rt_min = round(index.siblingAtColumn(2).data() * 1.0 / 60, 3)
            text = (
                "  "
                + str(round(index.siblingAtColumn(2).data(), 3))
                + "\t ["
                + str(rt_min)
                + " Min"
                + "]"
            )
            painter.setRenderHint(QPainter.Antialiasing)
            # adjust text into cell
            cell = option.rect
            cell.adjust(0, 5, 0, 5)
            painter.drawText(cell, Qt.AlignLeft, text)

            painter.restore()


class ScanTableWidget(QWidget):
    """
    Used for displaying information in a table.

    ===============================  =============================================================================
    **Signals:**
    sigScanClicked                   Emitted when the user has clicked on a row of the table and returns the
                                     current index. This index contains information about the current rows column
                                     data.

    ===============================  =============================================================================
    """

    sigScanClicked = pyqtSignal(QModelIndex, name="scanClicked")

    header = [
        "MS level",
        "Index",
        "RT (min)",
        "precursor m/z",
        "charge",
        "ID",
        "PeptideSeq",
        "PeptideIons",
    ]

    def __init__(self, ms_experiment, *args):
        QWidget.__init__(self, *args)
        self.ms_experiment = ms_experiment

        self.table_model = ScanTableModel(
            self, self.ms_experiment, self.header)
        self.table_view = QTableView()

        # register a proxy class for filering and sorting the scan table
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.table_model)

        self.table_view.sortByColumn(1, Qt.AscendingOrder)

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
        self.table_view.selectionModel().currentChanged.connect(
            self.onCurrentChanged
        )  # keyboard moves to new row
        self.horizontalHeader.sectionClicked.connect(self.onHeaderClicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

        # hide column 7 with the PepIon data, intern information usage
        self.table_view.setColumnHidden(7, True)

        # Add rt in minutes for better TIC interaction
        self.table_view.setItemDelegateForColumn(2, RTUnitDelegate(self))
        self.table_view.setColumnWidth(2, 160)

        # default : first row selected. in OpenMSWidgets

    def onRowSelected(self, index):
        if index.siblingAtColumn(1).data() == None:
            return  # prevents crash if row gets filtered out
        self.curr_spec = self.ms_experiment.getSpectrum(
            index.siblingAtColumn(1).data())
        self.scanClicked.emit(index)

    def onCurrentChanged(self, new_index, old_index):
        self.onRowSelected(new_index)

    def onHeaderClicked(self, logicalIndex):
        if logicalIndex != 0:
            return  # allow filter on first column only for now

        self.logicalIndex = logicalIndex
        self.menuValues = QMenu(self)
        self.signalMapper = QSignalMapper(self)

        # get unique values from (unfiltered) model
        valuesUnique = set(
            [
                self.table_model.index(row, self.logicalIndex).data()
                for row in range(
                    self.table_model.rowCount(
                        self.table_model.index(-1, self.logicalIndex)
                    )
                )
            ]
        )

        if len(valuesUnique) == 1:
            return  # no need to select anything

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
        filterString = QRegExp("", Qt.CaseInsensitive, QRegExp.RegExp)

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    def onSignalMapper(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        filterString = QRegExp(
            stringAction, Qt.CaseSensitive, QRegExp.FixedString)

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)


class ScanTableModel(QAbstractTableModel):
    """
        TODO: directly read model data from MSExperiment to remove copies
    """

    def __init__(self, parent, ms_experiment, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.header = header

        # create array with MSSpectrum
        self.scanRows = self.getScanListAsArray(
            ms_experiment)  # data type: list

    def getScanListAsArray(self, ms_experiment):
        scanArr = []
        for index, spec in enumerate(ms_experiment):
            MSlevel = "MS" + str(spec.getMSLevel())
            RT = spec.getRT()
            prec_mz = "-"
            charge = "-"
            native_id = spec.getNativeID()
            if len(spec.getPrecursors()) == 1:
                prec_mz = spec.getPrecursors()[0].getMZ()
                charge = spec.getPrecursors()[0].getCharge()
            PeptideSeq = "-"
            PeptideIons = "-"

            scanArr.append(
                [
                    MSlevel,
                    index,
                    RT,
                    prec_mz,
                    charge,
                    native_id,
                    PeptideSeq,
                    PeptideIons,
                ]
            )
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
        if index.isValid() and role == Qt.DisplayRole:
            self.scanRows[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, {Qt.DisplayRole, Qt.EditRole})
            return value
        return None

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
