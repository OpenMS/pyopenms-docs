import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QMainWindow,
                             QAction, qApp, QApplication,
                             QHBoxLayout, QVBoxLayout, QMessageBox,
                             QLineEdit, QTableWidget, QTableWidgetItem,
                             QGridLayout, QScrollArea, QPlainTextEdit,
                             QDesktopWidget, QLabel)
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
    "/home/caro/Downloads/iPRG2015_target_decoy_nocontaminants.fasta")

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
        "/home/caro/Downloads/iPRG2015_target_decoy_nocontaminants.fasta")

    def __init__(self):
        super().__init__()
        self.setFixedSize(650, 550)
        self.initUI()

    def initUI(self):
        # creating Action loadAct
        # when selected loads a file which is a fasta data
        # first implement with exit action to test if is working
        # later when the loading alg is ready implement correctly
        loadAct = QAction('load File', self)
        loadAct.setShortcut('Ctrl+O')
        loadAct.setStatusTip('load file')
        loadAct.triggered.connect(qApp.quit)
        # setting a menu bar

        menubar = self.menuBar()
        # file menu
        self.fileMenu = menubar.addMenu("File")
        # adding actions to file menu
        self.fileMenu.addAction(loadAct)

        # creating Buttons
        width = 800
        heightPro = 100
        heightID = 500
        self.searchButtonP = QtWidgets.QPushButton(self)
        self.searchButtonP.setText("search")
        self.searchButtonP.move(width, heightPro)

        self.searchButtonP.clicked.connect(self.clickprotein)
        self.searchButtonID = QPushButton(self)
        self.searchButtonID.setText("search")
        self.searchButtonID.move(width, heightID)

        # creating testboxes for the buttons
        self.boxPro = QLineEdit(self)
        self.boxPro.move(width-280, heightPro)
        self.boxPro.resize(280, 30)

        self.boxID = QLineEdit(self)
        self.boxID.move(width-280, heightID)
        self.boxID.resize(280, 30)
        # create a textfield for the result after a protein search
        self.resultBox = QPlainTextEdit(self)
        self.resultBox.setReadOnly(True)

        # creating Table
        self.table2 = QtWidgets.QTableWidget()
        self.table2.setRowCount(20)
        self.table2.setColumnCount(3)
        # naming the header of the Table
        self.table2.setItem(0, 0, QTableWidgetItem("Protein Name"))
        self.table2.setItem(0, 1, QTableWidgetItem("Protein Sqeuence"))
        self.table2.setItem(0, 2, QTableWidgetItem("ID"))

        # creatingLabels
        self.l1 = QLabel()
        self.l2 = QLabel()
        self.l1.setText("Enter protein acession:")
        self.l2.setText("Enter peptide sequence:")

        # Layout
        self.mainwidget = QWidget(self)
        self.main_layout = QGridLayout(self.mainwidget)
        self.main_layout.addWidget(self.l1, 0, 0)
        self.main_layout.addWidget(self.l2, 3, 0)
        self.main_layout.addWidget(self.resultBox, 2, 0)
        self.main_layout.addWidget(self.boxPro, 1, 0)
        self.main_layout.addWidget(self.boxID, 4, 0)
        self.main_layout.addWidget(self.searchButtonP, 1, 1)
        self.main_layout.addWidget(self.searchButtonID, 4, 1)
        self.main_layout.addWidget(self.table2, 5, 0)
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setRowStretch(0, 1)

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
