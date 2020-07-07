import sys
import webbrowser
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QPushButton, QFileDialog
from mzTabTableWidget import Window as mz

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "mzTabTableWidget"
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 500

        self.vBox = QVBoxLayout()

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.mzTabTableWidget = mz()

        self.loadButton = QtWidgets.QPushButton(self)
        self.loadButton.setText("load")
        self.loadButton.clicked.connect(self.loadFile)

        self.vBox.addWidget(self.loadButton)
        self.vBox.addWidget(self.mzTabTableWidget)

        self.setLayout(self.vBox)
        self.show()

    def loadFile(self):
        self.filename = QFileDialog.getOpenFileName()
        self.mzTabTableWidget.readFile(self.filename[0])

# the following is here to test the widget on its own, leave it commented if you want to use it elsewhere
"""
if __name__== '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
"""