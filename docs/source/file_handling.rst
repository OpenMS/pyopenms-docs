Reading Raw MS data
===================

mzML files in memory
********************

As discussed in the last section, the most straight forward way to load mass
spectrometric data is using the ``MzMLFile`` class:

.. code-block:: python

    from pyopenms import *
    from urllib.request import urlretrieve
    # from urllib import urlretrieve  # use this code for Python 2.x
    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"
    urlretrieve (gh + "/src/data/tiny.mzML", "test.mzML")
    exp = MSExperiment()
    MzMLFile().load("test.mzML", exp)

which will load the content of the "test.mzML" file into the ``exp``
variable of type ``MSExperiment``. We can access the raw data and spectra through:

.. code-block:: python

    spectrum_data = exp.getSpectrum(0).get_peaks()
    chromatogram_data = exp.getChromatogram(0).get_peaks()

Which will allow us to compute on spectra and chromatogram data. We can
manipulate the spectra in the file for example as follows:

.. code-block:: python

    spec = []
    for s in exp.getSpectra():
        if s.getMSLevel() != 1:
            spec.append(s)

    exp.setSpectra(spec)

Which will only keep MS2 spectra in the ``MSExperiment``. We can then store the modified data structure on disk:

.. code-block:: python

    MzMLFile().store("filtered.mzML", exp)

Putting this together, a small filtering program would look like this:

.. code-block:: python

    """
    Script to read mzML data and filter out all MS1 spectra
    """
    exp = MSExperiment()
    MzMLFile().load("test.mzML", exp)

    spec = []
    for s in exp.getSpectra():
        if s.getMSLevel() != 1:
            spec.append(s)

    exp.setSpectra(spec)

    MzMLFile().store("filtered.mzML", exp)

indexed mzML files
******************

Since pyOpenMS 2.4, you can open, read and inspect files that use the
indexedMzML standard. This allows users to read MS data without loading all
data into memory:

.. code-block:: python

    od_exp = OnDiscMSExperiment()
    od_exp.openFile("test.mzML")
    meta_data = od_exp.getMetaData()
    meta_data.getNrChromatograms()
    od_exp.getNrChromatograms()

    # data is not present in meta_data experiment
    sum(meta_data.getChromatogram(0).get_peaks()[1]) # no data!
    sum(od_exp.getChromatogram(0).get_peaks()[1]) # data is here!

    # meta data is present and identical in both data structures:
    meta_data.getChromatogram(0).getNativeID() # fast
    od_exp.getChromatogram(0).getNativeID() # slow

Note that the ``OnDiscMSExperiment`` allows users to access meta data through
the ``getMetaData`` function, which allows easy selection and filtering on meta
data attributes (such as MS level, precursor *m/z*, retention time etc.) in
order to select spectra and chromatograms for analysis.  Only once selection on
the meta data has been performed, will actual data be loaded into memory using
the ``getChromatogram`` and ``getSpectrum`` functions.

This approach is memory efficient in cases where computation should only occur
on part of the data or the whole data may not fit into memory.

mzML files as streams
*********************

In some instances it is impossible or inconvenient to load all data from an
mzML file directly into memory. OpenMS offers streaming-based access to mass
spectrometric data which uses a callback object that receives spectra and
chromatograms as they are read from the disk. A simple implementation could look like

.. code-block:: python

    class MSCallback():
        def setExperimentalSettings(self, s):
            pass

        def setExpectedSize(self, a, b):
            pass

        def consumeChromatogram(self, c):
            print ("Read a chromatogram")

        def consumeSpectrum(self, s):
            print ("Read a spectrum")


which can the be used as follows:

.. code-block:: output

    filename = b"test.mzML"
    consumer = MSCallback()
    MzMLFile().transform(filename, consumer)
    Read a spectrum
    Read a spectrum
    Read a spectrum
    Read a spectrum
    Read a chromatogram
    Read a chromatogram

which provides an intuition on how the callback object works: whenever a
spectrum or chromatogram is read from disk, the function ``consumeSpectrum`` or
``consumeChromatogram`` is called and a specific action is performed. We can
use this to implement a simple filtering function for mass spectra:

