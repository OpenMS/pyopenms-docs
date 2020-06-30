import os
import sys
import timeit
import pandas as pd
import math
from PyQt5 import Qt
from PyQt5.QtCore import QPersistentModelIndex
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QFileDialog, \
        QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, \
        QVBoxLayout, QGridLayout, QInputDialog, QLineEdit, QMessageBox, \
        QAbstractItemView
sys.path.append(os.getcwd() + '/../controller')
from filehandler import FileHandler as fh
sys.path.append(os.getcwd() + '/../model')
from tableDataFrame import TableDataFrame as Tdf


class mzMLTableView(QWidget):
    """
    Main Widget of the TableEditor app
    """
    def __init__(self, *args):
        # set variable self.testForTime to True to see all Runtimes
        self.testForTime = False
        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of overall Initiation : ", starttime)

        QWidget.__init__(self, *args)

        self.df = pd.DataFrame()
        self.tdf = Tdf
        self.drawtableactive = False

        self.initTable()
        self.initButtons()
        self.changeListener()

        """
        Layout for the entire View
        """
        layout = QVBoxLayout()
        layout.addWidget(self.buttons)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.resize(1280, 720)

        if self.testForTime:
            rt = timeit.default_timer() - starttime
            print("Runtime of overall Initiation was : ", rt)

    def initTable(self):
        """
        initializes Table
        """
        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of initTable : ", starttime)

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.header = ['Group', 'Fraction',
                       'Spectra Filepath', 'Label', 'Sample']
        self.table.setColumnCount(len(self.header))
        self.table.setHorizontalHeaderLabels(self.header)
        self.header = self.table.horizontalHeader()

        for col in range(len(self.header)):
            if col != 2:
                self.header.setSectionResizeMode(col,
                                                 QHeaderView.ResizeToContents)
            else:
                self.header.setSectionResizeMode(col, QHeaderView.Stretch)

        if self.testForTime:
            rt = timeit.default_timer() - starttime
            print("Runtime of initTable : ", rt)

    def initButtons(self):
        """
        initializes Buttons
        """
        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of initButtons : ", starttime)

        self.buttons = QWidget()
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.setFixedHeight(20)

        Buttons = [QPushButton('Load Project'), QPushButton('Load Table'),
                   QPushButton('Save Table'), QPushButton('Add File'),
                   QPushButton('Remove File'), QPushButton('Group'),
                   QPushButton('Fraction'), QPushButton('Label'),
                   QPushButton('Select All'), QPushButton('Search')]

        # Buttonlayout
        buttonlayout = QHBoxLayout()
        for button in Buttons:
            buttonlayout.addWidget(button)

        buttonlayout.addWidget(self.textbox)
        self.buttons.setLayout(buttonlayout)

        # Connections for Buttons and their apropriate functions
        Buttons[0].clicked.connect(self.loadBtnFn)
        Buttons[1].clicked.connect(self.importBtn)
        Buttons[2].clicked.connect(self.exportBtn)
        Buttons[3].clicked.connect(self.loadFile)
        Buttons[4].clicked.connect(self.RemoveBtn)
        Buttons[5].clicked.connect(self.GroupBtn)
        Buttons[6].clicked.connect(self.FractionBtn)
        Buttons[7].clicked.connect(self.LabelBtn)
        Buttons[8].clicked.connect(self.SelectAllBtn)

        # Disabled buttons until function are added
        Buttons[9].setEnabled(False)

        # init changelistener on textbox
        self.textbox.textChanged[str].connect(self.filterTable)
        if self.testForTime:
            rt = timeit.default_timer() - starttime
            print("Runtime of initButtons : ", rt)

    def drawTable(self):
        """
        draws a table with the dataframe table model in tableDataFrame
        """
        self.drawtableactive = True
        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of drawTable : ", starttime)

        tabledf = Tdf.getTable(self)
        # print(tabledf)  # For debugging
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

        self.drawtableactive = False

        if self.testForTime:
            rt = timeit.default_timer() - starttime
            print("Runtime of drawTable : ", rt)

    def importBtn(self):
        """
        Imports table files, currently working are csv and tsv
        """
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;tsv (*.tsv);; csv (*.csv)", options=options)

        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of importBtn : ", starttime)

        if file:
            df = fh.importTable(self, file)
            Tdf.setTable(self, df)
            self.drawTable()

        if self.testForTime:
            rt = timeit.default_timer() - starttime
            print("Runtime of importBtn : ", rt)

    def exportBtn(self):
        """
        Exports the table to csv or tsv;default is csv
        """
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;tsv (*.tsv);; csv (*.csv)", options=options)

        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of exportBtn : ", starttime)

        if file:
            df = Tdf.getTable(self)
            temp = file.split("/")
            fileName = temp[len(temp)-1]
            length = len(fileName)
            if length < 4:
                ftype = "csv"
                file = file + ".csv"
            elif fileName.find('.csv', length-4) != -1:
                ftype = "csv"
            elif fileName.find('.tsv', length-4) != -1:
                ftype = "tsv"
            else:
                ftype = "csv"
                file = file + ".csv"

            fh.exportTable(self, df, file, ftype)

        if self.testForTime:
            rt = timeit.default_timer() - starttime
            print("Runtime of exportBtn : ", rt)

    def loadBtnFn(self):
        """
        provides a dialog to get the path for a directory
        and load the directory into the table.
        """
        dlg = QFileDialog(self)
        filePath = dlg.getExistingDirectory()

        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of loadBtnFn : ", starttime)

        if filePath != '':
            Files = fh.getFiles(self, filePath)
            delimiters = ["_"]
            preparedFiles = fh.tagfiles(self, Files, delimiters[0])
            rawTable = fh.createRawTable(self, preparedFiles, filePath)
            Tdf.setTable(self, rawTable)
            self.drawTable()

        if self.testForTime:
            rt = timeit.default_timer() - starttime
            print("Runtime of loadBtnFn : ", rt)

    def loadFile(self):
        """
        provides a filedialog to load an additional file to the dataframe
        """
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;mzML Files (*.mzML)", options=options)

        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of loadFile : ", starttime)

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

        if self.testForTime:
            print("Runtime of loadFile : ", timeit.default_timer() - starttime)

    def getSelRows(self) -> list:
        """
        Function which returns a list of the Indexes of selected Rows
        todo: needs to be adjusted to fit the datamodel:
        so far index of table is only matching index of dataframe
        in first iteration, as soon as remove is called twice it crashes.
        """
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

        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of GroupBtn : ", starttime)

        if ok:
            Tdf.modifyGroup(self, selrows, groupnum)
            self.drawTable()

        if self.testForTime:
            print("Runtime of GroupBtn : ", timeit.default_timer() - starttime)

    def RemoveBtn(self):
        """
        Enables the user to remove selected rows
        """
        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of RemoveBtn : ", starttime)

        selrows = self.getSelRows()
        Tdf.rmvRow(self, selrows)
        self.drawTable()

        if self.testForTime:
            rt = timeit.default_timer() - starttime
            print("Runtime of RemoveBtn : ", rt)

    def FractionBtn(self):
        """
        Enables the user to change the Fraction of selected rows to a given
        number or give a range.
        """
        selrows = self.getSelRows()

        # first inputdialog
        fracmin, ok = QInputDialog.getInt(self,
                                          "Fraction",
                                          "Enter minimal Fractionnumber " +
                                          "or single Fractionnumber")
        # second inputdialog if first is accepted
        if ok:
            fracmax, ok = QInputDialog.getInt(self,
                                              "Fraction",
                                              "Enter maximal Fractionnumber " +
                                              "or 0 for single Fractionnumber")
            if ok:
                # decision if multiple fractions are set or just one
                if fracmax != 0:
                    if fracmax > fracmin:
                        # third messagedialog
                        rep = QMessageBox.question(self, "Fraction Group?",
                                                   "Do you want to infer a " +
                                                   "Fraction Group from the " +
                                                   "given range?",
                                                   (QMessageBox.Yes |
                                                    QMessageBox.No),
                                                   QMessageBox.No)

                        if self.testForTime:
                            starttime = timeit.default_timer()
                            print("Starttime of FractionBtn : ", starttime)

                        # when confirmed the fraction froup is set
                        # when max fraction is reached.
                        if rep == QMessageBox.Yes:
                            Tdf.modifyFraction(self, selrows, fracmin, fracmax)
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
                                Tdf.modifyGroup(self, subrows, group)
                        else:
                            Tdf.modifyFraction(self, selrows, fracmin, fracmax)

                        if self.testForTime:
                            rt = timeit.default_timer() - starttime
                            print("Runtime of FractionBtn : ", rt)

                    if self.testForTime:
                        starttime = timeit.default_timer()
                        print("Starttime of FractionBtn : ", starttime)

                    elif fracmax == fracmin:
                        Tdf.modifyFraction(self, selrows, fracmin)

                    if self.testForTime:
                        rt = timeit.default_timer() - starttime
                        print("Runtime of FractionBtn : ", rt)

                    else:
                        QMessageBox.warning(self, "Error", "Please use " +
                                            "a higher integer " +
                                            "number for the maximum " +
                                            "fractionnumber.")

                if self.testForTime:
                    starttime = timeit.default_timer()
                    print("Starttime of FractionBtn : ", starttime)

                else:
                    Tdf.modifyFraction(self, selrows, fracmin)
                self.drawTable()

                if self.testForTime:
                    rt = timeit.default_timer() - starttime
                    print("Runtime of FractionBtn : ", rt)

    def LabelBtn(self):
        """
        Let the user choose the number of labels, it will generate
        the labels for the copied rows and also links the sample to
        the label. Gives an option to continue the samplecount
        over fraction groups.
        """
        labelnum, ok = QInputDialog.getInt(self, "Label",
                                           "Please specify the multiplicity " +
                                           "of the selected rows")
        if ok:
            rep = QMessageBox.question(self, "Continuous Sample",
                                       "Does the samplenumber " +
                                       "continue over multiple " +
                                       "fraction groups?",
                                       (QMessageBox.Yes |
                                        QMessageBox.No),
                                       QMessageBox.No)

            if self.testForTime:
                starttime = timeit.default_timer()
                print("Starttime of LabelBtn : ", starttime)

            if rep == QMessageBox.Yes:
                try:
                    Tdf.modifyLabelSample(self, labelnum, True)
                except ValueError:
                    QMessageBox.about(self, "Warning", "Unfortunaly, " +
                                            "your Number was <1")
            else:
                try:
                    Tdf.modifyLabelSample(self, labelnum, False)
                except ValueError:
                    QMessageBox.about(self, "Warning", "Unfortunaly, " +
                                            "your Number was <1")
            self.drawTable()

            if self.testForTime:
                rt = timeit.default_timer() - starttime
                print("Runtime of LabelBtn : ", rt)

    def SelectAllBtn(self):
        """
        Selects all Rows of the Table
        """
        if self.testForTime:
            starttime = timeit.default_timer()
            print("Starttime of SelectAllBtn : ", starttime)

        self.table.setSelectionMode(QAbstractItemView.MultiSelection)

        for i in range(self.table.rowCount()):
            selected = self.getSelRows()

            for j in range(len(selected)):
                if i == selected[j]:
                    self.table.selectRow(i)

            self.table.selectRow(i)

        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

        if self.testForTime:
            rt = timeit.default_timer() - starttime
            print("Runtime of SelectAllBtn : ", rt)

    def filterTable(self):
        """
        get changes from textbox and update table when
        more than 3 characters are given.
        then update table with the rows that
        contain the input in the give column.
        """
        tb = self.textbox
        givencolumn = "Spectra_Filepath"
        tbinput = tb.text()
        ft = Tdf.getTable(self)
        validDf = not(ft.empty or ft.dropna().empty)
        print(validDf)
        print(type(ft))
        if len(tbinput) >= 3:
            rowstoshow = ft[ft[givencolumn].str.contains(tbinput)]
            # prints the rows containing the input
            print(rowstoshow)
            # updated table funtion goes here

    def changeListener(self):
        self.table.itemChanged.connect(self.editField)

    def editField(self):
        if len(self.table.selectedItems()) == 1:
            if not self.drawtableactive:
                itemchanged = self.table.currentItem()
                newvalue = itemchanged.text()
                row = itemchanged.row()
                column = itemchanged.column()
                if column != 2:
                    Tdf.modifyField(self, row, column, newvalue)
                    self.drawTable()
                else:
                    QMessageBox.about(self, "Warning", "Please only, " +
                                            "modify attribute columns," +
                                            "not the filepath.\n" +
                                            "To change the filepath," +
                                            "use remove and add file.")
                    self.drawTable()
