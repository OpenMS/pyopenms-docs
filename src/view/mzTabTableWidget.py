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
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "mzTabTableWidget"
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 500
        self.tableRows = 5

        self.PRTFull = []
        self.PSMFull = []

        self.PRTFiltered = []
        self.PSMFiltered = []

        self.selectedPRT = ""
        self.selectedPSM = ""

        self.tablePRTFull = QTableWidget()
        self.tablePSMFull = QTableWidget()
        self.vBoxFull = QVBoxLayout()

        self.tablePRTFiltered = QTableWidget()
        self.tablePSMFiltered = QTableWidget()
        self.vBoxFiltered = QVBoxLayout()

        self.outerVBox = QVBoxLayout()

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.parser('/home/taiki/Downloads/test.mzTab')

        self.initTables()
        self.createTable(self.tablePRTFull, self.PRTFull)
        self.createTable(self.tablePSMFull, self.PSMFull)

        self.tablePRTFull.itemDoubleClicked.connect(self.browsePRT)
        self.tablePSMFull.itemDoubleClicked.connect(self.browsePSM)

        self.vBoxFull.addWidget(self.tablePRTFull)
        self.vBoxFull.addWidget(self.tablePSMFull)

        self.vBoxFiltered.addWidget(self.tablePRTFiltered)
        self.vBoxFiltered.addWidget(self.tablePSMFiltered)

        self.outerVBox.addLayout(self.vBoxFull)
        self.outerVBox.addLayout(self.vBoxFiltered)

        self.setLayout(self.outerVBox)
        self.show()

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

    def createTable(self, table, content):
        """parameters: tableWidget to draw content in. Content to be drawn in list form"""
        """Setting count to zero empties the table. Then table is (re-)filled with specified content"""
        table.setRowCount(0)
        table.setRowCount(len(content))

        j = 0
        k = 0

        for item in content[1:]:
            while k < (len(content)):
                while j < (len(item)):
                    table.setItem(k, j, QTableWidgetItem(item[j]))
                    j += 1
                else:
                    k += 1
                    j = 0
                break

    def filterPRT(self, item):
        test = 0

    def filterPSM(self, item):
        test = 0

    def browsePRT(self, item):
        accession = self.PRTFull[item.row() + 1][0].split("|", 2)[1]
        webbrowser.open("https://www.uniprot.org/uniprot/" + accession)

    def browsePSM(self, item):
        accession = self.PSMFull[item.row() + 1][2].split("|", 2)[1]
        webbrowser.open("https://www.uniprot.org/uniprot/" + accession)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
