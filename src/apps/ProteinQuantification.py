import sys, os, glob
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, \
     QTabWidget, QAction, QInputDialog, QMessageBox, QFileDialog
sys.path.append(os.getcwd()+'/../view')
from GUI_FastaViewer import GUI_FastaViewer
from ConfigView import ConfigView
from mzMLTableView import mzMLTableView
from MultipleSpecView import MultipleSpecView
from mzTabTableWidget import Window as mzTabTableWidget
sys.path.append(os.getcwd() + '/../model')
from tableDataFrame import TableDataFrame as Tdf  # noqa E402
sys.path.append(os.getcwd() + '/../controller')
from filehandler import FileHandler as fh  # noqa E402


class ProteinQuantification(QMainWindow):
    """
    Application to use different Widgets in one Window
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()
        self.initVars()

    def initUI(self):
        '''
        sets the window with all applications and widgets
        '''
        self.view = QTabWidget()
        self.cview = ConfigView()
        self.tview = mzMLTableView()
        self.sview = MultipleSpecView()
        self.fview = GUI_FastaViewer()
        self.xview = mzTabTableWidget()

        self.view.addTab(self.cview, 'XML-Viewer')
        self.view.addTab(self.tview, 'Experimental-Design')
        self.view.addTab(self.fview, 'Fasta-Viewer')
        self.view.addTab(self.sview, 'Spec-Viewer')
        self.view.addTab(self.xview, 'mzTabViewer')

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        projectMenu = menubar.addMenu('Project')
        parametersMenu = menubar.addMenu('Parameters')
        loadAction = QAction("&Load Project", self)
        saveAction = QAction("&Save project", self)
        runAction = QAction("&Run in Terminal", self)
        Threads = QAction("&Adjust the Threadnumber", self)
        FDR = QAction("&Adjust the protein FDR", self)

        # saveAction.setDisabled(True)
        # runAction.setDisabled(True)
        projectMenu.addAction(loadAction)
        projectMenu.addAction(runAction)
        projectMenu.addAction(saveAction)
        parametersMenu.addAction(Threads)
        parametersMenu.addAction(FDR)

        runAction.triggered.connect(self.runFunktion)
        FDR.triggered.connect(self.adjustFDR)
        Threads.triggered.connect(self.adjustThreads)

        saveAction.triggered.connect(self.saveFunktion)
        loadAction.triggered.connect(self.loadFunction)

        # self.initDefaultValues()

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
        # self.spec_loaded = True
        # self.mztab_loaded = True

        self.loaded_dir = ""
        self.loaded_ini = ""
        self.loaded_table = ""
        self.loaded_fasta = ""
        # self.loaded_spec = ""
        # self.loaded_mztab = ""

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

    def runFunktion(self):
        """
        runs the processing from the GUI in a Terminal
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
                out = ("-out_cxml " + outfileprefix + ".consensusXML.tmp " +
                       "-out_msstats " + outfileprefix + ".csv.tmp " +
                       "-out " + outfileprefix + ".mzTab.tmp")
                command = (runcall + mzMLs + idXMLs + design +
                           refdb + configini + threads + fdr + out)
                os.chdir(projectfolder)
                os.system(command)
                self.procdone = True
                QMessageBox.about(self, "Information", "Processing has been " +
                                  "performed and outputfiles saved to " +
                                  "projectfolder")
                self.xview.readFile(outfileprefix + ".mzTab.tmp")
                self.view.setCurrentWidget(self.xview)

    def saveFunktion(self):
        """
        saves all work from the GUI in chosen folder
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

    def loadFunction(self):
        """
        loads all files (.tsv .ini, .fasta) from a given
        directory.
        If .tsv file is not present the experimental design is
        filled with mzMl files

        If no .ini file is present default ini file is written
        and has to be loaded with the button inside tab
        """
        dlg = QFileDialog(self)
        filePath = dlg.getExistingDirectory()
        self.loaded_dir = filePath
        self.sview.fillTable(filePath)

        try:
            if filePath != '':
                tsvfiles = glob.glob('*.tsv')
                for file in tsvfiles:
                    df = fh.importTable(self.tview, file)
                    Tdf.setTable(self.tview, df)
                    self.tview.drawTable()
                    self.loaded_table = file
                    self.tablefile_loaded = True
        except TypeError:
            "No tsv or csv file could be loaded."

        if self.tablefile_loaded is False:
            try:
                if filePath != '':
                    self.tview.loadDir(filePath)
                    self.tablefile_loaded = True
            except TypeError:
                print("Could not load .mzMl files")

        try:
            if filePath != '':
                iniFiles = glob.glob('*.ini')
                for file in iniFiles:
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

                if filePath != '':
                    iniFiles = glob.glob('*.ini')
                    for file in iniFiles:
                        self.cview.generateTreeModel(file)
                        self.loaded_ini = file
                        self.ini_loaded = True
            except TypeError:
                print("Could not write and load default ini file.")

        try:
            if filePath != '':
                fastafiles = glob.glob('*fasta')
                for file in fastafiles:
                    self.fview.loadFile(file)
                    self.loaded_fasta = file
                    self.fasta_loaded = True
        except TypeError:
            print("Could not load .fasta file")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ProteinQuantification()
    sys.exit(app.exec_())
