import sys

import pyopenms
from GUI_EXAMPLE_BASE import GUI_EXAMPLE_BASE
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, "../view")
from ScanBrowserWidget import ScanBrowserWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GUI_EXAMPLE_BASE()  # plain QMainWindow with basic layout and menu bar

    # load spectra and add example widget to window
    exp = pyopenms.MSExperiment()
    example_widget = ScanBrowserWidget()
    example_widget.loadFile("../data/190509_Ova_native_25ngul_R.mzML")
    ex.setExampleWidget(example_widget)
    ex.show()
    sys.exit(app.exec_())
