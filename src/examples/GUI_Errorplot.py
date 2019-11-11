import sys
from PyQt5.QtWidgets import QApplication
import numpy as np


from GUI_EXAMPLE_BASE import GUI_EXAMPLE_BASE
sys.path.insert(0, '../view')
from ErrorWidget import ErrorWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI_EXAMPLE_BASE() # plain QMainWindow with basic layout and menu bar

    # add example widget to window
    example_widget = ErrorWidget(ex)
    example_widget.setMassErrors(np.array([5, 3, 2]), np.array([10, 40, -12]), {"green":  (0, 255, 0), "purple": (128, 0, 255)})
    example_widget.setColor("green")
    ex.setExampleWidget(example_widget)
    ex.show()
    sys.exit(app.exec_())
