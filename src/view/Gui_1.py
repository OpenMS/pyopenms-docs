import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QMainWindow,
                             QAction, qApp, QApplication,
                             QHBoxLayout, QVBoxLayout, QMessageBox,
                             QLineEdit, QTableWidget, QTableWidgetItem,
                             QGridLayout, QScrollArea, QPlainTextEdit,
                             QDesktopWidget, QLabel, QRadioButton,
                             QGroupBox, QSizePolicy, QCheckBox, QFileDialog,
                             QTextEdit)
from PyQt5.QtGui import QFont, QColor
#from dictionaries import Dict
sys.path.insert(0, '../examples')
from Logic_fastaSearch import*  # NOQA: E402


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(835, 680)
        self.initUI()

    def initUI(self):
        # creating Action loadAct
        # when selected loads a file which is a fasta data
        # first implement with exit action to test if is working
        # later when the loading alg is ready implement correctly

        # creating Buttons
        #width = 800
        #heightPro = 100
        #heightID = 500
        self.searchButtonP = QtWidgets.QPushButton(self)
        self.searchButtonP.setText("search")
        #self.searchButtonP.move(width, heightPro)

        self.searchButtonP.clicked.connect(self.clickprotein)

        self.loadbutton = QtWidgets.QPushButton(self)
        self.loadbutton.setText("load")
        self.loadbutton.clicked.connect(self.loadingfile)

        # creating testboxes for the buttons
        self.boxPro = QLineEdit(self)
        # self.boxPro.move(width-280, heightPro)
        # self.boxPro.resize(280, 30)

        # Creating treewidget
        self.tw = QtWidgets.QTreeWidget()
        self.tw.setHeaderLabels(["Accession", "Organism", "Protein Name"])
        self.tw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.tw.setColumnWidth(1, 280)

        # create a textfield for the result after a protein search
        self.resultBox = QPlainTextEdit(self)
        self.resultBox.setReadOnly(True)

        # Layout
        self.mainwidget = QWidget(self)
        self.main_layout = QVBoxLayout(self.mainwidget)

        # every set contains all widgets on the level they should be in the UI
        # in set1 there is a textbox and a button
        self.set1 = QHBoxLayout()
        self.set1.addWidget(self.boxPro)
        self.set1.addWidget(self.searchButtonP)
        self.set1.addWidget(self.loadbutton)
        # self.set1.addStretch(1)

        # set 2 contains the radiobuttons and a label
        self.set2 = QHBoxLayout()
        self.radioname = QRadioButton("Name")
        self.radioid = QRadioButton("ID")
        self.radioseq = QRadioButton("sequence")
        self.radioname.setChecked(True)
        self.decoycheck = QCheckBox("Decoy search", self)
        self.datalabel = QLabel()
        self.datalabel.setText("Data not loaded")
        self.set2.addWidget(self.radioname)
        self.set2.addWidget(self.radioid)
        self.set2.addWidget(self.radioseq)
        self.set2.addWidget(self.decoycheck)
        self.set2.addWidget(self.datalabel)
        # self.set2.addStretch(1)

        # set 3 contains the table and the result box
        self.set3 = QHBoxLayout()
        self.set3.addWidget(self.tw)

        # adding all QHBoxLayout to the main QVBoxLayout
        self.main_layout.addLayout(self.set1)
        self.main_layout.addLayout(self.set2)
        self.main_layout.addLayout(self.set3)

        # creating a scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.mainwidget)
        self.scroll.setWidgetResizable(True)
        self.mainwidget.setLayout(self.main_layout)
        self.setCentralWidget(self.mainwidget)
        self.setWindowTitle('Protein Viewer')
        # defining some colors to marked searched sequences
        self.color = QColor(255, 0, 0)
        self.colorblack = QColor(0, 0, 0)
        self.center()
        self.show()
        # defining a counter var that checks if a file has been loaded
        # if not than there should be an error Window when a search is done

        self.fileloaded = 0
        # centering the widget

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # defining a help function to cut the sequence that is being search from the
    # Protein sequence that has been found
    def cutstring(self, oldstring, proteinseq):
        cut = oldstring.split(proteinseq)
        return cut
    # defining the function for load button to get path of database

    def loadingfile(self):
        self.filename = QFileDialog.getOpenFileName()
        self.path = self.filename[0]
        self.fileloaded = 1
        # loading the lists before searching in order to make the search faster
        self.dictKeyAccession, self.proteinList, self.proteinNameList, self.proteinOSList, self.dictKeyAccessionDECOY, self.proteinListDECOY, self.proteinNameListDECOY, self.proteinOSListDECOY = logic.protein_dictionary(
            self.path)
        self.datalabel.setText("Data loaded")
    # defining the clickprotein method for the searchButtonP

    def clickprotein(self):
        if self.fileloaded == 0:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Information)
            self.error.setText("Please load Data before searching")
            self.error.setWindowTitle("Error")
            c = self.error.exec_()
        else:
            self.tw.clear()
            # check if inputbox is empty. if empty return error if not proceed
            if self.boxPro.text() == "":
                self.error = QMessageBox()
                self.error.setIcon(QMessageBox.Information)
                self.error.setText("Please enter input before searching")
                self.error.setWindowTitle("Error")
                a = self.error.exec_()
            else:
                if self.radioid.isChecked() == True:
                    self.radioIdSearch()

                if self.radioseq.isChecked() == True:
                    self.sequenceSearch()

                if self.radioname.isChecked() == True:
                    self.nameSearch()

    def radioIdSearch(self):
        counter = 0
        protein_accession_maybe_sub_sequence = self.boxPro.text()
        if self.decoycheck.isChecked():
            for protein_accession in self.dictKeyAccessionDECOY:
                if protein_accession_maybe_sub_sequence in protein_accession:
                    counter = counter + 1
                    index = list(self.dictKeyAccessionDECOY).index(
                        protein_accession)
                    Protein = self.dictKeyAccessionDECOY.get(
                        protein_accession)
                    ID = list(self.dictKeyAccessionDECOY.keys())[
                        index]
                    Proteinname = self.proteinNameListDECOY[index]
                    OS = self.proteinOSListDECOY[index]
                    self.cg = QtWidgets.QTreeWidgetItem(self.tw)
                    self.cg.setData(0, 0, ID)
                    self.cg.setData(1, 0, OS)
                    self.cg.setData(2, 0, Proteinname)
                    self.textp = QTextEdit()
                    self.textp.resize(
                        self.textp.width(), self.textp.height())
                    self.textp.insertPlainText("Proteinsequenz: " + Protein)
                    self.textp.setReadOnly(True)
                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        else:
            for protein_accession in self.dictKeyAccession:
                if protein_accession_maybe_sub_sequence in protein_accession:
                    counter = counter + 1
                    index = list(self.dictKeyAccession).index(
                        protein_accession)
                    Protein = self.dictKeyAccession.get(
                        protein_accession)
                    ID = list(self.dictKeyAccession.keys())[index]
                    Protein = self.proteinList[index]
                    Proteinname = self.proteinNameList[index]
                    OS = self.proteinOSList[index]

                    self.cg = QtWidgets.QTreeWidgetItem(self.tw)
                    self.cg.setData(0, 0, ID)
                    self.cg.setData(1, 0, OS)
                    self.cg.setData(2, 0, Proteinname)

                    self.textp = QTextEdit()
                    self.textp.resize(
                        self.textp.width(), self.textp.height())
                    self.textp.insertPlainText(
                        "Proteinsequenz: " + Protein)
                    self.textp.setReadOnly(True)
                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        if counter == 0:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(
                "No matching protein accession found in database.")
            self.msg.setWindowTitle("Error")
            x = self.msg.exec_()

    def sequenceSearch(self):
        counter = 0
        protein_sub_sequence = self.boxPro.text()
        if self.decoycheck.isChecked():
            for protein_sequence in self.proteinListDECOY:
                if protein_sub_sequence in protein_sequence:
                    counter = counter + 1
                    index = self.proteinListDECOY.index(
                        protein_sequence)
                    ID = list(self.dictKeyAccessionDECOY.keys())[
                        index]
                    Protein = self.proteinListDECOY[index]
                    Proteinname = self.proteinNameListDECOY[index]
                    OS = self.proteinOSListDECOY[index]

                    self.cg = QtWidgets.QTreeWidgetItem(self.tw)
                    self.cg.setData(0, 0, ID)
                    self.cg.setData(1, 0, OS)
                    self.cg.setData(2, 0, Proteinname)

                    self.textp = QTextEdit()
                    self.textp.resize(
                        self.textp.width(), self.textp.height())
                    cuts = self.cutstring(
                        Protein, protein_sub_sequence)
                    self.textp.insertPlainText(
                        "Proteinsequenz: "
                    )

                    for i in range(len(cuts)):
                        # sofern wir ganz am Anfang der Liste sind
                        if (cuts[i] == '' and i == 0):
                            self.textp.setTextColor(self.color)
                            self.textp.insertPlainText(
                                protein_sub_sequence)
                            self.textp.setTextColor(
                                self.colorblack)
                        # sofern wir mitten drin sind und der sub_string mehrfach auftaucht
                        elif (cuts[i] == ''):
                            self.textp.setTextColor(self.color)
                            self.textp.insertPlainText(
                                protein_sub_sequence)
                            self.textp.setTextColor(
                                self.colorblack)
                        else:
                            if (i == len(cuts) - 1):
                                self.textp.insertPlainText(cuts[i])
                            else:
                                self.textp.insertPlainText(cuts[i])
                                self.textp.setTextColor(self.color)
                                self.textp.insertPlainText(
                                    protein_sub_sequence)
                                self.textp.setTextColor(
                                    self.colorblack)

                    self.textp.setReadOnly(True)
                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        else:
            for protein_sequence in self.proteinList:
                if protein_sub_sequence in protein_sequence:
                    counter = counter + 1
                    index = self.proteinList.index(
                        protein_sequence)
                    ID = list(self.dictKeyAccession.keys())[index]
                    Protein = self.proteinList[index]
                    Proteinname = self.proteinNameList[index]
                    OS = self.proteinOSList[index]

                    self.cg = QtWidgets.QTreeWidgetItem(self.tw)
                    self.cg.setData(0, 0, ID)
                    self.cg.setData(1, 0, OS)
                    self.cg.setData(2, 0, Proteinname)

                    self.textp = QTextEdit()
                    self.textp.resize(
                        self.textp.width(), self.textp.height())
                    cuts = self.cutstring(
                        Protein, protein_sub_sequence)
                    self.textp.insertPlainText(
                        "Proteinsequenz: "
                    )

                    for i in range(len(cuts)):
                        # sofern wir ganz am Anfang der Liste sind
                        if (cuts[i] == '' and i == 0):
                            self.textp.setTextColor(self.color)
                            self.textp.insertPlainText(
                                protein_sub_sequence)
                            self.textp.setTextColor(
                                self.colorblack)
                        # sofern wir mitten drin oder am Ende sind sind
                        elif (cuts[i] == ''):
                            self.textp.setTextColor(self.color)
                            self.textp.insertPlainText(
                                protein_sub_sequence)
                            self.textp.setTextColor(
                                self.colorblack)
                        else:
                            if (i == len(cuts) - 1):
                                self.textp.insertPlainText(cuts[i])
                            else:
                                self.textp.insertPlainText(cuts[i])
                                self.textp.setTextColor(self.color)
                                self.textp.insertPlainText(
                                    protein_sub_sequence)
                                self.textp.setTextColor(
                                    self.colorblack)

                    self.textp.setReadOnly(True)
                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        if counter == 0:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(
                "No matching protein sequence found in database.")
            self.msg.setWindowTitle("Error")
            x = self.msg.exec_()

    def nameSearch(self):
        counter = 0
        protein_sub_name = self.boxPro.text()
        if self.decoycheck.isChecked():
            for protein_name in self.proteinNameListDECOY:
                if protein_sub_name in protein_name:
                    counter = counter + 1
                    index = self.proteinNameListDECOY.index(
                        protein_name)
                    ID = list(self.dictKeyAccessionDECOY.keys())[
                        index]
                    Protein = self.proteinListDECOY[index]
                    Proteinname = protein_name
                    OS = self.proteinOSListDECOY[index]

                    self.cg = QtWidgets.QTreeWidgetItem(self.tw)
                    self.cg.setData(0, 0, ID)
                    self.cg.setData(1, 0, OS)
                    self.cg.setData(2, 0, Proteinname)

                    self.textp = QPlainTextEdit()
                    self.textp.resize(
                        self.textp.width(), self.textp.height())
                    self.textp.insertPlainText(
                        "\nProteinsequenz: " + Protein)
                    self.textp.setReadOnly(True)
                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        else:
            for protein_name in self.proteinNameList:
                if protein_sub_name in protein_name:
                    counter = counter + 1
                    index = self.proteinNameList.index(
                        protein_name)
                    ID = list(self.dictKeyAccession.keys())[index]
                    Protein = self.proteinList[index]
                    Proteinname = protein_name
                    OS = self.proteinOSList[index]

                    self.cg = QtWidgets.QTreeWidgetItem(self.tw,)
                    self.cg.setData(0, 0, ID)
                    self.cg.setData(1, 0, OS)
                    self.cg.setData(2, 0, Proteinname)

                    self.textp = QPlainTextEdit()
                    self.textp.resize(
                        self.textp.width(), self.textp.height())
                    self.textp.insertPlainText(
                        "Proteinsequenz: " + Protein)
                    self.textp.setReadOnly(True)
                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        if counter == 0:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(
                "No matching protein name found in database.")
            self.msg.setWindowTitle("Error")
            x = self.msg.exec_()


def main():

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
