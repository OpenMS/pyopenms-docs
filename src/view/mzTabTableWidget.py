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

        self.PRT = []
        self.PSM = []

        self.drawPRT = []
        self.drawPSM = []


        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.parser('/home/taiki/Downloads/test.mzTab')

        self.drawPRT = self.PRT
        self.drawPSM = self.PSM

        self.tablePRTFull = QTableWidget()
        self.tablePSMFull = QTableWidget()

        self.tablePRTFiltered = QTableWidget()
        self.tablePSMFiltered = QTableWidget()

        self.drawTables()
        self.createProtTableFull()
        self.createPSMTableFull()

        self.tablePRTFull.itemClicked.connect(self.filterPRT)
        self.tablePSMFull.itemClicked.connect(self.filterPSM)

        self.tablePRTFull.itemDoubleClicked.connect(self.browsePRT)
        self.tablePSMFull.itemDoubleClicked.connect(self.browsePSM)

        self.vboxFull = QVBoxLayout()
        self.vboxFull.addWidget(self.tablePRTFull)
        self.vboxFull.addWidget(self.tablePSMFull)

        self.vboxFiltered = QVBoxLayout()
        self.vboxFiltered.addWidget(self.tablePRTFiltered)
        self.vboxFiltered.addWidget(self.tablePSMFiltered)

        self.outerVbox = QVBoxLayout()
        self.outerVbox.addLayout(self.vboxFull)
        self.outerVbox.addLayout(self.vboxFiltered)

        self.setLayout(self.outerVbox)
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
                    self.PRT.append(line.strip().split('\t'))
                elif line.startswith("PRT") and not line.endswith("protein_details\n"):
                    self.PRT.append(line.strip().split('\t'))
                elif line.startswith("PSH") or line.startswith("PSM"):
                    self.PSM.append(line.strip().split('\t'))

        for item in self.PRT:
            item.pop(0)

        for item in self.PSM:
            item.pop(0)

    def drawTables(self):
        """draws protein and psm table with headers"""

        self.tablePRTFull.setRowCount(len(self.drawPRT))
        self.tablePRTFull.setColumnCount(len(self.drawPRT[0]))
        self.tablePRTFull.setHorizontalHeaderLabels(self.drawPRT[0])

        self.tablePSMFull.setRowCount(len(self.drawPSM))
        self.tablePSMFull.setColumnCount(len(self.drawPSM[0]))
        self.tablePSMFull.setHorizontalHeaderLabels(self.drawPSM[0])

        self.tablePRTFiltered.setRowCount(0)
        self.tablePRTFiltered.setColumnCount(len(self.drawPRT[0]))
        self.tablePRTFiltered.setHorizontalHeaderLabels(self.drawPRT[0])

        self.tablePSMFiltered.setRowCount(0)
        self.tablePSMFiltered.setColumnCount(len(self.drawPSM[0]))
        self.tablePSMFiltered.setHorizontalHeaderLabels(self.drawPSM[0])
        
    def createProtTableFull(self):
        """updates protein table by setting table items and changing number of rows"""
        self.tablePRTFull.setRowCount(len(self.PRT))

        j = 0
        k = 0

        for item in self.drawPRT[1:]:
            while k < (len(self.drawPRT)):
                while j < (len(item)):
                    self.tablePRTFull.setItem(k, j, QTableWidgetItem(item[j]))
                    j += 1
                else:
                    k += 1
                    j = 0
                break

    def createPSMTableFull(self):
        """updates psm table by setting table items and changing number of rows"""
        self.tablePSMFull.setRowCount(len(self.drawPSM))

        m = 0
        n = 0

        for item in self.drawPSM[1:]:
            while n < (len(self.drawPSM)):
                while m < (len(item)):
                    self.tablePSMFull.setItem(n, m, QTableWidgetItem(item[m]))
                    m += 1
                else:
                    n += 1
                    m = 0
                break

    def filterPRT(self, item):
        test = 0

    def filterPSM(self, item):
        test = 0

    def browsePRT(self, item):
        accession = self.PRT[item.row()+1][0].split("|", 2)[1]
        webbrowser.open("https://www.uniprot.org/uniprot/" + accession)

    def browsePSM(self, item):
        accession = self.PSM[item.row()+1][2].split("|", 2)[1]
        webbrowser.open("https://www.uniprot.org/uniprot/" + accession)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
