import sys

import numpy as np
from GUI_EXAMPLE_BASE import GUI_EXAMPLE_BASE
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, "../view")
from ErrorWidget import ErrorWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GUI_EXAMPLE_BASE()  # plain QMainWindow with basic layout and menu bar

    # add example widget to window
    example_widget = ErrorWidget(ex)
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.array([-2, 3, -8, -4, 3, 12, -15, 10, 5, -12])
    green = (0, 255, 0)
    purple = (128, 0, 255)
    c = np.array(
        [green, purple, green, purple, green, purple, green, purple, green, green]
    )
    example_widget.setMassErrors(x, y, c)
    ex.setExampleWidget(example_widget)
    ex.show()
    sys.exit(app.exec_())
