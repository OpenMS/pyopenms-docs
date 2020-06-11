import os
import sys
import pandas as pd
import math
from PyQt5 import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QFileDialog, \
        QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, \
        QVBoxLayout, QCheckBox, QInputDialog, QLineEdit, QMessageBox
sys.path.append(os.getcwd() + '/../controller')
from filehandler import FileHandler as fh
from TableModifier import TableModifier as Tm
sys.path.append(os.getcwd() + '/../model')
from tableDataFrame import TableDataFrame as Tdf


class OverallView(QWidget):

    def __init__(self, *args):
        QWidget.__init__(self, *args)

        buttonlayout = QHBoxLayout()
        layout = QVBoxLayout()
        self.tdf = Tdf
        self.tm = Tm()
        buttons = QWidget()
        self.table = QTableWidget()
        self.df = pd.DataFrame()
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.setFixedWidth(400)
        self.textbox.setFixedHeight(20)

        # Buttons
        Buttons = [QPushButton('Import'), QPushButton('Export'),
                   QPushButton('Load'), QPushButton('Fraction'),
                   QPushButton('Label'), QPushButton('Group'),
                   QPushButton('Remove File'), QPushButton('Add File'),
                   QPushButton('Search')]

        for button in Buttons:
            buttonlayout.addWidget(button)

        buttons.setLayout(buttonlayout)
        buttonlayout.addWidget(self.textbox)

        # Buttonconnections
        Buttons[0].clicked.connect(self.importBtn)
        Buttons[1].clicked.connect(self.exportBtn)
        Buttons[2].clicked.connect(self.loadBtnFn)
        Buttons[3].clicked.connect(self.FractionBtn)
        Buttons[4].clicked.connect(self.LabelBtn)
        Buttons[5].clicked.connect(self.GroupBtn)
        Buttons[7].clicked.connect(self.loadFile)

        """
        Disabled buttons until function are added
        """
        Buttons[6].setEnabled(False)
        Buttons[8].setEnabled(False)

        # Table
        self.table.setRowCount(0)
        self.header = ['Fraction Group', 'Fraction',
                       'Spectra Filepath', 'Label', 'Sample']
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
        layout.addWidget(buttons)
        layout.addWidget(self.table)

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
        print(tabledf)
        rowcount = len(tabledf.index)
        colcount = len(tabledf.columns)
        self.table.setRowCount(rowcount)
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

                ndf = cdf.append(df, ignore_index=True)

                Tdf.setTable(self, ndf)
                self.drawTable()
            else:
                return False

    def getSelRows(self):
        selindexes = self.table.selectionModel().selectedRows()
        selrows = []
        for index in sorted(selindexes):
            row = index.row()
            selrows.append(row)
        return selrows

    def GroupBtn(self):
        """
        Enables the user to change the group of selected rows to a given
        number.
        """
        selrows = self.getSelRows()

        groupnum, ok = QInputDialog.getInt(self,
                                           "Group Number",
                                           "Enter Integer Groupnumber")

        if ok:
            Tm.modifyGroup(self, selrows, groupnum)
            self.drawTable()

    def FractionBtn(self):
        """
        Enables the user to change the Fraction of selected rows to a given
        number or give a range.
        """
        selrows = self.getSelRows()

        fracmin, ok = QInputDialog.getInt(self,
                                          "Fraction",
                                          "Enter minimal Fractionnumber " +
                                          "or single Fractionnumber")
        if ok:
            fracmax, ok = QInputDialog.getInt(self,
                                              "Fraction",
                                              "Enter maximal Fractionnumber " +
                                              "or 0 for single Fractionnumber")
            if ok:
                if fracmax != 0:
                    if fracmax > fracmin:
                        rep = QMessageBox.question(self, "Fraction Group?",
                                                   "Do you want to infer a " +
                                                   "Fraction Group from the " +
                                                   "given range?",
                                                   (QMessageBox.Yes |
                                                    QMessageBox.No),
                                                   QMessageBox.No)
                        if rep == QMessageBox.Yes:
                            Tm.modifyFraction(self, selrows, fracmin, fracmax)
                            fractions = fracmax-fracmin + 1
                            numgroups = math.ceil(len(selrows)/fractions)
                            splicelist = [0]
                            for g in range(1, numgroups+1):
                                splicelist.append(g*fractions)
                            splicelist.append(len(selrows))
                            for group in range(1, numgroups+1):
                                indexa = splicelist[group-1]
                                indexb = splicelist[group]
                                subrows = selrows[indexa:indexb]
                                Tm.modifyGroup(self, subrows, group)
                        else:
                            Tm.modifyFraction(self, selrows, fracmin, fracmax)
                    elif fracmax == fracmin:
                        Tm.modifyFraction(self, selrows, fracmin)
                    else:
                        QMessageBox.warning(self, "Error", "Please use" +
                                            "a higher integer" +
                                            "number for the maximum" +
                                            "fractionnumber.")
                else:
                    Tm.modifyFraction(self, selrows, fracmin)
                self.drawTable()

    def LabelBtn(self):
        """
        Let the user choose the number of labels for the selected rows, it will
        automatically count the labels for the copied rows and also links
        the sample with the label. Gives an option to continue samplecount
        over fraction groups.
        """
        selrows = self.getSelRows()

        labelnum, ok = QInputDialog.getInt(self, "Label",
                                           "Please specify the multiplicity" +
                                           "of the selected rows")
        if ok:
            rep = QMessageBox.question(self, "Continuous Sample",
                                       "Does the samplenumber" +
                                       "continue over multiple" +
                                       "fraction groups?",
                                       (QMessageBox.Yes |
                                        QMessageBox.No),
                                       QMessageBox.No)
            if rep == QMessageBox.Yes:
                Tm.modifyLabelSample(self, selrows, labelnum, True)
            else:
                Tm.modifyLabelSample(self, selrows, labelnum, False)
            self.drawTable()

# print(len(rawTable.columns))
# print(len(rawTable.index))
# print('Fraction_Group' + str(rawTable.iloc[1, 0]))
# print('Fraction' + str(rawTable.iloc[1, 1]))
# print('Filename' + name)
# print('Label' + str(rawTable.iloc[1, 3]))
# print('Sample' + str(rawTable.iloc[1, 4]))
# print(rawTable)
