import sys, os, glob
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, \
     QTabWidget, QAction, QInputDialog, QMessageBox, QFileDialog, \
     QWidget, QLabel, QVBoxLayout, QCheckBox, QHBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt
sys.path.append(os.getcwd()+'/../view')
from GUI_FastaViewer import GUI_FastaViewer # noqa E402
from ConfigView import ConfigView # noqa E402
from mzMLTableView import mzMLTableView # noqa E402
from MultipleSpecView import MultipleSpecView # noqa E402
from mzTabTableWidget import Window as mzTabTableWidget # noqa E402
sys.path.append(os.getcwd() + '/../model')
from tableDataFrame import TableDataFrame as Tdf  # noqa E402
sys.path.append(os.getcwd() + '/../controller')
from filehandler import FileHandler as fh  # noqa E402
sys.path.insert(0, '../examples')


class ProteinQuantification(QMainWindow):
    """
    Application to use different Widgets in one Window:
    First Tab: Welcome tab with information about how the GUI works.
    Second Tab: Config view - here the .ini file can be viewed and edited
    Third Tab: mzMLTable view - the experimental design can be
    viewed and edited.
    Fourth Tab: Fasta view - fasta files can be loaded and inspected
    Fifth Tab: Spec view - ms spectras from loaded mzML files can be seen
    and inspected
    Sixth Tab: mzTabTable view - The result of the ProteomicsLFQ
    is displayed

    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()
        self.initVars()
        # flag for themetoggle
        self.flag = False
        # self.palette = self.palette()
        self.setPalette(self.palette)
        self.setTheme()

    def initUI(self):
        '''
        sets the window with all applications and widgets
        '''
        self.view = QTabWidget()
        self.welcome = QWidget()
        self.cview = ConfigView()
        self.tview = mzMLTableView()
        self.sview = MultipleSpecView()
        self.fview = GUI_FastaViewer()
        self.xview = mzTabTableWidget()

        self.view.addTab(self.welcome, 'Welcome')
        self.view.addTab(self.cview, 'XML-Viewer')
        self.view.addTab(self.tview, 'Experimental-Design')
        self.view.addTab(self.fview, 'Fasta-Viewer')
        self.view.addTab(self.sview, 'Spec-Viewer')
        self.view.addTab(self.xview, 'mzTab-Viewer')

        self.palette = QPalette()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        projectMenu = menubar.addMenu('Project')
        parametersMenu = menubar.addMenu('Parameters')
        loadAction = QAction(QIcon("Icons/load_icon.png"),
                             "&Load Project", self)
        loadAction.setShortcut("Ctrl+L")
        saveAction = QAction(QIcon("Icons/save_icon.png"),
                             "&Save Project", self)
        saveAction.setShortcut("Ctrl+S")
        runAction = QAction(QIcon("Icons/run_icon.png"),
                            "&Run in Terminal", self)
        runAction.setShortcut("Ctrl+R")
        Threads = QAction("&Adjust the Threadnumber", self)
        FDR = QAction("&Adjust the protein FDR", self)
        Out = QAction("&Choose outputfiles", self)

        projectMenu.addAction(loadAction)
        projectMenu.addAction(saveAction)
        projectMenu.addAction(runAction)
        parametersMenu.addAction(Threads)
        parametersMenu.addAction(FDR)
        parametersMenu.addAction(Out)

        runAction.triggered.connect(self.runFunction)
        FDR.triggered.connect(self.adjustFDR)
        Threads.triggered.connect(self.adjustThreads)
        Out.triggered.connect(self.chooseOutputfiles)

        saveAction.triggered.connect(self.saveFunction)
        loadAction.triggered.connect(self.loadFunction)

        # themeswitcher
        settingsMenu = menubar.addMenu('Settings')
        switchThemeAction = QAction('Change Theme', self)
        settingsMenu.addAction(switchThemeAction)
        switchThemeAction.triggered.connect(self.switchTheme)

        # Welcome Tab

        normalFont = QFont("Helvetica", 11)
        boldFont = QFont("Helvetica", 14, QFont.Bold)
        title = QLabel()
        title.setText("Welcome: Get started with your Proteinquantifcation!")
        title.setFont(boldFont)
        title.setMaximumHeight(30)
        welcome = QLabel()
        welcome.setText("This application performs a ProteomicsLFQ "
                        "Proteinquantification. \nThe files, needed to "
                        "run have to be loaded into "
                        "the first three tabs,\nnamed: XML-Viewer, "
                        "Experimental-Design, Fasta-Viewer \nThe result "
                        "will then be displayed in the last tab: "
                        "mzTab-Viewer.\n"
                        "If you want to look at the spectras used for the "
                        "quantification\ngive the Spec-Viewer tab a visit.\n\n"
                        "Following tabs are part of this application:\n")
        welcome.setFont(normalFont)

        xmlText = QLabel()

        xmlText.setText("XML Viewer: This application allows you to load, edit"
                        " and save your\nconfiguration file for"
                        "your Experiment. If no config file is present "
                        "a\ndefault file is written and used. "
                        "You can also modify that configuration\n"
                        "file if needed. "
                        "The configurationfile should be a .ini file.")
        xmlText.setFont(normalFont)

        experimentalText = QLabel()
        experimentalText.setText("Experimental Design: Here a table of your"
                                 " experimental design can\nbe loaded, "
                                 "and modified. "
                                 "You are able to edit specifics like number\n"
                                 "of files, fractions or groups.\n.tsv files"
                                 "can be directly loaded as table or single "
                                 ".mzml files can be\nincluded and the design "
                                 "set manually.")
        experimentalText.setFont(normalFont)

        fastaText = QLabel()
        fastaText.setText("Fasta Viewer: This viewer allows the user to load "
                          "a fasta file\nand search for information about the"
                          "sequences such as\nprotein IDs and accession"
                          " numbers.")
        fastaText.setFont(normalFont)

        specText = QLabel()
        specText.setText("Spectrum Viewer: The Spectrum Viewer enables you to "
                         "look at\nthe mzML spectras your Mass Spectrometer "
                         "measured for your\nsamples. It loads all "
                         "spectrafiles, which are located in your "
                         "projectfolder.")
        specText.setFont(normalFont)
        iconOpenMs = QPixmap("../view/IconOpenMS.png")
        iconLabel = QLabel()
        iconLabel.setPixmap(iconOpenMs)
        welcome_layout = QVBoxLayout()
        welcome_layout.addWidget(title)
        welcome_layout.addWidget(welcome)
        welcome_layout.addWidget(xmlText)
        welcome_layout.addWidget(experimentalText)
        welcome_layout.addWidget(fastaText)
        welcome_layout.addWidget(specText)
        welcome_layout.setSpacing(1)

        central_layout = QHBoxLayout()
        central_layout.addLayout(welcome_layout)
        central_layout.addWidget(iconLabel)
        self.welcome.setLayout(central_layout)

        self.setCentralWidget(self.view)
        self.resize(1280, 720)
        self.center()
        self.setWindowTitle('Protein Quantification')
        self.show()

    def initVars(self):
        """
        initiates usable variables
        """
        self.ini_loaded = False
        self.tablefile_loaded = False
        self.fasta_loaded = False
        self.mztab_loaded = False
        self.cxml_out = True
        self.msstats_out = True

        self.loaded_dir = ""
        self.loaded_ini = ""
        self.loaded_table = ""
        self.loaded_fasta = ""
        self.loaded_mztab = ""

        self.threads = 1
        self.fdr = 0.3
        self.procdone = False

    def center(self):
        """
        centers the widget to the screen
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def chooseOutputfiles(self):
        """
        Opens a popup window to choose the outputfiles
        If output is generated checkbox is checked.
        """
        # Popup
        self.outputCheckBoxWindow = PopupWindow()
        mainWidget = QWidget()
        mztabCheckbox = QCheckBox("Generate a mzTab outputfile")
        cxmlCheckbox = QCheckBox("Generate a cxml outputfile")
        msstatsCheckbox = QCheckBox("Generate a msstats outputfile")
        layout = QVBoxLayout()
        layout.addWidget(mztabCheckbox)
        layout.addWidget(cxmlCheckbox)
        layout.addWidget(msstatsCheckbox)
        mainWidget.setLayout(layout)
        self.outputCheckBoxWindow.setCentralWidget(mainWidget)
        self.outputCheckBoxWindow.setTitle("Choose Outputfiles")

        # Checkboxstates
        mztabCheckbox.setChecked(True)
        mztabCheckbox.setEnabled(False)

        if self.cxml_out:
            cxmlCheckbox.setChecked(True)

        if self.msstats_out:
            msstatsCheckbox.setChecked(True)

        # Change Checkbox
        cxmlCheckbox.clicked.connect(self.togglecxml)
        msstatsCheckbox.clicked.connect(self.togglemsstats)

    def togglecxml(self):
        if self.cxml_out:
            self.cxml_out = False
        else:
            self.cxml_out = True

    def togglemsstats(self):
        if self.msstats_out:
            self.msstats_out = False
        else:
            self.msstats_out = True

    def adjustFDR(self):
        """
        The user is allowed to change th FDR
        """
        newfdr, ok = QInputDialog.getDouble(
            self, "Adjust the value for the protein FDR",
            "Please specify a double as new FDR value")
        if ok:
            if newfdr > 0:
                if newfdr <= 1:
                    self.fdr = newfdr
                else:
                    QMessageBox.about(self, "Warning",
                                      "Please specify a value" +
                                      "between 0.0 and 1.0 for the FDR.")
            else:
                QMessageBox.about(self, "Warning",
                                  "Please specify a positive" +
                                  "value for the FDR.")

    def adjustThreads(self):
        """
        The user is allowed to change the number of threads
        """
        newthreads, ok = QInputDialog.getInt(
            self, "Adjust the number of threads",
            "Please specify the number of threads for the processing")
        if ok:
            if newthreads > 0:
                self.threads = newthreads
            else:
                QMessageBox.about(self, "Warning",
                                  "Please specify a positive" +
                                  "number of threads.")

    def runFunction(self):
        """
        runs the processing from the GUI in a Terminal
        based on the ProteomicsLFQ command of OpenMS
        """
        self.procdone = False
        outfileprefix, ok = QInputDialog.getText(self,
                                                 "Prefix for outputfiles",
                                                 "Please specify a prefix " +
                                                 "for the outputfiles")
        if ok:
            projectfolder = self.loaded_dir
            mzMLExpLayout = self.tview.getDataFrame()
            try:
                mzMLfiles = mzMLExpLayout['Spectra_Filepath']
                idXMLfiles = []
                for mzML in mzMLfiles:
                    temp = mzML.split(".")
                    idXML = temp[0] + ".idXML"
                    idXMLfiles.append(idXML)
                mzMLidXMLdefined = True
            except KeyError:
                QMessageBox.about(self, "Warning", "Please load or " +
                                  "create an Experimental Design first")
                mzMLidXMLdefined = False

            expdesign = self.loaded_table
            dbfasta = self.loaded_fasta
            inifile = self.loaded_ini

            if mzMLidXMLdefined:
                runcall = "ProteomicsLFQ "
                mzMLs = "-in " + " ".join(mzMLfiles)
                idXMLs = " -ids " + " ".join(idXMLfiles)
                design = " -design " + expdesign + " "
                refdb = "-fasta " + dbfasta + " "
                configini = "-ini " + inifile + " "
                threads = "-threads " + str(self.threads) + " "
                fdr = "-proteinFDR " + str(self.fdr) + " "
                out = ""
                if self.cxml_out:
                    out += "-out_cxml " + outfileprefix + ".consensusXML.tmp "
                if self.msstats_out:
                    out += "-out_msstats " + outfileprefix + ".csv.tmp "

                out += "-out " + outfileprefix + ".mzTab.tmp"

                command = (runcall + mzMLs + idXMLs + design +
                           refdb + configini + threads + fdr + out)
                os.chdir(projectfolder)
                os.system(command)
                self.procdone = True
                QMessageBox.about(self, "Information", "Processing has been " +
                                  "performed and outputfiles saved to " +
                                  "projectfolder")
                mztabfile = outfileprefix + ".mzTab.tmp"
                try:
                    self.xview.readFile(mztabfile)
                    self.loaded_mztab = mztabfile
                    self.mztab_loaded = True
                    self.view.setCurrentWidget(self.xview)
                except FileNotFoundError:
                    QMessageBox.about(self, "Warning", "Some Error occurred " +
                                      "and no mzTab could be found.")

    def saveFunction(self):
        """
        saves all work from the GUI in chosen folder
        the prefix of the outputfiles can be choosen
        """
        dlg = QFileDialog(self)
        filePath = dlg.getExistingDirectory()

        if filePath:
            filePath = filePath + "/"
            tablePath = ""
            ok = False
            table_empty = self.tview.table.rowCount() <= 0

            if table_empty:
                tablePath = ""
                self.tablefile_loaded = False
                self.tview.tablefile_loaded = False

            if self.tablefile_loaded is False and table_empty is False \
                    and self.tview.tablefile_loaded is False:
                prefix, ok = QInputDialog.getText(
                      self, "Prefix for outputfiles",
                      "Please specify a prefix " +
                      "for the outputfiles")
            if ok:
                tablePath = filePath + prefix + "_design.tsv"
                self.loaded_table = prefix + "_design.tsv"
                self.tablefile_loaded = True

            if self.tablefile_loaded and self.tview.tablefile_loaded is False:
                tablePath = filePath + self.loaded_table

            if self.tview.tablefile_loaded:
                tablePath = filePath + self.tview.loaded_table

            if (ok or self.tablefile_loaded or self.tview.tablefile_loaded) \
                    and table_empty is False:
                df = Tdf.getTable(self.tview)
                fh.exportTable(self.tview, df, tablePath, "tsv")

            xmlPath = filePath + self.loaded_ini
            try:
                self.cview.tree.write(xmlPath)
            except TypeError:
                print("No Config loaded to be saved!")

            if self.loaded_ini != "" and tablePath.split("/")[-1] != "":
                QMessageBox.about(self, "Successfully saved!",
                                        "Files have been saved as: " +
                                        self.loaded_ini + ", " +
                                        tablePath.split("/")[-1])
            elif self.loaded_ini != "":
                QMessageBox.about(self, "Successfully saved!",
                                        "ini has been saved as: " +
                                        self.loaded_ini)
            elif tablePath.split("/")[-1] != "":
                QMessageBox.about(self, "Successfully saved!",
                                        "Table has been saved as: " +
                                        tablePath.split("/")[-1])

    def loadFunction(self, file):
        """
        loads all files (.tsv .ini, .fasta) from a given
        directory.
        If .tsv file is not present the experimental design is
        filled with mzMl files

        If no .ini file is present default ini file is written
        and is loaded automatically
        """
        dlg = QFileDialog(self)
        filePath = dlg.getExistingDirectory()
        self.loaded_dir = filePath
        self.sview.fillTable(filePath)
        if filePath != '':
            try:
                self.tsvfiles = glob.glob('*.tsv')
                if len(self.tsvfiles) > 1:
                    QMessageBox.about(self, "Sorry!",
                                            "Where are multiple .tsv "
                                            "files in the specified folder. "
                                            "Please choose the one supposed "
                                            "to be used")
                    dial = QFileDialog(self)
                    newFilePath = dial.getOpenFileName(self,
                                                       "Choose .tsv",
                                                       filePath,
                                                       "Tables (*.tsv)")
                    if newFilePath[0] != '':
                        newFile = newFilePath[0].split("/")[-1]
                        self.tsvfiles = [newFile]
                    else:
                        QMessageBox.about(self, "Sorry!",
                                                "Nothing was choosen. "
                                                "Therefor no .tsv was "
                                                "loaded. ")
                        self.tsvfiles = []
                for file in self.tsvfiles:
                    df = fh.importTable(self.tview, file)
                    Tdf.setTable(self.tview, df)
                    self.tview.drawTable()
                    self.loaded_table = file
                    self.tablefile_loaded = True

            except TypeError:
                "No tsv or csv file could be loaded."

            if self.tablefile_loaded is False:
                try:
                    self.tview.loadDir(filePath)
                    self.tablefile_loaded = True
                except TypeError:
                    print("Could not load .mzMl files")

            try:
                self.iniFiles = glob.glob('*.ini')
                if len(self.iniFiles) > 1:
                    QMessageBox.about(self, "Sorry!",
                                            "There are multiple .ini "
                                            "files in the specified folder. "
                                            "Please choose the one supposed "
                                            "to be used")
                    dial = QFileDialog(self)
                    newFilePath = dial.getOpenFileName(self,
                                                       "Choose .ini",
                                                       filePath,
                                                       "Config (*.ini)")
                    if newFilePath[0] != '':
                        newFile = newFilePath[0].split("/")[-1]
                        self.iniFiles = [newFile]
                    else:
                        QMessageBox.about(self, "Sorry!",
                                                "Nothing was choosen. "
                                                "Therefore, no .ini was "
                                                "loaded. ")
                        self.iniFiles = []
                for file in self.iniFiles:
                    self.cview.generateTreeModel(file)
                    self.loaded_ini = file
                    self.ini_loaded = True
            except TypeError:
                print("Could not load .ini file")

            if self.ini_loaded is False:
                try:
                    runcall = "ProteomicsLFQ "
                    writeIniFile = "-write_ini "
                    out = "Config.ini"
                    command = (runcall + writeIniFile + out)
                    os.chdir(filePath)
                    os.system(command)
                    iniFiles = glob.glob('*.ini')
                    for file in iniFiles:
                        self.cview.generateTreeModel(file)
                        self.loaded_ini = file
                        self.ini_loaded = True
                except TypeError:
                    print("Could not write and load default ini file.")

            try:
                self.fastafiles = glob.glob('*fasta')
                if len(self.fastafiles) > 1:
                    self.multipleFilesPopup("fasta")
                    """
                    QMessageBox.about(self, "Sorry!",
                                            "There are multiple .fasta "
                                            "files in the specified folder. "
                                            "Please choose the one supposed "
                                            "to be used")
                    dial = QFileDialog(self)
                    newFilePath = dial.getOpenFileName(self,
                                                       "Choose .fasta",
                                                       filePath,
                                                       "Proteindata (*.fasta)")
                    if newFilePath[0] != '':
                        newFile = newFilePath[0].split("/")[-1]
                        self.fastafiles = [newFile]
                    else:
                        QMessageBox.about(self, "Sorry!",
                                                "Nothing was choosen. "
                                                "Therefore, no .fasta was "
                                                "loaded. ")
                        self.fastafiles = []
                    """
                for file in self.fastafiles:
                    self.fview.loadFile(file)
                    self.loaded_fasta = file
                    self.fasta_loaded = True
            except TypeError:
                print("Could not load .fasta file")

    def setTheme(self):
        """
        sets theme based on flag state, light or dark modes are possible
        default is light theme
        """
        p = self.palette
        if not self.flag:
            # lightmode
            p.setColor(QPalette.Window, QColor(202, 202, 202))
            p.setColor(QPalette.WindowText, Qt.black)
            p.setColor(QPalette.Base, QColor(230, 230, 230))
            p.setColor(QPalette.AlternateBase, QColor(202, 202, 202))
            p.setColor(QPalette.ToolTipBase, Qt.black)
            p.setColor(QPalette.ToolTipText, Qt.black)
            p.setColor(QPalette.Text, Qt.black)
            p.setColor(QPalette.Button, QColor(202, 202, 202))
            p.setColor(QPalette.ButtonText, Qt.black)
            p.setColor(QPalette.BrightText, Qt.red)
            p.setColor(QPalette.Link, QColor(213, 125, 37))
            p.setColor(QPalette.Highlight, QColor(213, 125, 37))
            p.setColor(QPalette.HighlightedText, Qt.white)
        else:
            # darkmode
            p.setColor(QPalette.Window, QColor(53, 53, 53))
            p.setColor(QPalette.WindowText, Qt.white)
            p.setColor(QPalette.Base, QColor(25, 25, 25))
            p.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            p.setColor(QPalette.ToolTipBase, Qt.white)
            p.setColor(QPalette.ToolTipText, Qt.white)
            p.setColor(QPalette.Text, Qt.white)
            p.setColor(QPalette.Button, QColor(53, 53, 53))
            p.setColor(QPalette.ButtonText, Qt.white)
            p.setColor(QPalette.BrightText, Qt.red)
            p.setColor(QPalette.Link, QColor(42, 130, 218))
            p.setColor(QPalette.Highlight, QColor(42, 130, 218))
            p.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(p)

    def switchTheme(self):
        """
        Toggles between dark and light theme
        """

        self.flag = not self.flag
        self.setTheme()


class PopupWindow(QMainWindow):
    """
    Popup window with checkboxes for outputfiles
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(300, 100)
        self.center()
        self.show()

    def center(self):
        """
        centers the widget to the screen
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setTitle(self, title: str):
        self.setWindowTitle(title)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ProteinQuantification()
    app.setStyle("Fusion")
    print(ex.flag)
    sys.exit(app.exec_())
