import sys
import pyqtgraph as pg
import pyopenms
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QFontMetricsF, QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout


class peptide_window(QWidget):

    HEIGHT = 200
    WIDTH = 400

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setFixedSize(peptide_window.WIDTH, peptide_window.HEIGHT)
        self.setWindowTitle('Peptide Viewer')

        self.layout = QHBoxLayout(self)
        self.pep = observed_peptide()
        self.pep.setSequence("PEPTIDE")
        self.pep.setPrefix([1, 4, 5, 6])
        self.pep.setSuffix([2,3])

        self.layout.addWidget(self.pep)

        self.show()

class observed_peptide(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(self.sizeHint())


    def initUI(self):
        self.sequence = ""
        self.suffix = []
        self.prefix = []


    def setSequence(self, seq):
        self.sequence = seq


    def setSuffix(self, lst):
        self.suffix = lst

    def setPrefix(self, lst):
        self.prefix = lst


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.fillRect(event.rect(), QBrush(Qt.white))
        self.__drawPeptide(qp)
        qp.end()

    def __drawPeptide(self, qp):
        qp.setWindow(0, 0, 400, 200)
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(self.__getFont())

        self.__fragmentPeptide(qp)

    def __fragmentPeptide(self, qp):
        SPACE = 8

        if self.sequence != "":
            dict_seq = {i: list(self.sequence)[i] for i in range(0, len(list(self.sequence)))}
            seq_keys = len(dict_seq.keys())
            dict_seq_last = list(dict_seq.values())[-1]

            metrics = QFontMetricsF(self.__getFont())

            blank = 0
            for i, s in dict_seq.items():
                width = metrics.boundingRect(s).width()
                height = metrics.boundingRect(s).height()

                seq_len = metrics.boundingRect(self.sequence).width()
                start_point = (peptide_window.WIDTH - seq_len - (SPACE * (seq_keys - 1)))/2 + metrics.boundingRect(dict_seq_last).width()/2

                # position of char
                position = QPointF(start_point + blank, (peptide_window.HEIGHT/2 + height/4))
                qp.drawText(position, s)

                pen = QPen(QColor(168, 34, 3), 0.75, Qt.SolidLine)
                pen.setStyle(Qt.DashDotLine)
                qp.setPen(pen)

                center = (peptide_window.HEIGHT / 2)
                pos_start = QPointF(start_point + blank - SPACE/2, center - 50)
                pos_end = QPointF(pos_start.x(), center + 50)

                if i in self.prefix:
                    qp.drawLine(pos_start, pos_end)
                    pos_left = QPointF(pos_end.x() - SPACE, pos_end.y())
                    qp.drawLine(pos_end, pos_left)

                # for given line, expand for prefix
                if i in self.suffix and i in self.prefix:
                    pos_right = QPointF(pos_start.x() + SPACE, pos_start.y())
                    qp.drawLine(pos_start, pos_right)

                elif i in self.suffix and i not in self.prefix:
                    qp.drawLine(pos_start, pos_end)
                    pos_right = QPointF(pos_start.x() + SPACE, pos_start.y())
                    qp.drawLine(pos_start, pos_right)

                blank += width + SPACE


    def __getFont(self):
        font = QFont("Courier")
        font.setStyleHint(QFont.TypeWriter)
        font.setPixelSize(30)
        return font


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = peptide_window()
    sys.exit(app.exec_())
