import queue
import random
import threading
import itertools
from functools import reduce, partial
from pathlib import Path
from time import perf_counter
import sys
import os

#from numba import jit
#from numba.experimental import jitclass
#import panel as pn

import bokeh.layouts
import datashader
import numpy as np
from bokeh.models import ColumnDataSource, CustomJS, Button, Select, Div
from bokeh.plotting import curdoc
from holoviews.plotting.util import process_cmap
from holoviews.streams import Selection1D
from numpy import log
from pyopenms import MSExperiment, PeakMap, MzMLFile, PeakFileOptions, SignalToNoiseEstimatorMedian, PeakSpectrum, DRange1, \
    DPosition1, FeatureMap, Feature, PeptideIdentification, PeptideHit, FeatureXMLFile
import pandas as pd

import holoviews as hv
import holoviews.operation.datashader as hd
from holoviews import opts, dim
from tornado import gen


class FeatureMapDF(FeatureMap):
    def __init__(self):
        super().__init__()

    def get_df(self):
        def gen(fmap: FeatureMap, fun):
            for f in fmap:
                yield from fun(f)

        def extractMetaData(f: Feature):
            # subfeatures = f.getFeatureList()  # type: list[FeatureHandle]
            pep = f.getPeptideIdentifications()  # type: list[PeptideIdentification]
            bb = f.getConvexHull().getBoundingBox2D()
            if len(pep) != 0:
                hits = pep[0].getHits()
                if len(hits) != 0:
                    besthit = hits[0]  # type: PeptideHit
                    # TODO what else
                    yield f.getUniqueId(), besthit.getSequence().toString(), f.getCharge(), f.getRT(), f.getMZ(), bb[0][0], bb[1][0], bb[0][1], bb[1][1], f.getOverallQuality(), f.getIntensity()
                else:
                    yield f.getUniqueId(), None, f.getCharge(), f.getRT(), f.getMZ(), bb[0][0], bb[1][0], bb[0][1], bb[1][1], f.getOverallQuality(), f.getIntensity()
            else:
                yield f.getUniqueId(), None, f.getCharge(), f.getRT(), f.getMZ(), bb[0][0], bb[1][0], bb[0][1], bb[1][1], f.getOverallQuality(), f.getIntensity()

        cnt = self.size()

        mddtypes = [('id', np.dtype('uint64')), ('sequence', 'U200'), ('charge', 'i4'), ('RT', 'f'), ('mz', 'f'),
                    ('RTstart', 'f'), ('RTend', 'f'), ('mzstart', 'f'), ('mzend', 'f'),
                    ('quality', 'f'), ('intensity', 'f')]
        mdarr = np.fromiter(iter=gen(self, extractMetaData), dtype=mddtypes, count=cnt)
        return pd.DataFrame(mdarr).set_index('id')

def SpectrumGenerator(file_path):
    q = queue.Queue(maxsize=1)
    JOB_DONE = object()
    TIMEOUT = 30

    def task():
        loader = MzMLFile()
        loadopts = loader.getOptions()  # type: PeakFileOptions
        loadopts.setMSLevels([1])
        loadopts.setSkipXMLChecks(True)
        loadopts.setIntensity32Bit(True)
        loadopts.setIntensityRange(DRange1(DPosition1(10000), DPosition1(sys.maxsize)))
        loader.setOptions(loadopts)
        loader.transform(file_path, MSCallback(q), True, True)
        q.put(JOB_DONE)

    t = threading.Thread(target=task)
    t.start()

    while True:
        # better set a timeout, or if task in sub-threading fails, it will result in a deadlock
        chunk = q.get(timeout=TIMEOUT)
        if chunk is JOB_DONE:
            break
        yield from chunk

    t.join()

#@jit(nopython=True)
def unpack(rt, mzs, intys):
    return [(rt, point[0], point[1]) for point in zip(mzs, intys)]

class MSCallback:
    def __init__(self, q):
        self.q = q

    def setExperimentalSettings(self, s):
        pass

    def setExpectedSize(self, a, b):
        pass

    def consumeChromatogram(self, c):
        pass

    def consumeSpectrum(self, s: PeakSpectrum):
        #if s.getMSLevel() == 2:
            self.q.put((s.getRT(), point[0], point[1]) for point in zip(*s.get_peaks()))

