Centroiding 
===========

MS instruments typically allow storing :term:`spectra` in profile mode (several data points per :term:`m/z` :term:`peak`)
or in the more condensed centroid mode (one data point per :term:`m/z` :term:`peak`). The process of converting
a profile :term:`mass spectrum` into a centroided one is called :term:`peak` centroiding or :term:`peak` picking.

Note: The term :term:`peak` picking is ambiguous as it is also used for :term:`feature` detection (i.e. 3D :term:`peak` finding).

First, we load some profile data:

.. code-block:: python

    from urllib.request import urlretrieve
    from pyopenms import *
    import matplotlib.pyplot as plt

    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-docs/master"
    urlretrieve(gh + "/src/data/PeakPickerHiRes_input.mzML", "tutorial.mzML")

    profile_spectra = MSExperiment()
    MzMLFile().load("tutorial.mzML", profile_spectra)

Let's zoom in on an isotopic pattern in profile mode and plot it.

.. code-block:: python

    plt.xlim(771.8, 774)  # zoom into isotopic pattern
    plt.plot(
        profile_spectra[0].get_peaks()[0], profile_spectra[0].get_peaks()[1]
    )  # plot the first spectrum

.. image:: img/profile_data.png

Because of the limited resolution of :term:`MS` instruments :term:`m/z` measurements are not of unlimited precision.
Consequently, :term:`peak`  shapes spreads in the :term:`m/z` dimension and resemble a gaussian distribution.
Using the :py:class:`~.PeakPickerHiRes` algorithm, we can convert data from profile to centroided mode. Usually, not much information is lost
by storing only centroided data. Thus, many algorithms and tools assume that centroided data is provided.

.. code-block:: python

    centroided_spectra = MSExperiment()

    # input, output, chec_spectrum_type (if set, checks spectrum type and throws an exception if a centroided spectrum is passed)
    PeakPickerHiRes().pickExperiment(
        profile_spectra, centroided_spectra, True
    )  # pick all spectra

    plt.xlim(771.8, 774)  # zoom into isotopic pattern
    plt.stem(
        centroided_spectra[0].get_peaks()[0], centroided_spectra[0].get_peaks()[1]
    )  # plot as vertical lines
.. image:: img/centroided_data.png

After centroiding, a single :term:`m/z` value for every isotopic :term:`peak` is retained. By plotting the centroided data as stem plot
we discover that (in addition to the isotopic :term:`peaks`) some low intensity :term:`peaks` (intensity at approx. 4k) were present in the profile data.

