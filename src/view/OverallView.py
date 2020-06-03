from PyQt5.QtWidgets import QHBoxLayout, QWidget
from TableView import TableView
from ButtonView import ButtonView

class OverallView(QWidget):

    def __init__(self, *args):
        QWidget.__init__(self, *args)

        layout = QHBoxLayout()

        table = TableView()
        buttons = ButtonView()

        layout.addWidget(table)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.resize(1280, 720)