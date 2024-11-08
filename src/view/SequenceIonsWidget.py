from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import (
    QFont,
    QFontMetricsF,
    QPainter,
    QColor,
    QPen,
    QBrush,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtWidgets import QWidget, QHBoxLayout


class SequenceIonsWidget(QWidget):
    """
    Used for creates a window for a peptide sequence with its given ions,
    which is adjusted to the sequence size.
    To avoid contortions of the window, spaceritems are added.

    """

    HEIGHT = 0
    WIDTH = 0
    SUFFIX_HEIGHT = 0

    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.initUI()

    def initUI(self):
        self.mainlayout = QHBoxLayout(self)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.container = QWidget(self)
        self.container.setStyleSheet("background-color:white;")

        self.setWindowTitle("SequenceIons Viewer")
        self.seqIons_layout = QHBoxLayout(self.container)

        # change default setting of 11 px
        self.seqIons_layout.setContentsMargins(0, 0, 0, 0)
        self._pep = observed_peptide()
        # resize window to fit peptide size
        self.resize()

        self._pep.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self._pep.setMinimumSize(
            SequenceIonsWidget.WIDTH, SequenceIonsWidget.HEIGHT)
        self.seqIons_layout.addItem(
            QSpacerItem(
                40,
                SequenceIonsWidget.HEIGHT,
                QSizePolicy.MinimumExpanding,
                QSizePolicy.Minimum,
            )
        )
        self.seqIons_layout.addWidget(self._pep)
        self.seqIons_layout.addItem(
            QSpacerItem(
                40,
                SequenceIonsWidget.HEIGHT,
                QSizePolicy.MinimumExpanding,
                QSizePolicy.Minimum,
            )
        )

        self.setFixedHeight(SequenceIonsWidget.HEIGHT)
        self.mainlayout.addWidget(self.container)
        self.show()

    def resize(self):
        """
        The integer 8 represents the additional space needed
        for the in addition drawn lines. The 18 represents the
        monospace width.

        """
        if len(self._pep.sequence) == 0:
            SequenceIonsWidget.WIDTH = 0
        else:
            SequenceIonsWidget.WIDTH = \
                (len(self._pep.sequence) * 18) + \
                (len(self._pep.sequence) - 1) * 8
        self.calculateHeight()

    def calculateHeight(self):
        """
        Calculate window height adjusting to sequence height
        with possible ions and set default setting in case of no
        ions.

        """
        prefix = self._pep.prefix
        suffix = self._pep.suffix

        if suffix == {}:
            max_ion_suff = 1
        else:
            max_ion_suff = len(
                suffix[max(suffix, key=lambda key: len(suffix[key]))])

        if prefix == {}:
            max_ion_pre = 1
        else:
            max_ion_pre = len(
                prefix[max(prefix, key=lambda key: len(prefix[key]))])

        metrics_pep = QFontMetricsF(self._pep.getFont_Pep())
        height_pep = metrics_pep.height()

        metrics_ion = QFontMetricsF(self._pep.getFont_Ion())
        height_ion = metrics_ion.height()

        # window height calculated with the sum of max prefix and suffix height
        height_ion_pre = height_ion * max_ion_pre + 15
        SequenceIonsWidget.SUFFIX_HEIGHT = height_ion * max_ion_suff + 5
        SequenceIonsWidget.HEIGHT = \
            (
                height_pep + height_ion_pre + SequenceIonsWidget.SUFFIX_HEIGHT
            )

    def setPeptide(self, seq):
        self._pep.setSequence(seq)
        self.updateWindow()

    def setSuffix(self, suff):
        self._pep.setSuffix(suff)
        self.updateWindow()

    def setPrefix(self, pre):
        self._pep.setPrefix(pre)
        self.updateWindow()

    def updateWindow(self):
        self.resize()
        self._pep.setMinimumSize(
            SequenceIonsWidget.WIDTH, SequenceIonsWidget.HEIGHT)
        self.setFixedHeight(SequenceIonsWidget.HEIGHT)
        self.update()

    def clear(self):
        self._pep.sequence = ""
        self._pep.suffix = {}
        self._pep.prefix = {}
        self.update()


class observed_peptide(QWidget):
    """
    Used for creates a peptide sequence with its given ions.
    The ions can be stacked above each other, e.g. in case for
    a1, b1. Each amino letter is also separated by a line
    and prefixes are colored blue, otherwise suffixes are colored
    red.

    """

    def __init__(self):
        QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.sequence = ""
        self.suffix = {}
        self.prefix = {}
        self.colors = {
            "black": QColor(0, 0, 0),
            "red": QColor(255, 0, 0),
            "blue": QColor(0, 0, 255),
        }

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
        qp.fillRect(event.rect(), QBrush(Qt.white))  # or changed to Qt.white
        self._drawPeptide(qp)
        qp.end()

    def _drawPeptide(self, qp):
        qp.setWindow(0, 0, SequenceIonsWidget.WIDTH, SequenceIonsWidget.HEIGHT)
        qp.setPen(self.colors["black"])
        qp.setFont(self.getFont_Pep())
        self._fragmentPeptide(qp)

    def _fragmentPeptide(self, qp):
        """
        In this function the sequence will be created stepwise.
        Each char of the sequence is drawn separately to add the
        lines between and the ions.

        1. Check if sequence is given, if so
        then transform seq into a dictionary
        (with the indices representing the positions of the chars).
        2. For each char in the sequence:
            First, calculate start position of char
            (be aware that the char rect is created
            at the left bottom corner of
            the char, meaning we have to add the height of the Font
            & possible suffixes to the starting height position
            to move it into the center of the window).

            Secound, calculate the center point for the vertical Line.
            The Line consists of a point start and point end.
            The starting line xPos yield in the
            start_point + blank - (SPACE/2),
            where blank represents the additional
            space from the starting point after each new char.

            Third, if prefix or suffix ions are given,
            then distinguish between suffix and prefix to draw the vertical
            line with either left or right line or both.

            Because of changing the fonts for the ions,
            the fonts needs to be reset.

        """
        SPACE = 8

        if self.sequence != "":

            seq = list(self.sequence)
            dict_seq = {i: seq[i] for i in range(0, len(seq))}

            metrics = QFontMetricsF(self.getFont_Pep())

            blank = 0
            for i, s in dict_seq.items():
                i_rev = self._getReverseIndex(i, dict_seq)

                width = metrics.boundingRect(s).width()
                height = metrics.boundingRect(s).height()

                start_point = 0

                # position of char with center indent
                position = QPointF(
                    start_point + blank,
                    SequenceIonsWidget.SUFFIX_HEIGHT + height
                )
                qp.drawText(position, s)

                # position lines for possible ions
                centerOfLine = \
                    (
                        SequenceIonsWidget.SUFFIX_HEIGHT + height - height / 4
                    ) - 1

                start_linePos = QPointF(
                    start_point + blank - (SPACE / 2),
                    centerOfLine - height / 2 - 2.5
                )
                end_linePos = QPointF(
                    start_linePos.x(), centerOfLine + height / 2 + 2.5
                )

                qp.setFont(self.getFont_Ion())
                metrics_ion = QFontMetricsF(self.getFont_Ion())

                if i in self.prefix:
                    left_linePos = self._drawIonsLines(
                        qp, start_linePos, end_linePos, SPACE, "prefix"
                    )
                    self._drawPrefixIon(qp, i, metrics_ion, left_linePos)

                # for given line of existing prefix, expand with given suffix
                if i in self.prefix and i_rev in self.suffix:
                    right_linePos = self._drawIonsLines(
                        qp, start_linePos, end_linePos, SPACE, "suffix"
                    )
                    self._drawSuffixIon(
                        qp, i_rev, metrics_ion, end_linePos, right_linePos
                    )

                elif i_rev in self.suffix and i not in self.prefix:
                    right_linePos = self._drawIonsLines(
                        qp, start_linePos, end_linePos, SPACE, "suffix"
                    )
                    self._drawSuffixIon(
                        qp, i_rev, metrics_ion, start_linePos, right_linePos
                    )

                blank += width + SPACE
                qp.setPen(self._getPen(self.colors["black"]))
                qp.setFont(self.getFont_Pep())

    def _drawPrefixIon(self, qp, index, metrics_ion, pos_left):
        qp.setPen(self._getPen(self.colors["blue"]))
        prefix_ions = sorted(self.prefix[index])
        blank_ion = 10

        for ion in prefix_ions:
            height_ion = metrics_ion.boundingRect(ion).height()
            pos_ion = QPointF(pos_left.x(), pos_left.y() + blank_ion)
            qp.drawText(pos_ion, ion)
            blank_ion += height_ion

    def _drawSuffixIon(
            self,
            qp,
            index_reverse,
            metrics_ion,
            pos_end,
            pos_right):
        qp.setPen(self._getPen(self.colors["red"]))
        suffix_ions = sorted(self.suffix[index_reverse], reverse=True)
        blank_ion = 5

        for ion in suffix_ions:
            height_ion = metrics_ion.boundingRect(ion).height()
            pos_ion = QPointF(pos_end.x() + 2.5, pos_right.y() - blank_ion)
            qp.drawText(pos_ion, ion)
            blank_ion += height_ion

    def _drawIonsLines(self, qp, pos_start, pos_end, SPACE, order):
        qp.setPen(self._getPen(self.colors["black"]))

        if order == "prefix":
            qp.drawLine(pos_start, pos_end)
            pos_left = QPointF(pos_end.x() - 2 * SPACE, pos_end.y())
            qp.drawLine(pos_end, pos_left)
            return pos_left

        if order == "suffix":
            qp.drawLine(pos_start, pos_end)
            pos_right = QPointF(pos_start.x() + 2 * SPACE, pos_start.y())
            qp.drawLine(pos_start, pos_right)
            return pos_right

    def getFont_Pep(self):
        font = QFont("Courier")
        font.setStyleHint(QFont.TypeWriter)
        font.setPixelSize(30)
        return font

    def getFont_Ion(self):
        font = QFont("Courier")
        font.setStyleHint(QFont.TypeWriter)
        font.setPixelSize(10)
        return font

    def _getPen(self, color):
        # style settings for the lines
        pen = QPen(color, 0.75, Qt.SolidLine)
        pen.setStyle(Qt.DashDotLine)
        return pen

    def _getReverseIndex(self, i, dict_seq):
        i_rev = 0
        if i != 0:
            i_rev = list(dict_seq.keys())[-i]
        return i_rev
