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
                             QTextEdit, QTextBrowser)
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QTextCursor
from PyQt5.QtCore import *  # Qt, QUrl
# from dictionaries import Dict
sys.path.insert(0, '../examples')
from Logic_fastaSearch import*  # NOQA: E402


class FastaViewer(QMainWindow):
    """
    A class used to make and change the apperance of a Window

    ...

    Attributes
    ----------
    searchButtonP : QtWidgets.QPushButton
        a button to be shown on window and exc action on click

    searchButtonP : QtWidgets.QPushButton
         Button to be shown on window and exc action on click

    boxPro : QLineEdit(self)
         Textfield in wich the user can type inputs

    tw : QtWidgets.QTreeWidget
         Treewidget used to hold and show data on the sceen

    mainwidget : QWidget
         QWidget that contains all the Widgets

    main_layout : QVBoxLayout
        The main Layout of the Window, contains all other Layouts

    set1,set2,set3 : QHBoxLayout()
         Horizontal Layouts that hold different Widgets

    radioname,radioid,radioseq=QRadioButton
            A QRadioButton that appears on sceen an can be cheked

    scroll : QScrollArea()
            Makes an areo of the Window scrollable

    color : QColor
            Red Color for the searched seq

    colorblack : QColor
            Black color for the found Protein sequence
    fileloaded : int
            Integer to check if file has been loaded
    Methods
    -------
    _init_(self)
        Sets Window size na exc. initUI()

    initUi(self)
            Creates the User Interface

    center(self)
            Centers the Window on screen

    cutstring(self,oldstring,proteinseq)
            Cuts the oldstring when proteinseq appears and returns a list of
            the cuts

    lodafile(self)
            A function for the loadbutton that open QFileDialog and saves the
            Path to the file fo the logic class

    clickprotein(self)
            A function for the searchButtonP, it checks if input is correct
            and exc a search function

    radioIdSearch()
            Searches for the Protein Information by ID


    sequenceSearch()
            Searches for the Protein Information by sequence and also changes
            the color of the are of the sequence that is the same as the input

    nameSearch()
            Searches for the Protein Information by name

    main()
            runs the QApplication
    """

    def __init__(self):
        """Gets self and sets Window size na exc. initUI()

        Parameters
        ----------
        self : QMainWindow


        Returns
        -------
        nothing
        """
        super().__init__()
        self.resize(800, 1000)
        self.initUI()

    def initUI(self):
        """Gets self and creates creates the User Interface

        Parameters
        ----------
        self : QMainWindow


        Returns
        -------
        nothing
        """
        # creating Buttons

        self.searchButtonP = QtWidgets.QPushButton(self)
        self.searchButtonP.setText("search")
        self.searchButtonP.clicked.connect(self.clickprotein)

        self.loadbutton = QtWidgets.QPushButton(self)
        self.loadbutton.setText("load")
        self.loadbutton.clicked.connect(self.loadingfile)

        # creating testboxes for the buttons
        self.boxPro = QLineEdit(self)

        # Creating treewidget for displaying the proteins
        self.tw = QtWidgets.QTreeWidget()
        self.tw.setHeaderLabels(["Accession", "Organism", "Protein Name"])
        self.tw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout
        self.mainwidget = QWidget(self)
        self.main_layout = QVBoxLayout(self.mainwidget)

        # every set contains all widgets on the level they should be in the UI
        # in set1 there is a textbox and a button
        self.set1 = QHBoxLayout()
        self.set1.addWidget(self.boxPro)
        self.set1.addWidget(self.searchButtonP)
        self.set1.addWidget(self.loadbutton)

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
        """Gets self and centers the Window
        Parameters
        ----------
        self : QMainWindow


        Returns
        -------
        changes so that the Window appears on the center of the screen
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # defining a help function to cut the sequence that is being search from the
    # Protein sequence that has been found

    def cutstring(self, oldstring: str, proteinseq: str) -> str:
        """Gets two strings and splits the first string in a list
            on the playces where the second string is found. This helps
            to change the color of the sequences later on

    Parameters
    ----------
    oldstring : str
        the enteire proteinseq as a string
    proteinseq : str
        is the searched seq and is used to split the entire seq in parts

    Returns
    -------
    list
        a list of strings to be later put together after recoloring
    """
        cut = oldstring.split(proteinseq)
        return cut
    # defining the function for load button to get path of database

    def loadingfile(self):
        """Gets QMainWindow and opens a QFileDialog and loads path

    Parameters
    ----------
    self : QMainWindow
        the MainWindow of the class


    Returns
    -------
    nothing , it changes the QMainWindow so that the user can see that a file
    has been loaded
    """
        self.filename = QFileDialog.getOpenFileName()
        self.path = self.filename[0]
        self.fileloaded = 1
        # loading the lists before searching in order to make the search faster
        self.dictKeyAccession, self.proteinList, self.proteinNameList, self.proteinOSList, self.dictKeyAccessionDECOY, self.proteinListDECOY, self.proteinNameListDECOY, self.proteinOSListDECOY = logic.protein_dictionary(
            self.path)
        self.datalabel.setText("Data loaded")
        for i in range(len(self.dictKeyAccession)):
            ID = list(self.dictKeyAccession.keys())[i]
            Protein = self.proteinList[i]
            Proteinname = self.proteinNameList[i]
            OS = self.proteinOSList[i]
            self.cg = QtWidgets.QTreeWidgetItem(self.tw)
            self.cg.setData(0, 0, ID)
            self.cg.setData(1, 0, OS)
            self.cg.setData(2, 0, Proteinname)

    # defining the clickprotein method for the searchButtonP

    def clickprotein(self):
        """Gets self and searches for Protein and shows the result
        on QMainWindow

    Parameters
    ----------
    self : QMainWindow


    Returns
    -------
    nothing but changes the QMainWindow to show the Protein or an Error message
    """
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
        # doc recommends enabling sorting after loading the tree with elements
        self.tw.setSortingEnabled(True)

    def radioIdSearch(self):
        """Gets self and searches for Protein based on ID
            and shows the result on QMainWindow, also adds a hyperlink for
            more Information

        Parameters
        ----------
        self : QMainWindow


        Returns
        -------
        nothing but changes the QMainWindow to show the Protein in treewidget
        """
        atLeastOneProteinFound = False
        protein_accession_maybe_sub_sequence = self.boxPro.text()

        if self.decoycheck.isChecked():
            for protein_accession in self.dictKeyAccessionDECOY:
                if protein_accession_maybe_sub_sequence in protein_accession:
                    atLeastOneProteinFound = True
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
                    self.link = QLabel()

                    self.link.setTextInteractionFlags(
                        Qt.LinksAccessibleByMouse)
                    self.link.setOpenExternalLinks(True)
                    self.link.setTextFormat(Qt.RichText)
                    self.link.setText("<a href =" + "https://www.uniprot.org/uniprot/" +
                                      ID + ">" + "More Information"+" </a>")
                    self.textp = QTextEdit()
                    self.textp.resize(
                        self.textp.width(), self.textp.height())
                    self.textp.insertPlainText(
                        "Proteinsequenz: " + Protein + "\n")

                    self.textp.setReadOnly(True)

                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild2 = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)
                    self.tw.setItemWidget(
                        self.cgChild2, 0, self.link)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        else:
            for protein_accession in self.dictKeyAccession:
                if protein_accession_maybe_sub_sequence in protein_accession:
                    atLeastOneProteinFound = True
                    index = list(self.dictKeyAccession).index(
                        protein_accession)
                    ID = list(self.dictKeyAccession.keys())[index]
                    Protein = self.proteinList[index]
                    Proteinname = self.proteinNameList[index]
                    OS = self.proteinOSList[index]
                    self.dummy = ID
                    self.cg = QtWidgets.QTreeWidgetItem(self.tw)
                    self.cg.setData(0, 0, ID)
                    self.cg.setData(1, 0, OS)
                    self.cg.setData(2, 0, Proteinname)
                    self.link = QLabel()

                    self.link.setTextInteractionFlags(
                        Qt.LinksAccessibleByMouse)
                    self.link.setOpenExternalLinks(True)
                    self.link.setTextFormat(Qt.RichText)
                    self.link.setText("<a href =" + "https://www.uniprot.org/uniprot/" +
                                      ID + ">" + "More Information"+" </a>")

                    self.textp = QTextEdit()
                    self.textp.resize(
                        self.textp.width(), self.textp.height())
                    self.textp.insertPlainText(
                        "Proteinsequenz: " + Protein + "\n")

                    self.textp.setReadOnly(True)

                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild2 = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)
                    self.tw.setItemWidget(
                        self.cgChild2, 0, self.link)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        if not atLeastOneProteinFound:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(
                "No matching protein accession found in database.")
            self.msg.setWindowTitle("Error")
            x = self.msg.exec_()

    def sequenceSearch(self):
        """Gets self and searches for Protein based on sequence
            and shows the result on QMainWindow, also adds a hyperlink for
            more Information

        Parameters
        ----------
        self : QMainWindow


        Returns
        -------
        nothing but changes the QMainWindow to show the Protein in treewidget
        also changes the color of the parts of the sequence
        that are being searched
        """
        atLeastOneProteinFound = False
        protein_sub_sequence = self.boxPro.text()

        if self.decoycheck.isChecked():
            for protein_sequence in self.proteinListDECOY:
                if protein_sub_sequence in protein_sequence:
                    atLeastOneProteinFound = True
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
                    self.link = QLabel()

                    self.link.setTextInteractionFlags(
                        Qt.LinksAccessibleByMouse)
                    self.link.setOpenExternalLinks(True)
                    self.link.setTextFormat(Qt.RichText)
                    self.link.setText("<a href =" + "https://www.uniprot.org/uniprot/" +
                                      ID + ">" + "More Information"+" </a>")

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
                    self.textp.insertPlainText("\n")

                    self.textp.setReadOnly(True)

                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild2 = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)
                    self.tw.setItemWidget(
                        self.cgChild2, 0, self.link)
            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        else:
            for protein_sequence in self.proteinList:
                if protein_sub_sequence in protein_sequence:
                    atLeastOneProteinFound = True
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

                    self.link = QLabel()

                    self.link.setTextInteractionFlags(
                        Qt.LinksAccessibleByMouse)
                    self.link.setOpenExternalLinks(True)
                    self.link.setTextFormat(Qt.RichText)
                    self.link.setText("<a href =" + "https://www.uniprot.org/uniprot/" +
                                      ID + ">" + "More Information"+" </a>")

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
                    self.cgChild2 = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)
                    self.tw.setItemWidget(
                        self.cgChild2, 0, self.link)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        if not atLeastOneProteinFound:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(
                "No matching protein sequence found in database.")
            self.msg.setWindowTitle("Error")
            x = self.msg.exec_()

    def nameSearch(self):
        """Gets self and searches for Protein based on Proteinname
            and shows the result on QMainWindow, also adds a hyperlink for
            more Information

        Parameters
        ----------
        self : QMainWindow


        Returns
        -------
        nothing but changes the QMainWindow to show the Protein in treewidget
        """
        atLeastOneProteinFound = False
        protein_sub_name = self.boxPro.text()

        if self.decoycheck.isChecked():
            for protein_name in self.proteinNameListDECOY:
                if protein_sub_name in protein_name:
                    atLeastOneProteinFound = True
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

                    self.link = QLabel()

                    self.link.setTextInteractionFlags(
                        Qt.LinksAccessibleByMouse)
                    self.link.setOpenExternalLinks(True)
                    self.link.setTextFormat(Qt.RichText)
                    self.link.setText("<a href =" + "https://www.uniprot.org/uniprot/" +
                                      ID + ">" + "More Information"+" </a>")

                    self.textp = QTextEdit()
                    self.textp.resize(
                        self.textp.width(), self.textp.height())
                    self.textp.insertPlainText(
                        "\nProteinsequenz: " + Protein + "\n")

                    self.textp.setReadOnly(True)

                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild2 = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)
                    self.tw.setItemWidget(
                        self.cgChild2, 0, self.link)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        else:
            for protein_name in self.proteinNameList:
                if protein_sub_name in protein_name:
                    atLeastOneProteinFound = True
                    index = self.proteinNameList.index(
                        protein_name)
                    ID = list(self.dictKeyAccession.keys())[index]
                    Protein = self.proteinList[index]
                    Proteinname = self.proteinNameList[index]
                    OS = self.proteinOSList[index]

                    self.cg = QtWidgets.QTreeWidgetItem(self.tw,)
                    self.cg.setData(0, 0, ID)
                    self.cg.setData(1, 0, OS)
                    self.cg.setData(2, 0, Proteinname)

                    self.link = QLabel()

                    self.link.setTextInteractionFlags(
                        Qt.LinksAccessibleByMouse)
                    self.link.setOpenExternalLinks(True)
                    self.link.setTextFormat(Qt.RichText)
                    self.link.setText("<a href =" + "https://www.uniprot.org/uniprot/" +
                                      ID + ">" + "More Information"+" </a>")

                    self.textp = QTextEdit()
                    self.textp.resize(
                        self.textp.width(), self.textp.height())
                    self.textp.insertPlainText(
                        "Proteinsequenz: " + Protein + "\n")

                    self.textp.setReadOnly(True)
                    self.cgChild = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild2 = QtWidgets.QTreeWidgetItem(
                        self.cg)
                    self.cgChild.setFirstColumnSpanned(True)
                    self.tw.setItemWidget(
                        self.cgChild, 0, self.textp)
                    self.tw.setItemWidget(
                        self.cgChild2, 0, self.link)

            header = self.tw.header()
            header.setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        if not atLeastOneProteinFound:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(
                "No matching protein name found in database.")
            self.msg.setWindowTitle("Error")
            x = self.msg.exec_()


def main():
    """Gets nothing, runs the QApplication

    Parameters
    ----------
    nothing


    Returns
    -------
    nothing
    """
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
