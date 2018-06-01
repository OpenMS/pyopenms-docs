mzML files in memory
********************

As discussed in the last section, the most straight forward way to load mass
spectrometric data is using the ``MzMLFile`` class: 

.. code-block:: python

    import urllib
    from pyopenms import *
    urllib.urlretrieve ("http://proteowizard.sourceforge.net/example_data/tiny.pwiz.1.1.mzML", "tiny.pwiz.1.1.mzML")
    exp = MSExperiment()
    MzMLFile().load("tiny.pwiz.1.1.mzML", exp)

which will load the content of the "tiny.pwiz.1.1.mzML" file into the ``exp``
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
    MzMLFile().load("tiny.pwiz.1.1.mzML", exp)

    spec = []
    for s in exp.getSpectra():
        if s.getMSLevel() != 1:
            spec.append(s)

    exp.setSpectra(spec)

    MzMLFile().store("filtered.mzML", exp)


