from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QFileDialog,\
    QPushButton, QHBoxLayout, QDesktopWidget, QMainWindow, QPlainTextEdit
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as ET


class ConfigView(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.tree = ET.ElementTree
        self.header = ['name', 'value', 'type', 'restrictions']
        self.descriptions = {}

        view = QWidget(self)
        self.treeWidget = QTreeWidget(self)
        QTreeWidget.__init__(self.treeWidget)
        self.treeWidget.setHeaderLabels(self.header)

        button = QPushButton('Load')
        button.clicked.connect(self.openXML)

        self.textbox = QPlainTextEdit(self)

        layout = QVBoxLayout()
        layout.addWidget(button, 1)
        layout.addWidget(self.treeWidget, 3)
        layout.addWidget(self.textbox, 1)
        view.setLayout(layout)

        self.setLayout(layout)
        self.resize(500, 720)

    def openXML(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;xml (*.xml)")
        self.tree = ET.parse(file)
        self.drawTree()

    def generateTreeWidgetItem(self, item):
        treeitem = QTreeWidgetItem()
        try:
            treeitem.setText(0, item.attrib['name'])
        except KeyError:
            pass
        try:
            treeitem.setText(1, item.attrib['value'])
        except KeyError:
            pass
        try:
            treeitem.setText(2, item.attrib['type'])
        except KeyError:
            pass
        try:
            treeitem.setText(3, item.attrib['restrictions'])
        except KeyError:
            pass
        try:
            self.descriptions[item.attrib['name']] = item.attrib['description']
        except KeyError:
            pass

        return treeitem

    def drawTree(self):
        root = self.tree.getroot()
        for child in root:
            childitem = self.generateTreeWidgetItem(child)
            self.treeWidget.addTopLevelItem(childitem)
            for sub1child in child:
                sub1childitem = self.generateTreeWidgetItem(sub1child)
                childitem.addChild(sub1childitem)
                for sub2child in sub1child:
                    sub2childitem = self.generateTreeWidgetItem(sub2child)
                    sub1childitem.addChild(sub2childitem)
                    for sub3child in sub2child:
                        sub3childitem = self.generateTreeWidgetItem(sub3child)
                        sub2childitem.addChild(sub3childitem)
                        for sub4child in sub3child:
                            sub4childitem = self.generateTreeWidgetItem(sub4child)
                            sub3childitem.addChild(sub4childitem)
