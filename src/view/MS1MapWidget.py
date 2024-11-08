import numpy as np
import pyopenms
import pyqtgraph as pg
from pyqtgraph import PlotWidget


class MS1MapWidget(PlotWidget):
    def __init__(self, parent=None, dpi=100):
        PlotWidget.__init__(self)
        self.setLabel("bottom", "m/z")
        self.setLabel("left", "RT")

    def setSpectra(self, msexperiment):
        msexperiment.updateRanges()

        # resolution: mz_res Da in m/z, rt_res seconds in RT dimension
        mz_res = 1.0
        rt_res = 1.0

        # size of image
        cols = 1.0 / mz_res * msexperiment.getMaxMZ()
        rows = 1.0 / rt_res * msexperiment.getMaxRT()

        # create regular spaced data to turn spectra into an image
        """se_comment: max_intensity was never used"""
        """max_intensity = msexperiment.getMaxInt()"""
        bilip = pyopenms.BilinearInterpolation()
        tmp = bilip.getData()
        tmp.resize(int(rows), int(cols), float())
        bilip.setData(tmp)

        bilip.setMapping_0(0.0, 0.0, rows - 1, msexperiment.getMaxRT())
        bilip.setMapping_1(0.0, 0.0, cols - 1, msexperiment.getMaxMZ())

        img = pg.ImageItem(autoDownsample=True)
        self.addItem(img)

        for spec in msexperiment:
            if spec.getMSLevel() == 1:
                mzs, ints = spec.get_peaks()
                rt = spec.getRT()
                for i in range(0, len(mzs)):
                    bilip.addValue(rt, mzs[i], ints[i])  # slow

        data = np.ndarray(shape=(int(cols), int(rows)), dtype=np.float64)
        grid_data = bilip.getData()
        for i in range(int(rows)):
            for j in range(int(cols)):
                data[j][i] = grid_data.getValue(i, j)  # slow

        # Set a custom color map
        pos = np.array([0.0, 0.01, 0.05, 0.1, 1.0])
        color = np.array(
            [
                (255, 255, 255, 0),
                (255, 255, 0, 255),
                (255, 0, 0, 255),
                (0, 0, 255, 255),
                (0, 0, 0, 255),
            ],
            dtype=np.ubyte,
        )
        cmap = pg.ColorMap(pos, color)
        img.setLookupTable(cmap.getLookupTable(0.0, 1.0, 256))
        img.setImage(data)
