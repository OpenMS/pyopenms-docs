import os
import sys
import glob
from PyQt5.QtWidgets import QWidget, QTableWidget, \
    QTableWidgetItem, QVBoxLayout, QHeaderView
sys.path.append(os.getcwd()+'/../view')
from SpecViewer import Specviewer  # noqa E402


class MultipleSpecView(QWidget):
    """
    Displays the SpecviewerWidget and additionally a
    table containing all files from working dir
    """

    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.table = QTableWidget()
        self.sview = Specviewer()
        self.table.setRowCount(0)
        self.table.setSortingEnabled(True)
        self.table.setColumnCount(1)
        self.header = ['Filename']
        self.table.setHorizontalHeaderLabels(self.header)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.selectionModel().selectionChanged.connect(self.loadmzML)

        layout = QVBoxLayout()
        layout.addWidget(self.sview, 10)
        layout.addWidget(self.table, 4)

        self.setLayout(layout)
        self.resize(1280, 720)

    def fillTable(self, projectdir: str):
        """
        Uses the project directory to access all mzML files
        Loads all mzML files in the table
        """
        directory = projectdir
        os.chdir(directory)
        files = glob.glob('*.mzML')
        numfiles = len(files)
        self.table.setRowCount(numfiles)
        if numfiles > 0:
            for file, row in zip(files, range(numfiles)):
                self.table.setItem(row, 0, QTableWidgetItem(file))

    def loadmzML(self):
        """
        By selection of a mzML file the specviewer updates his file
        """
        selected = self.table.selectedItems()[0]
        selectedFile = selected.text()
        self.sview.setScanBrowserWidget()
        self.sview.scanbrowser.loadFile(selectedFile)
