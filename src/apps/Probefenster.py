import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QDesktopWidget, QWidget
from PyQt5.QtCore import Qt
sys.path.insert(0, '../view')
from OverallView import OverallView


class Programm1(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        # erzeugt unsere Ansicht
        view = OverallView(self)

        self.setCentralWidget(view)

        self.resize(1280, 720)
        self.center()
        self.setWindowTitle('Programm1')
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Programm1()
    sys.exit(app.exec_())
