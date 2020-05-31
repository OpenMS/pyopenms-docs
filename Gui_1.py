import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QMainWindow,
                             QAction, qApp, QApplication,
                             QHBoxLayout, QVBoxLayout, QMessageBox,
                             QLineEdit)
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
        fileMenu = menubar.addMenu("File")
        # adding actions to file menu
        fileMenu.addAction(loadAct)

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

        boxPro = QLineEdit(self)
        boxPro.move(width-280, heightPro)
        boxPro.resize(280, 30)

        boxID = QLineEdit(self)
        boxID.move(width-280, heightID)
        boxID.resize(280, 30)
        #self.resize(1000, 1000)
        self.setWindowTitle('Protein Viewer')
        self.show()

        def clickprotein(self):
            textboxValue = boxPro.text()
            QMessageBox.question(self, "textboxmessage",
                                 "you typed " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)

        #self.resize(1000, 1000)
        self.setWindowTitle('Protein Viewer')
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
