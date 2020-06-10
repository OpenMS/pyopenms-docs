import os
import sys
import pandas as pd
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QFileDialog, \
        QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, \
        QVBoxLayout, QCheckBox, QInputDialog
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
        self.tm = Tm()
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
        Buttons[0].clicked.connect(self.importBtn)
        Buttons[1].clicked.connect(self.exportBtn)
        Buttons[2].clicked.connect(self.loadBtnFn)
        Buttons[5].clicked.connect(self.GroupBtn)
        Buttons[7].clicked.connect(self.loadFile)

        # Table
        self.table.setRowCount(10)
        self.header = ['Fraction_Group', 'Fraction',
                       'Spectra_Filepath', 'Label', 'Sample']
        self.table.setColumnCount(len(self.header))
        self.table.setHorizontalHeaderLabels(self.header)

        """
        # Fügt zu jeder Zeile eine Checkbox hinzu
        for index in range(self.table.rowCount()):
            CHBX = QCheckBox()
            self.table.setCellWidget(index, 0, CHBX)
        """

        self.header = self.table.horizontalHeader()

        for col in range(len(self.header)):
            if col != 2:
                self.header.setSectionResizeMode(col,
                                                 QHeaderView.ResizeToContents)
            else:
                self.header.setSectionResizeMode(col, QHeaderView.Stretch)

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

    def drawTable(self):
        """
        draws a table with the dataframe table model in tableDataFrame
        """
        tabledf = Tdf.getTable(self)
        rowcount = len(tabledf.index)
        colcount = len(tabledf.columns)
        for r in range(rowcount):
            row = tabledf.index[r]
            for c in range(colcount):
                col = tabledf.columns[c]
                if col == 'Spectra_Filepath':
                    path = tabledf.at[row, col].split("/")
                    name = path[len(path)-1]
                    self.table.setItem(r, c, QTableWidgetItem(name))
                else:
                    item = str(tabledf.at[row, col])
                    self.table.setItem(r, c, QTableWidgetItem(item))

    def importBtn(self):
        """
        import button handler
        """
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;tsv (*.tsv);; csv (*.csv)", options=options)
        if file:
            df = fh.importTable(self, file)
            Tdf.setTable(self, df)
            self.drawTable()

    def exportBtn(self):
        """
        export button handler
        """
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;tsv (*.tsv);; csv (*.csv)", options=options)
        if file:
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
        if filePath != '':
            Files = fh.getFiles(self, filePath)
            delimiters = ["_"]
            preparedFiles = fh.tagfiles(self, Files, delimiters[0])
            rawTable = fh.createRawTable(self, preparedFiles, filePath)
            Tdf.setTable(self, rawTable)
            self.drawTable()

    def loadFile(self):
        """
        provides a filedialog to load an additional file to the dataframe
        """
        ftype = "*.mzML"
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;mzML Files (*.mzML)", options=options)
        if file:
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
                self.drawTable()
            else:
                return False

    def GroupBtn(self):
        groupin, ok = QInputDialog.getInt(self, "Group Number", "Enter Integer Groupnumber")

        if ok:
            groupnum = groupin
            selindexes = self.table.selectionModel().selectedRows()
            selrows = []
            df = Tdf.getTable(self)
            for index in sorted(selindexes):
                row = index.row()
                tempfn = df.iloc[row, 2].split("/")  # static header
                filename = tempfn[len(tempfn)-1]
                selrows.append(filename)
            Tm.modifyGroup(self, selrows, groupnum)
            self.drawTable()

        # print(len(rawTable.columns))
        # print(len(rawTable.index))
        # print('Fraction_Group' + str(rawTable.iloc[1, 0]))
        # print('Fraction' + str(rawTable.iloc[1, 1]))
        # print('Filename' + name)
        # print('Label' + str(rawTable.iloc[1, 3]))
        # print('Sample' + str(rawTable.iloc[1, 4]))
        # print(rawTable)
