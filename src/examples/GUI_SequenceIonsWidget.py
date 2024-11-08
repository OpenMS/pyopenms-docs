import sys
from GUI_EXAMPLE_BASE import GUI_EXAMPLE_BASE
from PyQt5.QtWidgets import QApplication
sys.path.insert(0, "../view")
from SequenceIonsWidget import SequenceIonsWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GUI_EXAMPLE_BASE()  # plain QMainWindow with basic layout and menu bar
    example_widget = SequenceIonsWidget(ex)
    example_widget.setPeptide("HLDKIDMLKSLD")
    example_widget.setPrefix(
        {1: ["a1", "b1", "c1"], 3: ["a3", "b3", "c3"], 5: ["a3", "b3", "c3"]}
    )
    example_widget.setSuffix(
        {1: ["x1", "x3"], 2: ["x2", "y2"], 4: ["x4", "y4", "z4"]})
    ex.setExampleWidget(example_widget)
    ex.show()
    sys.exit(app.exec_())
