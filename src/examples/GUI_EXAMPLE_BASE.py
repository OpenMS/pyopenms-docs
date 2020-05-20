import sys

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QAction

pg.setConfigOption("background", "w")  # white background
pg.setConfigOption("foreground", "k")  # black peaks


class GUI_EXAMPLE_BASE(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(800, 601)
        self._initUI()

    def _initUI(self):
        self.setWindowTitle("Example Widget Viewer")
        self.centerWidget = QWidget(self)
        self.setCentralWidget(self.centerWidget)
        self.layout = QVBoxLayout(self.centerWidget)

        self._setMainMenu()
        self._setExitButton()

    def _setMainMenu(self):
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        self.titleMenu = mainMenu.addMenu("PyOpenMS")

    def _setExitButton(self):
        exitButton = QAction("Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(self.close)
        self.titleMenu.addAction(exitButton)

    def closeEvent(self, event):
        event.accept()

    def setExampleWidget(self, widget):
        self.widget = widget
        self.layout.addWidget(self.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GUI_EXAMPLE_BASE()
    ex.show()
    sys.exit(app.exec_())
