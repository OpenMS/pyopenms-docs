import sys, os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, \
     QDesktopWidget, QWidget, QTabWidget, QAction, QPushButton
from PyQt5.QtCore import pyqtSlot
sys.path.append(os.getcwd()+'/../view')
from ConfigView import ConfigView
from mzMLTableView import mzMLTableView


class FinalBox(QMainWindow):
    """
    Application to use different Widgets in one Window
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        '''
        sets the window with all applications and widgets
        '''
        view = QTabWidget()
        cview = ConfigView()
        tView = mzMLTableView()
        # sview = ()
        # fview = ()
        # xview = ()

        view.addTab(cview, 'XML-Viewer')
        view.addTab(tView, 'Experimental-Design')
        # view.addTab(sView, 'Spec-Viewer')
        # view.addTab(fView, 'Fasta-Viewer')
        # view.addTab(xView, 'Viewer')

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        saveAction = QAction("&Save File", self)
        loadAction = QAction("&Load File", self)

        saveAction.setDisabled(True)

        fileMenu.addAction(loadAction)
        fileMenu.addAction(saveAction)

        '''
        Hier muss noch vlt ein conditional hin sodass
        die connections sich für das aktuelle tab jeweils 
        ändern
        '''
        loadAction.triggered.connect(cview.openXML)
        saveAction.triggered.connect(cview.saveFile)

        self.setCentralWidget(view)
        self.resize(1280, 720)
        self.center()
        self.setWindowTitle('Final Box')
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
    ex = FinalBox()
    sys.exit(app.exec_())