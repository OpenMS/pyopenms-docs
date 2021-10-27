Centroiding 
===========

MS instruments typically allow storing spectra in profile mode (several data points per m/z peak)
or in the more codensed centroid mode (one data point per m/z peak). The process of converting
a profile spectrum into a centroided one is called peak centroiding peak picking.

Note: The term peak picking is ambigious as it is also used for feature detection.

First, we load some profile data:

.. code-block:: python

    from urllib.request import urlretrieve
    from pyopenms import *
    import matplotlib.pyplot as plt

    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"
    urlretrieve (gh +"/src/data/peakpicker_tutorial_1_baseline_filtered.mzML", "tutorial.mzML")
    profile_spectra = MSExperiment()
    MzMLFile().load("tutorial.mzML", profile_spectra) # centroid all spectra,
    plt.bar(profile_spectra[0].get_peaks()[0], profile_spectra[0].get_peaks()[1], snap=False) # but only plot the first one


Because of the limited resolution of MS instruments, peak shapes resemble a gaussian distribution that spreads in the m/z dimension.
Using the PeakPickerHiRes algorithm, we can convert data from profile to centroided mode. Usually, not much information is lost
and by storing only centroided data. Thus, many algorithms and tools assume that centroided data is provided.

.. code-block:: python
    centroided_spectra = MSExperiment()
    PeakPickerHiRes().pickExperiment(profile_spectra, centroided_spectra)
    plt.bar(centroided_spectra[0].get_peaks()[0], centroided_spectra[0].get_peaks()[1], snap=False) # but only plot the first one

After centroding, a single m/z value for every isotopic peak is retained.
