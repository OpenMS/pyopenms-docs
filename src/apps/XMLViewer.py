import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, \
     QDesktopWidget
sys.path.append(os.getcwd()+'/../view')
from ConfigView import ConfigView   # noqa E402


class XMLViewer(QMainWindow):
    """
    Widget for visualizing configuration data
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        '''
        sets the window with all applications and widgets
        which are loaded from the ConfigView.py file
        '''
        cview = ConfigView()

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
