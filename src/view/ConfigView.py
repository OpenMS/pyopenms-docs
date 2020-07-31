from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, \
    QTreeWidgetItem, QFileDialog, QPushButton, QHBoxLayout, \
    QPlainTextEdit, QCheckBox, QHeaderView, QMessageBox, \
    QInputDialog
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
from functools import partial


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
        self.loadbtn.setToolTip("Load a .ini file to display and " +
                                "modify the configuration of your processing.")

        self.savebtn = QPushButton('Save')
        self.savebtn.setMaximumWidth(80)
        self.savebtn.clicked.connect(self.saveFile)
        self.savebtn.setToolTip("Save the modified " +
                                "configuration as .ini file.")

        self.checkbox = QCheckBox('Show advanced parameters')
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.drawTreeInit)
        self.checkbox.setToolTip("Shows or hides parameters, " +
                                 "which are tagged as advance in " +
                                 "the .ini configuration file.")

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

    def dragDropEvent(self, files: list):
        """
        Gets the input from the main Application.
        The function chooses if the dragged files are
        valid for the ConfigView Widget
        """
        if len(files) > 1:
            QMessageBox.about(self, "Warning",
                              "Please only use one file")
        else:
            if ".ini" not in files[0]:
                QMessageBox.about(self, "Warning",
                                  "Please only use .ini files.")
            else:
                file = str(files[0])
                self.generateTreeModel(file)

    def openXML(self):
        """
        Loads a XML file with .ini tag, parses the xml into ET.ElementTree
        calls the drawTree function to draw a Tree with the loaded xml
        """
        file, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;ini (*.ini)")
        if file:
            self.generateTreeModel(file)

    def generateTreeModel(self, file: str):
        """
        Function to parse the xml .ini file to a tree model
        Also initialises the TreeWidget
        """
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
        self.additembtns = {}
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
        self.header.setSectionResizeMode(QHeaderView.ResizeToContents)
        for btn in self.additembtns.keys():
            self.additembtns[btn].clicked.connect(
                partial(self.addItemToItemList, btn))
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

            if subnode.tag == "ITEMLIST":
                newbtn = QPushButton('Add New')
                newbtn.setFixedSize(100, 20)
                newbtn.setToolTip("Add new Item to the Itemlist, " +
                                  "according to type and restrictions.")
                listname = subnode.attrib['name']
                self.additembtns[listname] = newbtn
                self.treeWidget.setItemWidget(subitem, 1,
                                              self.additembtns[listname])

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
                changeditemindex = itemparent.indexOfChild(itemchanged)
                parentname = itemparent.text(self.NAMECOL)
                parentres = itemparent.text(self.RESTRICTIONCOL)
                parenttype = itemparent.text(self.TYPECOL)
                itemname = itemchanged.text(self.NAMECOL)
                newvalue = itemchanged.text(self.VALUECOL)
                restrictions = itemchanged.text(self.RESTRICTIONCOL)
                types = itemchanged.text(self.TYPECOL)

                parentcheck = False
                for itemlist in self.tree.iter('ITEMLIST'):
                    if str(itemlist.attrib['name']) == str(parentname):
                        parentcheck = True

                if parentcheck:
                    reschecked = self.checkRestrictionString(
                        newvalue, parentres)
                    typechecked = self.checkTypeRestrictions(
                        newvalue, parenttype)
                else:
                    reschecked = self.checkRestrictionString(
                        newvalue, restrictions)
                    typechecked = self.checkTypeRestrictions(
                        newvalue, types)

                if reschecked and typechecked:
                    for parent in self.tree.iter('NODE'):
                        if parent.attrib['name'] == parentname:
                            for child in parent:
                                if child.attrib['name'] == itemname:
                                    child.attrib['value'] = newvalue
                    for parent in self.tree.iter('ITEMLIST'):
                        if parent.attrib['name'] == parentname:
                            for child, childindex in zip(parent,
                                                         range(len(parent))):
                                if childindex == changeditemindex:
                                    child.attrib['value'] = newvalue
                elif typechecked and not reschecked:
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
            if "-file" in types:
                typechecked = True
            else:
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

    def addItemToItemList(self, parentnodename: str):
        """
        Adds new Item to a ItemList parent, both in etree model and QTreeWidget
        """
        newdata, ok = QInputDialog.getText(self, "Add new row to List",
                                           "Please input the new Parameter," +
                                           "which should be added.")
        if ok:
            if newdata != "":
                for itemlist in self.tree.iter('ITEMLIST'):
                    if itemlist.attrib['name'] == parentnodename:
                        try:
                            restrictions = itemlist.attrib['restrictions']
                            reschecked = self.checkRestrictionString(
                                newdata, restrictions)
                        except KeyError:
                            reschecked = True
                        try:
                            types = itemlist.attrib['type']
                            typechecked = self.checkTypeRestrictions(
                                newdata, types)
                        except KeyError:
                            typechecked = True
                        if reschecked and typechecked:
                            newelement = ET.Element(
                                "LISTITEM", {'value': newdata})
                            itemlist.append(newelement)
                        elif typechecked and not reschecked:
                            QMessageBox.about(
                                self, "Warning", "Please only, " +
                                "modify according to Restrictions")
                        else:
                            QMessageBox.about(
                                self, "Warning", "Please only, " +
                                "modify according to Typerestrictions")
                self.drawTreeInit()

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
