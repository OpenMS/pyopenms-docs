""" 
mzTabTableWidget
----------------
This script allows the user to transfer information about proteins and psms from a mzTab file into two tables, 
one containing the proteins, the other one containing the psms.

By clicking on a row, the tables get updated regarding their listed proteins or psms.
Once you choose a protein/psm, the table displays only those psms/proteins that are linked to one another.

This tool is designed to accept mzTab files. It is required to save those files under '.../examples/data/' or 
change the path within the InitWindow.
"""
import sys
import webbrowser
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QPushButton, QFileDialog


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "mzTabTableWidget"
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 500
        self.tableRows = 5

        self.fileLoaded = False

        self.PRTFull = []
        self.PSMFull = []

        self.PRTFiltered = []
        self.PSMFiltered = []

        self.PRTColumn = [True]
        self.PSMColumn = [True]

        self.selectedPRT = ""
        self.selectedPSM = ""

        self.tablePRTFull = QTableWidget()
        self.tablePSMFull = QTableWidget()

        self.tablePRTFiltered = QTableWidget()
        self.tablePSMFiltered = QTableWidget()

        self.vBoxPRT = QVBoxLayout()
        self.vBoxPSM = QVBoxLayout()

        self.outerVBox = QVBoxLayout()

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.tablePRTFull.setHidden(True)
        self.tablePSMFull.setHidden(True)
        self.tablePRTFiltered.setHidden(True)
        self.tablePSMFiltered.setHidden(True)

        self.tablePRTFull.itemClicked.connect(self.PRTClicked)
        self.tablePRTFiltered.itemClicked.connect(self.PRTClicked)
        self.tablePSMFull.itemClicked.connect(self.PSMClicked)
        self.tablePSMFiltered.itemClicked.connect(self.PSMClicked)

        self.tablePRTFull.itemDoubleClicked.connect(self.browsePRT)
        self.tablePRTFiltered.itemDoubleClicked.connect(self.browsePRT)
        self.tablePSMFull.itemDoubleClicked.connect(self.browsePSM)
        self.tablePSMFiltered.itemDoubleClicked.connect(self.browsePSM)

        self.vBoxPRT.addWidget(self.tablePRTFull)
        self.vBoxPRT.addWidget(self.tablePRTFiltered)

        self.vBoxPSM.addWidget(self.tablePSMFull)
        self.vBoxPSM.addWidget(self.tablePSMFiltered)

        self.outerVBox.addLayout(self.vBoxPRT)
        self.outerVBox.addLayout(self.vBoxPSM)

        self.setLayout(self.outerVBox)
        self.show()

    def readFile(self, file):
        if self.fileLoaded:
            self.tablePRTFull.clear()
            self.tablePSMFull.clear()
            self.tablePSMFiltered.clear()
            self.tablePRTFiltered.clear()

            self.tablePRTFull.setRowCount(0)
            self.tablePSMFull.setRowCount(0)
            self.tablePSMFiltered.setRowCount(0)
            self.tablePRTFiltered.setRowCount(0)

            self.PRTFull.clear()
            self.PSMFull.clear()

            self.PRTFiltered.clear()
            self.PSMFiltered.clear()

            self.PRTColumn.clear()
            self.PSMColumn.clear()

            self.PRTColumn = [True]
            self.PSMColumn = [True]

        self.parser(file)

        self.PRTColumn *= len(self.PRTFull[1])
        self.PSMColumn *= len(self.PSMFull[1])

        self.initTables()
        self.createTable(self.tablePRTFull, self.PRTFull)
        self.createTable(self.tablePSMFull, self.PSMFull)

        self.hidePRTColumns()
        self.hidePSMColumns()

        self.tablePRTFull.setHidden(False)
        self.tablePSMFull.setHidden(False)

        self.fileLoaded = True


    def parser(self, file):
        """parses the given mzTab file and saves PRT and PSM information
        Parameters
        ----------
        file : str
            The file path of the mzTab file
        """

        with open(file) as inp:
            for line in inp:
                if line.startswith("PRH"):
                    self.PRTFull.append(line.strip().split('\t'))
                elif line.startswith("PRT") and not line.endswith("protein_details\n"):
                    self.PRTFull.append(line.strip().split('\t'))
                elif line.startswith("PSH") or line.startswith("PSM"):
                    self.PSMFull.append(line.strip().split('\t'))

        for item in self.PRTFull:
            item.pop(0)

        for item in self.PSMFull:
            item.pop(0)



    def initTables(self):
        """draws protein and psm tables with headers"""

        self.tablePRTFull.setRowCount(len(self.PRTFull))
        self.tablePRTFull.setColumnCount(len(self.PRTFull[0]))
        self.tablePRTFull.setHorizontalHeaderLabels(self.PRTFull[0])

        self.tablePSMFull.setRowCount(len(self.PSMFull))
        self.tablePSMFull.setColumnCount(len(self.PSMFull[0]))
        self.tablePSMFull.setHorizontalHeaderLabels(self.PSMFull[0])

        self.tablePRTFiltered.setRowCount(0)
        self.tablePRTFiltered.setColumnCount(len(self.PRTFull[0]))
        self.tablePRTFiltered.setHorizontalHeaderLabels(self.PRTFull[0])

        self.tablePSMFiltered.setRowCount(0)
        self.tablePSMFiltered.setColumnCount(len(self.PSMFull[0]))
        self.tablePSMFiltered.setHorizontalHeaderLabels(self.PSMFull[0])

        """removes now unnecessary header information from content lists """
        self.PRTFull.pop(0)
        self.PSMFull.pop(0)

    def createTable(self, table, content):
        """parameters: tableWidget to draw content in. Content to be drawn in list form"""
        """Setting count to zero empties the table. Then table is (re-)filled with specified content"""
        table.setRowCount(0)
        table.setRowCount(len(content))

        j = 0
        k = 0

        for item in content[0:]:
            while k < (len(content)):
                while j < (len(item)):
                    table.setItem(k, j, QTableWidgetItem(item[j]))
                    j += 1
                else:
                    k += 1
                    j = 0
                break

        self.tablePRTFull.resizeColumnsToContents()  # resize columns
        self.tablePSMFull.resizeColumnsToContents()  # resize columns
        self.tablePRTFiltered.resizeColumnsToContents()  # resize columns
        self.tablePSMFiltered.resizeColumnsToContents()  # resize columns

    def hidePRTColumns(self):
        """hides constant columns in PRT table by default by checking if every value equals"""
        i = 0
        j = 0
        k = 0

        while i < len(self.PRTFull) - 1:
            while j < len(self.PRTFull[i]):
                if self.PRTColumn[j]:
                    if self.PRTFull[i][j] != self.PRTFull[i + 1][j]:
                        self.PRTColumn[j] = False
                j += 1
            i += 1

        while k < len(self.PRTColumn):
            if self.PRTColumn[k]:
                self.tablePRTFull.setColumnHidden(k, True)
                self.tablePRTFiltered.setColumnHidden(k, True)
            k += 1

    def hidePSMColumns(self):
        """hides constant columns in PSM table by default by checking if every value equals"""
        i = 0
        j = 0
        k = 0

        while i < len(self.PSMFull) - 1:
            while j < len(self.PSMFull[i]):
                if self.PSMColumn[j]:
                    if self.PSMFull[i][j] != self.PSMFull[i + 1][j]:
                        self.PSMColumn[j] = False
                j += 1
            i += 1

        while k < len(self.PSMColumn):
            if self.PSMColumn[k]:
                self.tablePSMFull.setColumnHidden(k, True)
                self.tablePSMFiltered.setColumnHidden(k, True)
            k += 1

    def PRTClicked(self, item):

        if self.tablePRTFull.isHidden():
            relevantContent = self.PRTFiltered
        else:
            relevantContent = self.PRTFull

        accession = relevantContent[item.row()][0]

        if self.selectedPSM == accession:
            self.unfilterPSM()
        else:
            self.filterPSM(accession)

    def PSMClicked(self, item):

        if self.tablePSMFull.isHidden():
            relevantContent = self.PSMFiltered
        else:
            relevantContent = self.PSMFull

        accession = relevantContent[item.row()][2]

        if self.selectedPRT == accession:
            self.unfilterPRT()
        else:
            self.filterPRT(accession)

    def filterPRT(self, accession):
        self.tablePRTFiltered.setHidden(False)
        self.tablePRTFull.setHidden(True)

        self.selectedPRT = accession

        self.PRTFiltered = [p for p in self.PRTFull if p[0] == self.selectedPRT]
        self.createTable(self.tablePRTFiltered, self.PRTFiltered)

    def filterPSM(self, accession):
        self.tablePSMFiltered.setHidden(False)
        self.tablePSMFull.setHidden(True)

        self.selectedPSM = accession

        self.PSMFiltered = [p for p in self.PSMFull if p[2] == self.selectedPSM]
        self.createTable(self.tablePSMFiltered, self.PSMFiltered)

    def unfilterPRT(self):
        self.tablePRTFiltered.setHidden(True)
        self.tablePRTFull.setHidden(False)
        self.selectedPRT = ""
        self.PRTFiltered = []

    def unfilterPSM(self):
        self.tablePSMFiltered.setHidden(True)
        self.tablePSMFull.setHidden(False)
        self.selectedPSM = ""
        self.PSMFiltered = []

    def browsePRT(self, item):
        if self.tablePRTFull.isHidden():
            accession = self.PRTFiltered[item.row()][0].split("|", 2)[1]
        else:
            accession = self.PRTFull[item.row()][0].split("|", 2)[1]

        webbrowser.open("https://www.uniprot.org/uniprot/" + accession)

    def browsePSM(self, item):
        if self.tablePSMFull.isHidden():
            accession = self.PSMFiltered[item.row()][2].split("|", 2)[1]
        else:
            accession = self.PSMFull[item.row()][2].split("|", 2)[1]

        webbrowser.open("https://www.uniprot.org/uniprot/" + accession)

