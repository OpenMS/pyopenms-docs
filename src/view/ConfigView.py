from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, \
    QTreeWidgetItem, QFileDialog, QPushButton, QHBoxLayout, \
    QDesktopWidget, QMainWindow, QPlainTextEdit, QCheckBox, QHeaderView
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse


class ConfigView(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.tree = ET.ElementTree
        self.header = ['Name', 'Value', 'Type', 'Restrictions']
        self.descriptions = {}

        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setHeaderLabels(self.header)
        self.header = self.treeWidget.header()
        self.header.resizeSection(0, 150)
        self.header.resizeSection(1, 150)
        self.header.resizeSection(2, 150)
        # self.header.setMinimumSectionSize(50)

        self.treeWidget.itemSelectionChanged.connect(self.loadDescription)

        btns = QWidget(self)
        # loadbtn = QPushButton('Load')
        # savebtn = QPushButton('Save')
        # loadbtn.clicked.connect(self.openXML)
        # savebtn.clicked.connect(self.saveFile)

        self.checkbox = QCheckBox('Show advanced parameters')
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.drawTree)

        self.textbox = QPlainTextEdit(self)
        self.textbox.setReadOnly(True)

        btnlayout = QVBoxLayout()
        layout = QVBoxLayout()

        btnlayout.addWidget(self.checkbox)
        btns.setLayout(btnlayout)

        layout.addWidget(self.treeWidget, 6)
        layout.addWidget(self.textbox, 1)
        layout.addWidget(btns, 0.5)

        self.setLayout(layout)
        self.resize(500, 720)

    def openXML(self):
        """
        Loads a XML file with .ini tag, parses the xml into ET.ElementTree
        calls the drawTree function to draw a Tree with the loaded xml
        """
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;ini (*.ini)")
        if file:
            self.tree = parse(file)
            self.drawTree()

            self.header.setSectionResizeMode(QHeaderView.ResizeToContents)

    def generateTreeWidgetItem(self, item: ET.Element) -> QTreeWidgetItem:
        """
        generates a QTreeWidgetItem with each column for an
        ET.Element (e.g. root)
        """
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
        """
        Main function of this widget:
        Draws a tree for the loaded XML file
        The checkbox "show advanced options" is implemented here aswell
        it will only draw those items, which have the according advanced flag
        """
        try:
            self.treeWidget.clear()
            root = self.tree.getroot()
            for child in root:
                if self.checkbox.isChecked():
                    childitem = self.generateTreeWidgetItem(child)
                    self.treeWidget.addTopLevelItem(childitem)
                else:
                    try:
                        if child.attrib['advanced'] == 'false':
                            childitem = self.generateTreeWidgetItem(child)
                            self.treeWidget.addTopLevelItem(childitem)
                    except KeyError:
                        childitem = self.generateTreeWidgetItem(child)
                        self.treeWidget.addTopLevelItem(childitem)

                for sub1child in child:
                    if self.checkbox.isChecked():
                        sub1childitem = self.generateTreeWidgetItem(sub1child)
                        childitem.addChild(sub1childitem)
                    else:
                        try:
                            if sub1child.attrib['advanced'] == 'false':
                                sub1childitem = self.generateTreeWidgetItem(
                                    sub1child)
                                childitem.addChild(sub1childitem)
                        except KeyError:
                            sub1childitem = self.generateTreeWidgetItem(
                                sub1child)
                            childitem.addChild(sub1childitem)

                    for sub2child in sub1child:
                        if self.checkbox.isChecked():
                            sub2childitem = (
                                self.generateTreeWidgetItem(sub2child))
                            sub1childitem.addChild(sub2childitem)
                        else:
                            try:
                                if sub2child.attrib['advanced'] == 'false':
                                    sub2childitem = (
                                        self.generateTreeWidgetItem(sub2child))
                                    sub1childitem.addChild(sub2childitem)
                            except KeyError:
                                sub2childitem = (
                                    self.generateTreeWidgetItem(sub2child))
                                sub1childitem.addChild(sub2childitem)

                        for sub3child in sub2child:
                            if self.checkbox.isChecked():
                                sub3childitem = (
                                    self.generateTreeWidgetItem(sub3child))
                                sub2childitem.addChild(sub3childitem)
                            else:
                                try:
                                    if sub3child.attrib['advanced'] == 'false':
                                        sub3childitem = (
                                            self.generateTreeWidgetItem(
                                                sub3child))
                                        sub2childitem.addChild(sub3childitem)
                                except KeyError:
                                    sub3childitem = (
                                        self.generateTreeWidgetItem(sub3child))
                                    sub2childitem.addChild(sub3childitem)

                            for sub4child in sub3child:
                                if self.checkbox.isChecked():
                                    sub4childitem = (
                                        self.generateTreeWidgetItem(sub4child))
                                    sub3childitem.addChild(sub4childitem)
                                else:
                                    try:
                                        if (sub4child.attrib['advanced']
                                           == 'false'):
                                            sub4childitem = (
                                                self.generateTreeWidgetItem(
                                                    sub4child))
                                            sub3childitem.addChild(
                                                sub4childitem)
                                    except KeyError:
                                        sub4childitem = (
                                            self.generateTreeWidgetItem(
                                                sub4child))
                                        sub3childitem.addChild(sub4childitem)
            self.treeWidget.expandAll()
        except TypeError:
            pass

    def loadDescription(self):
        """
        Shows the description of the configuration parameter in the textbox
        """
        getSelected = self.treeWidget.selectedItems()
        if getSelected:
            try:
                node = getSelected[0].text(0)
                self.textbox.setPlainText(self.descriptions[node])
            except KeyError:
                node = getSelected[0].parent().text(0)
                self.textbox.setPlainText(self.descriptions[node])

    def saveFile(self):
        print('sollte noch speichern')