#pn.extension()
hv.extension('bokeh')
renderer = hv.renderer('bokeh').instance(mode='server')
spectradf = pd.DataFrame()

def modify_doc(doc):
    """Add a plotted function to the document.

    Arguments:
        doc: A bokeh document to which elements can be added.
    """

    # Now done with a generator
    exp = MSExperiment() # type: PeakMap
    loader = MzMLFile()
    loadopts = loader.getOptions()  # type: PeakFileOptions
    loadopts.setMSLevels([1])
    loadopts.setSkipXMLChecks(True)
    loadopts.setIntensity32Bit(True)
    loadopts.setIntensityRange(DRange1(DPosition1(10000), DPosition1(sys.maxsize)))
    loader.setOptions(loadopts)

    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        #file = "/Users/pfeuffer/git/OpenMS-fixes-src/share/OpenMS/examples/FRACTIONS/BSA1_F1.mzML"
        #file = "/Volumes/Data/UPS1/mzML/UPS1_250amol_R1.mzML"
        file = str(Path(__file__).resolve().parent) + "/static/data/BSA1.mzML"
        #fxmlfile = None
        fxmlfile = str(Path(__file__).resolve().parent) + "/static/data/BSA1_F1_idmapped.featureXML"

    jsupdateinfo = '''
        renderAllCDS(data, xr.start, xr.end, yr.start, yr.end);
        '''

    # Instead of listening to the range, we require a button press. Much easier and performant.
    #hvplot.state.x_range.js_on_change('start', CustomJS(code=jsupdateinfo))

    # If enabled via args, creates a button to stop the server
    def stopbutton_callback():
        sys.exit()  # Stop the server
    stopbutton = Button(label="Stop server", button_type="danger")
    stopbutton.on_click(stopbutton_callback)

    # Fake selectors that we use to trigger both a python function (for data filtering)
    # and a JS function to update the 3D View with the filtered data
    invisText = Select(title="Option:", value="foo", options=["foo", "bar", "baz", "quux"], visible=False, id="InvisibleText")
    invisText2 = Select(title="Option:", value="bar", options=["foo", "bar", "baz", "quux"], visible=False, id="InvisibleText2")


    js_on_invisText2 = '''
    console.log("js_on_invisText2 triggered")
    Bokeh.documents[0].get_model_by_id("InvisibleText").value = "bar" + new Date().timeNow();
    '''

    invisText2.js_on_change("value", CustomJS(code=js_on_invisText2))

    ## Layout
    doc.title = 'Mass-spectrometry Viewer'

    dynamic_col = bokeh.layouts.column(Div(text="Loading spectra...", width=300, height=150, css_classes=["lds-dual-ring"]), css_classes=["centered"])
    if len(sys.argv) > 2 and sys.argv[2] == "stoppable":
        layout = bokeh.layouts.layout(dynamic_col, [invisText, invisText2, stopbutton], css_classes=["centered"])
    else:
        layout = bokeh.layouts.layout(dynamic_col, [invisText, invisText2], css_classes=["centered"])


    def init_2D_plot_and_update_btn():
        global spectradf
        if spectradf.empty:

            # Start the stopwatch / counter
            t1_start = perf_counter()

            cols = ["RT", "mzarray", "intarray"]
            expandcols = ["RT", "mz", "inty"]

            # On-the-fly: With the on-the-fly parsing we cannot use a count anymore. And a double-pass parse does not
            # make sense if you have to load the full data to count the peaks. Maybe if nr of peaks were annotated.
            # but then we could not filter during load. So this is probably as good as it gets.
            #spectraarr = np.fromiter(SpectrumGenerator(file),
            #                         dtype=[('RT', 'f'), ('mz', 'f'), ('inty', 'f')])

            # InMem:
            # The doublepass for counting seems to be not worth it.
            loader.load(file, exp)
            exp.updateRanges()

            np_stop1 = perf_counter()
            print("Time for loading:",
                  np_stop1 - t1_start)

            ## 2DPeakDataLong version
            spectraarrs2d = exp.get2DPeakDataLong(exp.getMinRT(), exp.getMaxRT(), exp.getMinMZ(), exp.getMaxMZ())

            ## Iter long version
            #spectraarr = np.fromiter(((spec.getRT(), point[0], point[1]) for spec in exp for point in zip(*spec.get_peaks())), dtype=[('RT', 'f'), ('mz', 'f'), ('inty', 'f')])#, count=sum(s.size() for s in exp))

            np_stop = perf_counter()
            print("Time for creating numpy array:",
                  np_stop - np_stop1)

            ## 2D PeakDataLong version
            spectradf = pd.DataFrame(dict(zip(expandcols, spectraarrs2d)))

            ## Iter long version
            #spectradf = pd.DataFrame(data=spectraarr, columns=expandcols)

            # Initial tests showed that loading into numpy array first is faster than direct construction from iter.
            ## Wide version
            # spectradf = pd.DataFrame(data=((spec.getRT(), *spec.get_peaks()) for spec in exp), columns=cols)
            ## Long version (direct DF)
            # spectradf = pd.DataFrame(data=((spec.getRT(), point[0], point[1]) for spec in exp for point in zip(*spec.get_peaks())), columns=expandcols)

            print("Loaded " + str(len(spectradf)) + " peaks.")

            # Stop the stopwatch / counter
            df_stop = perf_counter()
            print("Time for loading and creating DF:",
                  df_stop - np_stop)

        df_stop = perf_counter()
        # spectracds = ColumnDataSource(spectradf)

        points = hv.Points(spectradf, kdims=['RT', 'mz'], vdims=['inty'], label="MS1 survey scans").opts(
            fontsize={'title': 16, 'labels': 14, 'xticks': 6, 'yticks': 12},
            color=log(dim('int')),
            colorbar=True,
            cmap='Magma',
            width=1000,
            height=1000,
            tools=['hover'])

        #rectdata = pd.DataFrame(np.fromiter(((rt - 10, mz - 1, rt + 10, mz + 1) for rt, mz in itertools.product(range(1500, 2400, 10), range(400, 800, 5))), count=int(90*(400/5)), dtype=[('xs','f'),('ys','f'),('xe','f'),('ye','f')]))
        if (fxmlfile is not None):
            fmap = FeatureMapDF()
            FeatureXMLFile().load(fxmlfile, fmap)
            featdf = fmap.get_df()
            rects = hv.Rectangles(featdf, kdims=["RTstart", "mzstart", "RTend", "mzend"]).opts(color="value", alpha=0.1, tools=['tap'])
        else:
            rects = hv.Rectangles([])

        # for later lookup, index the dataframe
        # TODO the best would be if we could access the data from points, but I just cannot figure out how.
        spectradf = spectradf.set_index(["RT","mz"])

        maxrt = spectradf.index.get_level_values(0).max()
        minrt = spectradf.index.get_level_values(0).min()
        maxmz = spectradf.index.get_level_values(1).max()
        minmz = spectradf.index.get_level_values(1).min()

        def new_bounds_hook(plot, elem):
            x_range = plot.state.x_range
            y_range = plot.state.y_range
            x_range.bounds = minrt, maxrt
            y_range.bounds = minmz, maxmz

        # Unfortunately datashade cannot transfer interactiveness (e.g. hover) or colorbars
        # see https://anaconda.org/jbednar/datashade_vs_rasterize/notebook
        # shade = hd.datashade(points,cmap=process_cmap("blues", provider="bokeh"), alpha=250, min_alpha=10).opts(
        #    plot=dict(
        #        width=1000,
        #        height=1000))#, color_key=colors)
        raster = hd.rasterize(points, cmap=process_cmap("blues", provider="bokeh"), aggregator=datashader.sum('inty'),
                              cnorm='log', alpha=10, min_alpha=0
        ).opts(
            active_tools=['box_zoom'],
            tools=['hover'],
            hooks=[new_bounds_hook]
        ).opts(  # weird.. I have no idea why one has to do this. But with one opts you will get an error
            plot=dict(
                width=800,
                height=800,
                xlabel="Retention time (s)",
                ylabel="mass/charge (Da)"
            )
        )

        t2_stop = perf_counter()
        print("Time for creating plot objects:",
              t2_stop - df_stop)

        stream = Selection1D(source=rects)
        def rect_selection(index):
            if len(index) > 0:
                return hv.Rectangles(featdf.iloc[index[0]].to_frame().T, kdims=["RTstart", "mzstart", "RTend", "mzend"])
            else:
                return hv.Rectangles([])

        def rect_annotation(index):
            if len(index) > 0:
                return hv.Table(featdf.iloc[index[0]].to_frame().T).opts(title="Selected feature", height=70, width=800)
            else:
                return hv.Table([]).opts(title="Selected feature", height=70, width=800)

        # in case we ever want to check for intersections ourselves. Holoviews seems to be a bit slow.
        # actually an interval/KD/quad tree like structure would be nice for checking intersections.
        def rect_tap(x,y):
            print(featdf[featdf.apply(lambda row : x > row[0] and x < row[2] and y > row[1] and y < row[3])])
            return hv.Points([])

        dyn = hv.DynamicMap(rect_selection, kdims=[], streams=[stream]).opts(color="red", alpha=0.1)
        dyntable = hv.DynamicMap(rect_annotation, kdims=[], streams=[stream])

        # Dynspread dynamically increases the size of the points when zooming in.
        finalplot = hv.Layout(dyntable + (hd.dynspread(raster, threshold=0.7, how="add", shape="square") * rects * dyn))
            #.opts( # this is how you can change specific styles afterwards
            #    opts.Rectangles(color="value", alpha=0.1, tools=['tap'])
            #)
        finalplot.cols(1)

        tableplot = renderer.get_plot(finalplot[0], doc)
        hvplot = renderer.get_plot(finalplot[1], doc)

        # updates the JS function to be triggered by invisText with the new filtered data.
        # then triggers a value change in invisText2. This will trigger a js side change for invisText,
        # eventually rendering the new data in 3D.
        # TODO with the new filtering mechanism, we can stop earlier if we see that the points are too many.
        #   We also do not need much of the binary search in the JS code anymore (and do not need to pass the RT range to JS)
        #   We could even call pyOpenMS functions on callback (e.g. extract range or noise filtering)
        def onbuttonclick():
            invisText.js_on_change("value",
                                   CustomJS(
                                       code=jsupdateinfo,
                                       args=dict(
                                            xr=hvplot.state.x_range,
                                            yr=hvplot.state.y_range,
                                            data=ColumnDataSource(
                                                  spectradf.query(
                                                      str(hvplot.state.x_range.start) +
                                                      " <= RT <= " +
                                                      str(hvplot.state.x_range.end) +
                                                      " and " +
                                                      str(hvplot.state.y_range.start) +
                                                      " <= mz <= " +
                                                      str(hvplot.state.y_range.end)
                                                  ).reset_index()
                                              ))))

            # This was without index
            #invisText.js_on_change("value", CustomJS(code=jsupdateinfo, args=dict(xr=hvplot.state.x_range,
            #                                                                      yr=hvplot.state.y_range,
            #                                                                      data=ColumnDataSource(
            #                                                                          spectradf[spectradf['RT'].between(
            #                                                                              hvplot.state.x_range.start,
            #                                                                              hvplot.state.x_range.end)]))))
            invisText2.value = "baz" + str(random.randint(0, 10000))

        # The update 3D button
        bt = Button(label='Update 3D View')
        bt.on_click(onbuttonclick)
        dynamic_col.children = []  # reset, then add
        #dynamic_col.children.append(finalplot)
        dynamic_col.children.append(tableplot.state)
        dynamic_col.children.append(hvplot.state)
        dynamic_col.children.append(bt)

    @gen.coroutine
    def load_data(event):
        print("Starting load!")
        #doc.add_timeout_callback(partial(init_2D_plot_and_update_btn, spectradf), 0)  # we do this instead
        doc.add_timeout_callback(init_2D_plot_and_update_btn, 0)  # we do this instead

    doc.add_root(layout)
    doc.on_event("document_ready", load_data)
    return doc

def main():
    modify_doc(curdoc())

main()
