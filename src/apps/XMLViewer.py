import sys, os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QDesktopWidget, QWidget, QPushButton, QAction
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

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        saveAction = QAction("&Save File", self)
        loadAction = QAction("&Load File", self)

        saveAction.setDisabled(True)

        fileMenu.addAction(loadAction)
        fileMenu.addAction(saveAction)

        loadAction.triggered.connect(cview.openXML)
        saveAction.triggered.connect(cview.saveFile)

        self.setCentralWidget(cview)
        self.resize(800, 1000)
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
