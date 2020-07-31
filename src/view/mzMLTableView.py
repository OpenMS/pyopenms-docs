import os
import sys
import timeit
import pandas as pd
import math
from PyQt5 import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QFileDialog, \
        QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, \
        QVBoxLayout, QInputDialog, QLineEdit, QMessageBox, \
        QAbstractItemView
sys.path.append(os.getcwd() + '/../controller')
from filehandler import FileHandler as fh  # noqa E402
sys.path.append(os.getcwd() + '/../model')
from tableDataFrame import TableDataFrame as Tdf  # noqa E402


class mzMLTableView(QWidget):
    """
    Main Widget of the TableEditor app
    """

    def __init__(self, *args):
        # set variable self.testForTime to True to see Runtimes
        # the following 2 if constructs can be used to determine
        # timing
        # just put them around whatever should be timed

        # self.testForTime = False
        # if self.testForTime:
        #    starttime = timeit.default_timer()
        #    print("Starttime of overall Initiation : ", starttime)

        # if self.testForTime:
        #    rt = timeit.default_timer() - starttime
        #    print("Runtime of overall Initiation was : ", rt)

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

    def initTable(self):
        """
        initializes Table
        """
        self.tablefile_loaded = False
        self.loaded_table = ""
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setSortingEnabled(True)
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

    def initButtons(self):
        """
        initializes Buttons
        """
        self.buttons = QWidget()
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.setFixedHeight(20)
        self.textbox.setToolTip("Filter the experimental layout " +
                                "according to Spectra Filepath " +
                                "column. It will be dynamically \n" +
                                "updated as soon as 2 characters " +
                                "are inserted.")

        Buttons = [QPushButton('Load Project'), QPushButton('Load Table'),
                   QPushButton('Save Table'), QPushButton('Add File'),
                   QPushButton('Remove File'), QPushButton('Group'),
                   QPushButton('Fraction'), QPushButton('Label'),
                   QPushButton('Select All')]

        # Buttonlayout
        buttonlayout = QHBoxLayout()
        for button in Buttons:
            buttonlayout.addWidget(button)

        buttonlayout.addWidget(self.textbox)
        self.buttons.setLayout(buttonlayout)

        # Connections for Buttons and their apropriate functions
        Buttons[0].clicked.connect(self.loadBtnFn)
        Buttons[0].setToolTip("Load a directory with .mzML files to " +
                              "generate your own eperimental layout. " +
                              "For mzML filenames, \"F\" is the regular \n" +
                              "expression for fraction, while \"G\" or " +
                              "\"FG\"is the regular expression for the " +
                              "fraction groups.")
        Buttons[1].clicked.connect(self.importBtn)
        Buttons[1].setToolTip("Load an existing experimental layout, as " +
                              ".csv or .tsv to display and modify it.")
        Buttons[2].clicked.connect(self.exportBtn)
        Buttons[2].setToolTip("Save the experimental layout as .csv or " +
                              ".tsv file. .csv is the default option")
        Buttons[3].clicked.connect(self.loadFile)
        Buttons[3].setToolTip("Load an additional single .mzML file " +
                              "to the experimental layout.")
        Buttons[4].clicked.connect(self.RemoveBtn)
        Buttons[4].setToolTip("Remove one or more selected .mzML " +
                              "files from the experimental layout.")
        Buttons[5].clicked.connect(self.GroupBtn)
        Buttons[5].setToolTip("Set the fraction group of selected rows " +
                              "to a given number.")
        Buttons[6].clicked.connect(self.FractionBtn)
        Buttons[6].setToolTip("Set the fraction of selected rows to a " +
                              "specific number or use a range to define " +
                              "multiple fractions. This function is \n" +
                              "also able to work over multiple fraction " +
                              "groups and sets the group according to the " +
                              "fraction number.")
        Buttons[7].clicked.connect(self.LabelBtn)
        Buttons[7].setToolTip("Set the number of labels, the program will " +
                              "generate the necessary rows and will also " +
                              "define the samplenumber for you. You can \n" +
                              "apply the option to continue samplenumbers " +
                              "over mutliple fraction groups to combine " +
                              "two sample preparations.")
        Buttons[8].clicked.connect(self.SelectAllBtn)

        # init changelistener on textbox
        self.textbox.textChanged[str].connect(self.filterTable)

    def getDataFrame(self):
        return self.tdf.getTable(self)

    def drawTable(self):
        """
        draws a table with the dataframe table model in tableDataFrame
        """
        self.drawtableactive = True

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

    def importBtn(self, file: str = ""):
        """
        Imports table files, currently working are csv and tsv
        """
        options = QFileDialog.Options()
        if not file:
            file, _ = QFileDialog.getOpenFileName(
                self, "QFileDialog.getOpenFileName()", "",
                "All Files (*);;tsv (*.tsv);; csv (*.csv)", options=options)

        if file:
            df = fh.importTable(self, file)
            Tdf.setTable(self, df)
            self.drawTable()
            self.tablefile_loaded = True
            file = file.split("/")[-1]
            self.loaded_table = file

    def exportBtn(self):
        """
        Exports the table to csv or tsv;default is csv
        """
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;tsv (*.tsv);; csv (*.csv)", options=options)

        if file:
            self.tablefile_loaded = True
            fpath = file.split("/")[-1]
            self.loaded_table = fpath
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

    def loadBtnFn(self):
        """
        provides a dialog to get the path for a directory
        and load the directory into the table.
        """
        dlg = QFileDialog(self)
        filePath = dlg.getExistingDirectory()

        if filePath != '':
            self.loadDir(filePath)

    def loadDir(self, filepath: str):
        Files = fh.getFiles(self, filepath)
        delimiters = ["_"]
        preparedFiles = fh.tagfiles(self, Files, delimiters[0])
        rawTable = fh.createRawTable(self, preparedFiles, filepath)
        Tdf.setTable(self, rawTable)
        self.drawTable()

    def loadFile(self, file: str = ""):
        """
        provides a filedialog to load an additional file to the dataframe
        """
        options = QFileDialog.Options()
        if not file:
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

        if ok:
            Tdf.modifyGroup(self, selrows, groupnum)
            self.drawTable()

    def RemoveBtn(self):
        """
        Enables the user to remove selected rows
        """
        selrows = self.getSelRows()
        Tdf.rmvRow(self, selrows)
        self.drawTable()

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

                    elif fracmax == fracmin:
                        Tdf.modifyFraction(self, selrows, fracmin)

                    else:
                        QMessageBox.warning(self, "Error", "Please use " +
                                            "a higher integer " +
                                            "number for the maximum " +
                                            "fractionnumber.")

                else:
                    Tdf.modifyFraction(self, selrows, fracmin)
                self.drawTable()

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

    def SelectAllBtn(self):
        """
        Selects all Rows of the Table
        """
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)

        for i in range(self.table.rowCount()):
            selected = self.getSelRows()

            for j in range(len(selected)):
                if i == selected[j]:
                    self.table.selectRow(i)

            self.table.selectRow(i)

        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def updateTableView(self, rows):
        tabledf = Tdf.getTable(self)
        rowcount = len(tabledf.index)
        for i in range(rowcount):
            self.table.setRowHidden(i, True)
        for i in rows:
            self.table.setRowHidden(i, False)

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
        # print(validDf)  # for debugging
        # print(type(ft))  # for debugging
        if len(tbinput) >= 2:
            rowstoshow = ft[ft[givencolumn].str.contains(tbinput)]
            self.updateTableView(rowstoshow.index)
        else:
            self.updateTableView(ft.index)

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
