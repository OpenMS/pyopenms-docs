import sys, os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QDesktopWidget, QWidget, QPushButton
from PyQt5.QtCore import Qt
sys.path.append(os.getcwd()+'/../view')
from ConfigView import ConfigView


class XMLViewer(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        '''
        sets the window with all applications and widgets
        '''
        cview = ConfigView()

        self.setCentralWidget(cview)
        self.resize(1280, 720)
        self.center()
        self.setWindowTitle('ini File Viewer')
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
    ex = XMLViewer()
    sys.exit(app.exec_())
