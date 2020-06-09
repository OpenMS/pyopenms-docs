import os
import sys
import pandas as pd
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QFileDialog, \
        QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, \
        QVBoxLayout, QCheckBox
sys.path.append(os.getcwd() + '/../controller')
from filehandler import FileHandler as fh
from TableModifier import TableModifier as Tm
sys.path.append(os.getcwd() + '/../model')
from tableDataFrame import TableDataFrame as Tdf


class OverallView(QWidget):

    def __init__(self, *args):
        QWidget.__init__(self, *args)

        buttonlayout = QVBoxLayout()
        layout = QHBoxLayout()
        self.tdf = Tdf
        buttons = QWidget()
        self.table = QTableWidget()
        self.df = pd.DataFrame()

        # Buttons
        Buttons = [QPushButton('Import'), QPushButton('Export'),
                   QPushButton('Load'), QPushButton('Save'),
                   QPushButton('Label'), QPushButton('Group'),
                   QPushButton('Search'), QPushButton('Load File')]

        for button in Buttons:
            buttonlayout.addWidget(button)

        buttons.setLayout(buttonlayout)

        buttons.resize(200, 690)

        # Buttonconnections
        Buttons[2].clicked.connect(self.loadBtnFn)
        Buttons[7].clicked.connect(self.loadFile)
        Buttons[0].clicked.connect(self.importBtn)
        Buttons[1].clicked.connect(self.exportBtn)

        # Table
        self.table.setRowCount(10)
        header = ['', 'Fraction_Group', 'Fraction',
                  'Spectra_Filepath', 'Label', 'Sample']
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)

        # Fügt zu jeder Zeile eine Checkbox hinzu
        for index in range(self.table.rowCount()):
            CHBX = QCheckBox()
            self.table.setCellWidget(index, 0, CHBX)

        header = self.table.horizontalHeader()

        for col in range(len(header)):
            if col != 3:
                header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
            else:
                header.setSectionResizeMode(col, QHeaderView.Stretch)

        # setzte die Widgets ins gewünschte layout rein
        layout.addWidget(self.table)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.resize(1280, 720)

    def initUI(self):
        """
        initializes Ui Elements
        """
    def setButtonLayout(self):
        """
        sets layout for buttons
        """
    def setTableLayout(self):
        """
        sets table layout
        """

    def drawTable(self, tabledf):
        """
        draws a table witha given dataframe and filepath
        """
        rowSize = len(tabledf.index)
        columSize = len(tabledf.columns)
        for i in range(rowSize):
            for j in range(columSize):
                if j == 2:
                    path = tabledf.iloc[i, j].split("/")
                    name = path[len(path)-1]
                    self.table.setItem(i, j+1, QTableWidgetItem(name))
                else:
                    self.table.setItem(
                        i, j+1, QTableWidgetItem(tabledf.iloc[i, j]))

    def importBtn(self):
        """
        import button handler
        """
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;tsv (*.tsv);; csv (*.csv)", options=options)

        df = fh.importTable(self, file)
        Tdf.setTable(self, df)
        self.drawTable(df)

    def exportBtn(self):
        """
        export button handler
        """
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;tsv (*.tsv);; csv (*.csv)", options=options)

        df = Tdf.getTable(self)

        temp = file.split("/")
        fileName = temp[len(temp)-1]
        ftype = fileName.split(".")[1]
        fh.exportTable(self, df, fileName, ftype)

    def loadBtnFn(self):
        """
        provides a dialog to get the path for a directory
        """
        dlg = QFileDialog(self)
        filePath = dlg.getExistingDirectory()
        Files = fh.getFiles(self, filePath)
        delimiters = ["_"]
        preparedFiles = fh.tagfiles(self, Files, delimiters[0])
        rawTable = fh.createRawTable(self, preparedFiles, filePath)
        self.drawTable(rawTable)
        Tdf.setTable(self, rawTable)

    def loadFile(self):
        """
        provides a filedialog to load an additional file to the dataframe
        """
        ftype = "*.mzML"
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;mzML Files (*.mzML)", options=options)

        cdf = Tdf.getTable(self)
        filelist = []
        filePath = file.rsplit("/", 1)[0]
        temp = file.split("/")
        fileName = temp[len(temp)-1]
        if file:
            # print(file)
            filelist.append(fileName)
            tagged_file = fh.tagfiles(self, filelist)
            df = fh.createRawTable(self, tagged_file, filePath)

            ndf = cdf.append(df)

            Tdf.setTable(self, ndf)
            self.drawTable(ndf)
        else:
            return False

        # print(len(rawTable.columns))
        # print(len(rawTable.index))
        # print('Fraction_Group' + str(rawTable.iloc[1, 0]))
        # print('Fraction' + str(rawTable.iloc[1, 1]))
        # print('Filename' + name)
        # print('Label' + str(rawTable.iloc[1, 3]))
        # print('Sample' + str(rawTable.iloc[1, 4]))
        # print(rawTable)
