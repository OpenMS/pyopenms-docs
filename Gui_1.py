import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QMainWindow,
                             QAction, qApp, QApplication,
                             QHBoxLayout, QVBoxLayout, QMessageBox,
                             QLineEdit, QTableWidget, QTableWidgetItem,
                             QGridLayout, QScrollArea)
from PyQt5.QtGui import QFont


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 1000)
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

        #width = self.frameGeometry().width()
        #height = self.frameGeometry().height()
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

        # creating Table
        self.table1 = QtWidgets.QTableWidget()
        self.table1.setRowCount(10)
        self.table1.setColumnCount(4)

        self.table1.setItem(0, 0, QTableWidgetItem("Protein Name"))
        self.table1.setItem(0, 1, QTableWidgetItem("Protein Sqeuence"))
        self.table1.setItem(0, 2, QTableWidgetItem("ID"))

        # Layout
        self.mainwidget = QWidget(self)
        self.main_layout = QGridLayout(self.mainwidget)
        self.main_layout.addWidget(self.table1, 1, 0)
        self.main_layout.addWidget(self.boxPro, 0, 1)
        self.main_layout.addWidget(self.boxID, 1, 1)
        self.main_layout.addWidget(self.searchButtonP, 0, 2)

        self.main_layout.addWidget(self.searchButtonID, 1, 2)
        self.mainwidget.setLayout(self.main_layout)
        self.setCentralWidget(self.mainwidget)

        self.setWindowTitle('Protein Viewer')
        self.show()

    def clickprotein(self):
        textboxValue = self.boxPro.text()
        QMessageBox.question(self, "textboxmessage",
                             "you typed " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        boxPro.setText("")


def main():

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
