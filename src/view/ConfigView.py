from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QFileDialog,\
    QPushButton, QHBoxLayout, QDesktopWidget, QMainWindow
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as ET


class ConfigView(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.tree = ET.ElementTree

        view = QWidget(self)
        self.bottom = QTreeWidget(self)
        QTreeWidget.__init__(self.bottom)
        button = QPushButton('something for a button')

        button.clicked.connect(self.openXML)

        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.bottom)
        view.setLayout(layout)

        self.setLayout(layout)
        self.resize(1280, 720)

    def openXML(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;xml (*.xml)")
        self.tree = ET.parse(file)
        self.drawTree()

    def getRoot(self):
        root = self.tree.getroot()

        return root

    def drawTree(self):
        root = self.getRoot()
        rootitem = QTreeWidgetItem()
        rootitem.setText(0, root.attrib[''])
        self.bottom.addTopLevelItem(rootitem)
        """
        for row in self.tree.getiterator():
            rowItem = QTreeWidgetItem()
            rowItem.setText(0, row.tag)
            self.bottom.addTopLevelItem(rowItem)
            for subRow in row.getiterator():
                subRowItem = QTreeWidgetItem(rowItem)
                subRowItem.setText(0, subRow.tag)
        """
