import os
import sys
import pandas as pd
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QVBoxLayout, QCheckBox
sys.path.append(os.getcwd() + '/../controller')
from filehandler import FileHandler as fh


class OverallView(QWidget):

    def __init__(self, *args):
        QWidget.__init__(self, *args)

        buttonlayout = QVBoxLayout()
        layout = QHBoxLayout()

        buttons = QWidget()
        self.table = QTableWidget()

        # Buttons
        LoadBtn = QPushButton('Load')
        SaveBtn = QPushButton('Save')
        LabelBtn = QPushButton('Label')
        GroupBtn = QPushButton('Group')
        SearchBtn = QPushButton('Search')

        buttonlayout.addWidget(LoadBtn)
        buttonlayout.addWidget(SaveBtn)
        buttonlayout.addWidget(LabelBtn)
        buttonlayout.addWidget(GroupBtn)
        buttonlayout.addWidget(SearchBtn)

        buttons.setLayout(buttonlayout)

        buttons.resize(200, 690)

        # Buttonconnections
        LoadBtn.clicked.connect(self.loadBtnFn)

        # Table
        self.table.setRowCount(10)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['', 'Fraction_Group', 'Fraction', 'Filename',
                'Label', 'Sample', ''])

        # Fügt zu jeder Zeile einen Edit Button hinzu
        for index in range(self.table.rowCount()):
            editBtn = QPushButton('Edit')
            self.table.setCellWidget(index, 6, editBtn)

        # Fügt zu jeder Zeile eine Checkbox hinzu
        for index in range(self.table.rowCount()):
            CHBX = QCheckBox()
            self.table.setCellWidget(index, 0, CHBX)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        # setzte die Widgets ins gewünschte layout rein
        layout.addWidget(self.table)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.resize(1280, 720)

# Loadfunction
    def loadBtnFn(self):
        dlg = QFileDialog(self)
        filePath = dlg.getExistingDirectory()
        Files = fh.getFiles(self, filePath)
        delimiters = ["_"]
        preparedFiles = fh.tagfiles(self, Files, delimiters[0])
        rawTable = fh.createRawTable(self, preparedFiles, filePath)
        rowSize = len(rawTable.index)
        columSize = len(rawTable.columns)
        i = 0
        j = 0

        for i in range(rowSize):
            for j in range(columSize):
                if j == 2:
                    name = str(rawTable.iloc[i, j])[len(filePath):]
                    self.table.setItem(i, j+1, QTableWidgetItem(name))
                else:
                    self.table.setItem(i, j+1, QTableWidgetItem(rawTable.iloc[i, j]))

        # print(len(rawTable.columns))
        # print(len(rawTable.index))
        # print('Fraction_Group' + str(rawTable.iloc[1, 0]))
        # print('Fraction' + str(rawTable.iloc[1, 1]))
        # print('Filename' + name)
        # print('Label' + str(rawTable.iloc[1, 3]))
        # print('Sample' + str(rawTable.iloc[1, 4]))
        # print(rawTable)
