from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QFileDialog,\
    QPushButton, QHBoxLayout
import xml.etree.ElementTree as ET


class ConfigView(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.tree = ET.ElementTree
        self.initXMLView = QTreeWidget()

        self.buttons = QWidget()
        loadbtn = QPushButton('Load Project')
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(loadbtn)
        loadbtn.clicked.connect(self.openXML)
        self.buttons.setLayout(buttonlayout)

        layout = QVBoxLayout()

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

    def drawTree(self):
        for row in self.tree:
            rowItem = QTreeWidgetItem()
            rowItem.setText(0, row)
            for subRow in row:
                subRowItem = QTreeWidgetItem(rowItem)
                subRowItem.setText(0, subRow)
