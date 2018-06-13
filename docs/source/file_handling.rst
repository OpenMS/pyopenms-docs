Reading Raw MS data
===================

mzML files in memory
********************

As discussed in the last section, the most straight forward way to load mass
spectrometric data is using the ``MzMLFile`` class: 

.. code-block:: python

    import urllib
    from pyopenms import *
    urllib.urlretrieve ("http://proteowizard.sourceforge.net/example_data/tiny.pwiz.1.1.mzML", "test.mzML")
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
    from pyopenms import *
    exp = MSExperiment()
    MzMLFile().load("test.mzML", exp)

    spec = []
    for s in exp.getSpectra():
        if s.getMSLevel() != 1:
            spec.append(s)

    exp.setSpectra(spec)

    MzMLFile().store("filtered.mzML", exp)

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
            print "Read a chromatogram"
            
        def consumeSpectrum(self, s):
            print "Read a spectrum"


which can the be used as follows:

.. code-block:: python

    >>> from pyopenms import *
    >>> filename = "test.mzML"
    >>> consumer = MSCallback()
    >>> MzMLFile().transform(filename, consumer)
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

.. code-block:: python

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

    consumer = pyopenms.PlainMSDataWritingConsumer(outputfile)
    consumer = FilteringConsumer(consumer, filter_string)

    pyopenms.MzMLFile().transform(inputfile, consumer)


where the spectra and chromatograms are filtered by their native ids. It is
similarly trivial to implement filtering by other attributes. Note how the data
are written to disk using the ``PlainMSDataWritingConsumer`` which is one of
multiple available consumer classes -- this specific class will simply take the
spectrum ``s`` or chromatogram ``c`` and write it to disk (the location of the
output file is given by the ``outfile`` variable).

This approach is memory efficient in cases where the whole data data may not
fit into memory.

