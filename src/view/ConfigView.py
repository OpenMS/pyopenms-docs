from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, \
    QTreeWidgetItem, QFileDialog, QPushButton, QHBoxLayout, \
    QPlainTextEdit, QCheckBox, QHeaderView
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
        loadbtn = QPushButton('Load')
        loadbtn.setMaximumWidth(80)
        savebtn = QPushButton('Save')
        savebtn.setMaximumWidth(80)
        loadbtn.clicked.connect(self.openXML)
        savebtn.clicked.connect(self.saveFile)

        self.checkbox = QCheckBox('Show advanced parameters')
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.drawTreeInit)

        self.textbox = QPlainTextEdit(self)
        self.textbox.setReadOnly(True)

        btnlayout = QHBoxLayout()
        layout = QVBoxLayout()

        btnlayout.addWidget(loadbtn)
        btnlayout.addWidget(savebtn)
        btnlayout.addWidget(self.checkbox)
        btns.setLayout(btnlayout)
        btns.setFixedWidth(500)
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
            self.root = self.tree.getroot()
            self.drawTreeInit()

            self.header.setSectionResizeMode(QHeaderView.ResizeToContents)

    def generateTreeWidgetItem(self, item: ET.Element) -> QTreeWidgetItem:
        """
        generates a QTreeWidgetItem with each column for an
        ET.Element (e.g. root)
        """
        treeitem = QTreeWidgetItem()
        treeitem.setFlags(treeitem.flags() | Qt.ItemIsEditable)
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

    def drawTreeInit(self):
        """
        Initialises the treewidget, add the top level item
        and starts the main recursion
        """
        try:
        self.treeWidget.clear()
        root = self.tree.getroot()
        for child in root:
            if self.checkbox.isChecked():
                childitem = self.generateTreeWidgetItem(child)
                self.treeWidget.addTopLevelItem(childitem)
                if len(child.getchildren()) > 0:
                    self.drawTreeRecursive(childitem, child)
            else:
                try:
                    if child.attrib['advanced'] == 'false':
                        childitem = self.generateTreeWidgetItem(child)
                        self.treeWidget.addTopLevelItem(childitem)
                        if len(child.getchildren()) > 0:
                            self.drawTreeRecursive(childitem, child)
                except KeyError:
                    childitem = self.generateTreeWidgetItem(child)
                    self.treeWidget.addTopLevelItem(childitem)
                    if len(child.getchildren()) > 0:
                        self.drawTreeRecursive(childitem, child)
        self.treeWidget.expandAll()

    def drawTreeRecursive(self, nodeitem: QTreeWidgetItem, node: ET.Element):
        """
        Draws a tree for the loaded XML file
        The checkbox "show advanced options" is implemented here as well
        it will only draw those items, which have the according advanced flag
        """
        for subnode in node:
            if self.checkbox.isChecked():
                subitem = self.generateTreeWidgetItem(subnode)
                nodeitem.addChild(subitem)
                if len(subnode.getchildren()) > 0:
                    self.drawTreeRecursive(subitem, subnode)
            else:
                try:
                    if subnode.attrib['advanced'] == 'false':
                        subitem = self.generateTreeWidgetItem(subnode)
                        nodeitem.addChild(subitem)
                        if len(subnode.getchildren()) > 0:
                            self.drawTreeRecursive(subitem, subnode)
                except KeyError:
                    subitem = self.generateTreeWidgetItem(subnode)
                    nodeitem.addChild(subitem)
                    if len(subnode.getchildren()) > 0:
                        self.drawTreeRecursive(subitem, subnode)

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
