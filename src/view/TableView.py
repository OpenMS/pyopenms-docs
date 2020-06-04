from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView


# erzeugt unsere Tabelle
class TableView(QTableWidget):

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setRowCount(20)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(['Check', 'Filename', 'Label', 'Group', 'Fractions', 'Comments'])
        self.setItem(0, 0, QTableWidgetItem("0,0"))
        self.setItem(0, 1, QTableWidgetItem("0,1"))
        self.setItem(1, 1, QTableWidgetItem("1,1"))

    # setzt die Verhaltensweisen der Spalten
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
