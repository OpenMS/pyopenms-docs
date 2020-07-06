from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, \
    QTreeWidgetItem, QFileDialog, QPushButton, QHBoxLayout, \
    QPlainTextEdit, QCheckBox, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse


class ConfigView(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.initTreeModel()
        self.initTreeWidget()
        self.initUI()

    def initTreeModel(self):
        """
        Initialise the tree model using a fixed header
        Columns are defined as constants
        """
        self.tree = ET.ElementTree
        self.header = ['Name', 'Value', 'Type', 'Restrictions']
        self.NAMECOL = 0
        self.VALUECOL = 1
        self.TYPECOL = 2
        self.RESTRICTIONCOL = 3
        self.descriptions = {}
        self.drawTree = False

    def initTreeWidget(self):
        """
        Initialise the TreeWidget, with corresponding header
        A change listener is implemented and initialised here too
        """
        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setHeaderLabels(self.header)

        self.header = self.treeWidget.header()
        self.header.resizeSection(0, 150)
        self.header.resizeSection(1, 150)
        self.header.resizeSection(2, 150)

        self.treeWidget.itemSelectionChanged.connect(self.loadDescription)
        self.changeListener()

    def initUI(self):
        """
        Initialise the GUI with buttons, checkbox, textbox and treewidget
        """
        self.loadbtn = QPushButton('Load')
        self.loadbtn.setMaximumWidth(80)
        self.loadbtn.clicked.connect(self.openXML)

        self.savebtn = QPushButton('Save')
        self.savebtn.setMaximumWidth(80)
        self.savebtn.clicked.connect(self.saveFile)

        self.checkbox = QCheckBox('Show advanced parameters')
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.drawTreeInit)

        self.textbox = QPlainTextEdit(self)
        self.textbox.setReadOnly(True)

        btnlayout = QHBoxLayout()
        layout = QVBoxLayout()

        btns = QWidget(self)
        btnlayout.addWidget(self.loadbtn)
        btnlayout.addWidget(self.savebtn)
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
        self.drawTreeActive = True
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
        self.drawTreeActive = False

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

    def changeListener(self):
        """
        Change Listener for the tree widget
        to connect the model with the widget
        """
        self.treeWidget.itemChanged.connect(self.editField)

    def editField(self):
        """
        Fields in model are edited upon change of treewidget
        Edit is only allowed if restrictions are checked and type is correct
        """
        if not self.drawTreeActive:
            if self.treeWidget.currentColumn() == self.VALUECOL:
                itemchanged = self.treeWidget.currentItem()
                itemparent = itemchanged.parent()
                itemname = itemchanged.text(self.NAMECOL)
                parentname = itemparent.text(self.NAMECOL)
                newvalue = itemchanged.text(self.VALUECOL)
                restrictions = itemchanged.text(self.RESTRICTIONCOL)
                types = itemchanged.text(self.TYPECOL)

                reschecked = self.checkRestrictionString(newvalue,
                                                         restrictions)
                typechecked = self.checkTypeRestrictions(newvalue, types)

                if reschecked and typechecked:
                    for parent in self.tree.iter('NODE'):
                        if parent.attrib['name'] == parentname:
                            for child in parent:
                                if child.attrib['name'] == itemname:
                                    child.attrib['value'] = newvalue
                elif typechecked:
                    QMessageBox.about(self, "Warning", "Please only, " +
                                      "modify according to Restrictions")
                else:
                    QMessageBox.about(self, "Warning", "Please only, " +
                                      "modify according to Typerestrictions")
            else:
                QMessageBox.about(self, "Warning", "Please only, " +
                                  "modify the Column: value")
            self.drawTreeInit()

    def checkRestrictionString(self,
                               newvalue: type, restrictions: str) -> bool:
        """
        Checks the restrictions of a item are matched when edited
        """
        if restrictions != "":
            if newvalue not in restrictions:
                reschecked = False
            else:
                reschecked = True
        else:
            reschecked = True

        return reschecked

    def checkTypeRestrictions(self, newvalue: type, types: str) -> bool:
        """
        Checks if the edit is corresponding to the type
        """
        if types != "":
            try:
                float(newvalue)
                if len(newvalue.split('.')) == 2:
                    valtype = "double"
                else:
                    valtype = "int"
            except ValueError:
                valtype = "string"
            if valtype not in types:
                typechecked = False
            else:
                typechecked = True
        else:
            typechecked = True

        return typechecked

    def saveFile(self):
        """
        Saves current tree model as .ini file
        """
        file, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "",
            "All Files (*);;ini (*.ini)")
        if file:
            temp = file.split(".")
            if len(temp) < 2:
                file = file + ".ini"
            self.tree.write(file)
