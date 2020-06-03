from PyQt5.QtWidgets import QHBoxLayout, QWidget
from TableView import TableView
from ButtonView import ButtonView


#kombiniert unsere Tabelle und unsere Buttons in ein Widget
class OverallView(QWidget):

    def __init__(self, *args):
        QWidget.__init__(self, *args)

        layout = QHBoxLayout()

        #lade beide Widgets
        table = TableView()
        buttons = ButtonView()

        #setzte die Widgets ins gewünschte layout rein
        layout.addWidget(table)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.resize(1280, 720)