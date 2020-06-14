""" 
mzTabTableWidget
----------------
This script allows the user to transfer information about proteins and psms from a mzTab file into two tables, 
one containing the proteins, the other one containing the psms.

By clicking on a row, the tables get updated regarding their listed proteins or psms. 
Once you choose a protein/psm, the table displays only those psms/proteins that are linked to one another.

This tool is designed to accept mzTab files. It is required to save those files under '.../examples/data/' or change the path within the InitWindow.
"""

import sys
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

        self.PRT = []
        self.PSM = []

        self.drawPSM = []
        self.drawPRT = [] 

        self.selected = ""

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.parser('../examples/data/iPRG2015.mzTab')

        self.drawPSM = self.PSM
        self.drawPRT = self.PRT 

        self.tableWidget1 = QTableWidget()
        self.tableWidget2 = QTableWidget()
        self.drawTables()
        self.createProtTable()
        self.createPSMTable()

        self.tableWidget1.itemClicked.connect(self.filterProteins)
        self.tableWidget2.itemClicked.connect(self.filterPSMs) 

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tableWidget1)
        self.vbox.addWidget(self.tableWidget2)
        self.setLayout(self.vbox)
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

        self.tableWidget2.setRowCount(len(self.drawPSM))
        self.tableWidget2.setColumnCount(len(self.drawPSM[0]))
        self.tableWidget2.setHorizontalHeaderLabels(self.drawPSM[0])

        self.tableWidget1.setRowCount(len(self.drawPRT))
        self.tableWidget1.setColumnCount(len(self.drawPRT[0]))
        self.tableWidget1.setHorizontalHeaderLabels(self.drawPRT[0])

    def createProtTable(self):
            """updates protein table by setting table items and changing number of rows"""
        self.tableWidget1.setRowCount(len(self.drawPRT))
        
        j = 0
        k = 0
                        
        for item in self.drawPRT[1:]:
            while k < (len(self.drawPRT)):
                while j < (len(item)):
                 self.tableWidget1.setItem(k,j,QTableWidgetItem(item[j]))
                 j+=1
                else:
                    k+=1
                    j=0
                break       
        
    def createPSMTable(self):
            """updates psm table by setting table items and changing number of rows"""
        self.tableWidget2.setRowCount(len(self.drawPSM))
        
        m = 0
        n = 0
        
        for item in self.drawPSM[1:]:
            while n < (len(self.drawPSM)):
                while m < (len(item)):
                 self.tableWidget2.setItem(n,m,QTableWidgetItem(item[m]))
                 m+=1
                else:
                    n+=1
                    m=0
                break

    def filterProteins(self, item):
        self.selected = self.PRT[item.row()][0]
        print(self.selected)
        self.drawPSM = [p for p in self.PSM if p[2] == self.selected]
        self.createPSMTable()
            
    def filterPSMs(self, item):
        self.selected = self.PSM[item.row()][2]
        print(self.selected)
        self.drawPRT = [f for f in self.PRT if f[0] in self.selected]
        self.createProtTable()

            
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
