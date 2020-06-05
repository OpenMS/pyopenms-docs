from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget


# erzeugt unser Buttonwidget
class ButtonView(QWidget):

    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.buttonLayout = QVBoxLayout(self)

        # leere Buttons im gewünschten Layout
        self.buttonLayout.addWidget(QPushButton('Load'))
        self.buttonLayout.addWidget(QPushButton('Save'))
        self.buttonLayout.addWidget(QPushButton('Label'))
        self.buttonLayout.addWidget(QPushButton('Auto-Label'))
        self.buttonLayout.addWidget(QPushButton('Group'))
        self.buttonLayout.addWidget(QPushButton('Auto-Group'))

        self.resize(200, 690)
