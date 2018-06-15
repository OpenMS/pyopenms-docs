Datastructures
=============

Spectrum
********

The most important container for raw data and peaks is ``MSSpectrum``.
``MSSpectrum`` is a container for 1-dimensional peak data (a container of
``Peak1D``). It is derived from ``SpectrumSettings``, a container for the meta
data of a spectrum. 

In the following example program, a MSSpectrum is
filled with peaks, sorted according to mass-to-charge ratio and a selection of
peak positions is displayed.

First we create a spectrum and insert peaks with descending mass-to-charge ratios: 

.. code-block:: python

    from pyopenms import *
    spectrum = MSSpectrum()
    peak = Peak1D()
    for mz in range(1500, 500, -100):
        peak.setMZ(mz)
        spectrum.push_back(peak)

    # Sort the peaks according to ascending mass-to-charge ratio
    spectrum.sortByPosition()

    # Iterate over spectrum of those peaks
    for p in spectrum:
        print(p.getMZ(), p.getIntensity())

    # Access a peak by index
    print(spectrum[1].getMZ(), spectrum[1].getIntensity())

Peak Map
*********

In OpenMS, LC-MS/MS injections are stored in so-called peak maps, which a
container of series of ``MSSpectrum`` object. The ``MSExperiment`` object holds
such peak maps as well as meta-data about the injection. 

In the following code, we create an ``MSExperiment`` and populate it with several spectra

.. code-block:: python

    # The following examples creates a MSExperiment containing four MSSpectrum instances.
    exp = MSExperiment()
    for i in range(4):
        spectrum = MSSpectrum()
        spectrum.setRT(i)
        spectrum.setMSLevel(1)
        for mz in range(500, 900, 100):
          peak = Peak1D()
          peak.setMZ(mz + i)
          peak.setIntensity(100)
          spectrum.push_back(peak)
        exp.addSpectrum(spectrum)

    # Iterate over spectra
    for s in exp:
        for p in s:
            print (s.getRT(), p.getMZ(), p.getIntensity())

    # Sum intensity of all spectra between RT 2.0 and 3.0
    print(sum([p.getIntensity() for s in exp if s.getRT() >= 2.0 and s.getRT() <= 3.0 for p in s]))

Chromatogram
************

An addition container for raw data is the ``MSChromatogram`` container, which
is highly analogous to the ``MSSpectrum`` container, but contains an array of
``ChromatogramPeak`` and is derived from ``ChromatogramSettings``:

.. code-block:: python

    from pyopenms import *
    chromatogram = MSChromatogram()
    peak = ChromatogramPeak()
    for rt in range(1500, 500, -100):
        peak.setRT(rt)
        chromatogram.push_back(peak)

    # Sort the peaks according to ascending retention time
    chromatogram.sortByPosition()

    # Iterate over chromatogram of those peaks
    for p in chromatogram:
        print(p.getRT(), p.getIntensity())

    # Access a peak by index
    print(chromatogram[1].getRT(), chromatogram[1].getIntensity())


