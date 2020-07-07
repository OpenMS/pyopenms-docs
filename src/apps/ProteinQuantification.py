import sys, os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, \
     QDesktopWidget, QWidget, QTabWidget, QAction, QPushButton
from PyQt5.QtCore import pyqtSlot
sys.path.append(os.getcwd()+'/../view')
from GUI_FastaViewer import GUI_FastaViewer
from ConfigView import ConfigView
from mzMLTableView import mzMLTableView
from SpecViewer import Specviewer


class ProteinQuantification(QMainWindow):
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
        tview = mzMLTableView()
        sview = Specviewer()
        fview = GUI_FastaViewer()
        # xview = ()

        view.addTab(cview, 'XML-Viewer')
        view.addTab(tview, 'Experimental-Design')
        view.addTab(fview, 'Fasta-Viewer')
        view.addTab(sview, 'Spec-Viewer')
        # view.addTab(xView, 'Viewer')

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('Project')
        saveAction = QAction("&Save project", self)
        runAction = QAction("&Run", self)

        saveAction.setDisabled(True)
        runAction.setDisabled(True)

        fileMenu.addAction(runAction)
        fileMenu.addAction(saveAction)

        self.setCentralWidget(view)
        self.resize(1280, 720)
        self.center()
        self.setWindowTitle('Protein Quantification')
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
    ex = ProteinQuantification()
    sys.exit(app.exec_())
