import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QMainWindow,
                             QAction, qApp, QApplication,
                             QHBoxLayout, QVBoxLayout, QMessageBox,
                             QLineEdit, QTableWidget, QTableWidgetItem,
                             QGridLayout, QScrollArea, QPlainTextEdit,
                             QDesktopWidget, QLabel, QRadioButton,
                             QGroupBox)
from PyQt5.QtGui import QFont
from dictionaries import Dict
sys.path.insert(0, '../Teamprojekt')
from Teamprojekt_FastaSuche import*  # NOQA: E402


class logic:
    # Aufgabe a) + b)

    # Aufgabe a) + b)
    def protein_dictionary(fastaFile):
        thisdict = {}
        protein_dict = {}
        with open(fastaFile) as file_content:
            for seqs in file_content:
                if seqs.startswith('>'):
                    bounds = find_all_indexes(seqs, '|')
                    if len(bounds) != 0:
                        key = (seqs[bounds[0]+1:bounds[1]])
                        descr_upper_index = seqs.find('OS')
                        description = (seqs[bounds[1]+1:descr_upper_index])
                        stringValue = "Proteinname: " + description + "\nProtein:\n"
                        stringKeyForProteinDict = ""
                        nextLine = next(file_content)
                        while not nextLine.startswith('>'):
                            stringValue += nextLine
                            stringKeyForProteinDict += nextLine
                            nextLine = next(file_content)
                        thisdict[key] = stringValue
                        protein_dict[stringKeyForProteinDict] = stringValue
        return thisdict, protein_dict


dictionary, protein_dict = protein_dictionary(
    "/home/hris/Documents/iPRG2015_target_decoy_nocontaminants.fasta")

# wird für das protein_dictionary benötigt


def find_all_indexes(input_str, search_str):
    l1 = []
    length = len(input_str)
    index = 0
    while index < length:
        i = input_str.find(search_str, index)
        if i == -1:
            return l1
        l1.append(i)
        index = i + 1
    return l1


class Window(QMainWindow):

    dictionary, protein_dict = logic.protein_dictionary(
        "/home/hris/Documents/iPRG2015_target_decoy_nocontaminants.fasta")

    def __init__(self):
        super().__init__()
        self.setFixedSize(650, 550)
        self.initUI()

    def initUI(self):
        # creating Action loadAct
        # when selected loads a file which is a fasta data
        # first implement with exit action to test if is working
        # later when the loading alg is ready implement correctly

        # creating Buttons
        width = 800
        heightPro = 100
        heightID = 500
        self.searchButtonP = QtWidgets.QPushButton(self)
        self.searchButtonP.setText("search")
        self.searchButtonP.move(width, heightPro)

        self.searchButtonP.clicked.connect(self.clickprotein)

        # creating testboxes for the buttons
        self.boxPro = QLineEdit(self)
        self.boxPro.move(width-280, heightPro)
        self.boxPro.resize(280, 30)

        # create a textfield for the result after a protein search
        self.resultBox = QPlainTextEdit(self)
        self.resultBox.setReadOnly(True)

        # creating Table
        self.table2 = QtWidgets.QTableWidget()
        self.table2.setRowCount(20)
        self.table2.setColumnCount(2)
        # naming the header of the Table
        self.table2.setItem(0, 1, QTableWidgetItem("Protein Name"))
        self.table2.setItem(0, 0, QTableWidgetItem("ID"))
        # Set QTableWidget to not be Editable
        self.table2.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Layout
        self.mainwidget = QWidget(self)
        self.main_layout = QVBoxLayout(self.mainwidget)
        # every set contains all widgets on the level they should be in the UI
        # in set1 there is a textbox and a button
        self.set1 = QHBoxLayout()
        self.set1.addWidget(self.boxPro)
        self.set1.addWidget(self.searchButtonP)

        # set 2 contains the radiobuttons
        self.set2 = QHBoxLayout()
        self.radioname = QRadioButton("Name")
        self.radioid = QRadioButton("ID")
        self.radioseq = QRadioButton("sequence")
        self.radioname.setChecked(True)
        self.set2.addWidget(self.radioname)
        self.set2.addWidget(self.radioid)
        self.set2.addWidget(self.radioseq)
        self.set2.addStretch(1)
        # set 3 contains the table and the result box
        self.set3 = QHBoxLayout()
        self.set3.addWidget(self.table2)
        self.set3.addWidget(self.resultBox)

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

        self.center()
        self.show()

        # centering the widget
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # defining the clickprotein method for the searchButtonP

    def clickprotein(self):

        protein_accession = self.boxPro.text()
        if protein_accession in dictionary:
            self.resultBox.clear()
            self.resultBox.insertPlainText(dictionary.get(protein_accession))
        else:
            self.resultBox.clear()
            self.resultBox.insertPlainText("No matching protein accession found in database.\n")


def main():

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