.. code-block:: output

    class FilteringConsumer():
        """
        Consumer that forwards all calls the internal consumer (after
        filtering)
        """

        def __init__(self, consumer, filter_string):
            self._internal_consumer = consumer
            self.filter_string = filter_string

        def setExperimentalSettings(self, s):
            self._internal_consumer.setExperimentalSettings(s)

        def setExpectedSize(self, a, b):
            self._internal_consumer.setExpectedSize(a, b)

        def consumeChromatogram(self, c):
            if c.getNativeID().find(self.filter_string) != -1:
                self._internal_consumer.consumeChromatogram(c)

        def consumeSpectrum(self, s):
            if s.getNativeID().find(self.filter_string) != -1:
                self._internal_consumer.consumeSpectrum(s)

    ###################################
    filter_string = "DECOY"
    inputfile = "in.mzML"
    outputfile = "out.mzML"
    ###################################

    consumer = PlainMSDataWritingConsumer(outputfile)
    consumer = FilteringConsumer(consumer, filter_string)

    MzMLFile().transform(inputfile, consumer)


where the spectra and chromatograms are filtered by their native ids. It is
similarly trivial to implement filtering by other attributes. Note how the data
are written to disk using the ``PlainMSDataWritingConsumer`` which is one of
multiple available consumer classes -- this specific class will simply take the
spectrum ``s`` or chromatogram ``c`` and write it to disk (the location of the
output file is given by the ``outfile`` variable).

Note that this approach is memory efficient in cases where computation should
only occur on part of the data or the whole data may not fit into memory.


cached mzML files
*********************

In addition, since pyOpenMS 2.4 the user can efficiently cache mzML files to disk which
provides very fast access with minimal overhead in memory. Basically the data
directly mapped into memory when requested. You can use this feature as follows:

.. code-block:: python

    # First load data and cache to disk
    exp = MSExperiment()
    MzMLFile().load("test.mzML", exp)
    CachedmzML.store("myCache.mzML", exp)

    # Now load data
    cfile = CachedmzML()
    CachedmzML.load("myCache.mzML", cfile)

    meta_data = cfile.getMetaData()
    cfile.getNrChromatograms()
    cfile.getNrSpectra()

    # data is not present in meta_data experiment
    sum(meta_data.getChromatogram(0).get_peaks()[1]) # no data!
    sum(cfile.getChromatogram(0).get_peaks()[1]) # data is here!

    # meta data is present and identical in both data structures:
    meta_data.getChromatogram(0).getNativeID() # fast
    cfile.getChromatogram(0).getNativeID() # slow

Note that the ``CachedmzML`` allows users to access meta data through
the ``getMetaData`` function, which allows easy selection and filtering on meta
data attributes (such as MS level, precursor *m/z*, retention time etc.) in
order to select spectra and chromatograms for analysis.  Only once selection on
the meta data has been performed, will actual data be loaded into memory using
the ``getChromatogram`` and ``getSpectrum`` functions.

Note that in the example above all data is loaded into memory first and then
cached to disk. This is not very efficient and we can use the
``MSDataCachedConsumer`` to directly cache to disk (without loading any data
into memory):

.. code-block:: python

    # First cache to disk
    # Note: writing meta data to myCache2.mzML is required
    cacher = MSDataCachedConsumer("myCache2.mzML.cached")
    exp = MSExperiment()
    MzMLFile().transform(b"test.mzML", cacher, exp)
    CachedMzMLHandler().writeMetadata(exp, "myCache2.mzML")
    del cacher

    # Now load data
    cfile = CachedmzML()
    CachedmzML.load("myCache2.mzML", cfile)

    meta_data = cfile.getMetaData()
    # data is not present in meta_data experiment
    sum(meta_data.getChromatogram(0).get_peaks()[1]) # no data!
    sum(cfile.getChromatogram(0).get_peaks()[1]) # data is here!

This approach is now memory efficient in cases where computation should only occur
on part of the data or the whole data may not fit into memory.
