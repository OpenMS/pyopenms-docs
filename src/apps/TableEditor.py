import sys, os
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QDesktopWidget, QWidget
from PyQt5.QtCore import Qt
sys.path.append(os.getcwd()+'/../view')
from mzMLTableView import mzMLTableView


class TableEditor(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        '''
        sets the window with all applications and widgets
        '''
        view = mzMLTableView(self)

        self.setCentralWidget(view)

        self.resize(1280, 720)
        self.center()
        self.setWindowTitle('ExperimentalDesign')
        self.show()

    def center(self):
        """
        centers the widget to the screen
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = TableEditor()
    sys.exit(app.exec_())
    