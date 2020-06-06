from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QPushButton, QCheckBox


# erzeugt unsere Tabelle
class TableView(QTableWidget):

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setRowCount(20)
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(['Check', 'Filename', 'Label', 'Group', 'Fractions', 'Comments', ''])
        self.setItem(0, 1, QTableWidgetItem("0,1"))
        self.setItem(1, 1, QTableWidgetItem("1,1"))

        # Fügt in jede Zeile eine Checkbox hinzu
        for index in range(self.rowCount()):
            checkbox = QCheckBox(self)
            self.setCellWidget(index, 0, checkbox)

        # Fügt zu jeder Zeile einen Edit Button hinzu
        for index in range(self.rowCount()):
            editBtn = QPushButton(self)
            editBtn.setText('Edit')
            self.setCellWidget(index, 6, editBtn)

    # setzt die Verhaltensweisen der Spalten
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
