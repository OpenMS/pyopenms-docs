MS Data
=======

Spectrum
********

The most important container for raw data and peaks is ``MSSpectrum`` which we
have already worked with in the `Getting Started <getting_started.html>`_
tutorial.  ``MSSpectrum`` is a container for 1-dimensional peak data (a
container of ``Peak1D``). You can access these objects directly, however it is
faster to use the ``get_peaks()`` and ``set_peaks`` functions which use Python
numpy arrays for raw data access. Meta-data is accessible through inheritance
of the ``SpectrumSettings``  objects which handles meta data of a spectrum. 

In the following example program, a MSSpectrum is filled with peaks, sorted
according to mass-to-charge ratio and a selection of peak positions is
displayed.

First we create a spectrum and insert peaks with descending mass-to-charge ratios: 

.. code-block:: python
   :linenos:

    from pyopenms import *
    spectrum = MSSpectrum()
    mz = range(1500, 500, -100)
    i = [0 for mass in mz]
    spectrum.set_peaks([mz, i])

    # Sort the peaks according to ascending mass-to-charge ratio
    spectrum.sortByPosition()

    # Iterate over spectrum of those peaks
    for p in spectrum:
        print(p.getMZ(), p.getIntensity())

    # More efficient peak access
    for mz, i in zip(*spectrum.get_peaks()):
        print(mz, i)

    # Access a peak by index
    print(spectrum[1].getMZ(), spectrum[1].getIntensity())


Note how lines 11-12 use the direct access to the ``Peak1D`` objects (explicit
but slow) while lines 15-16 use the faster access through numpy arrays.

To discover the full set of functionality of ``MSSpectrum``, we use the
``help()`` function. In particular, we find several important sets of meta
information attached to the spectrum including retention time, the ms level
(MS1, MS2, ...), precursor ion, ion mobility drift time and extra data arrays.

.. code-block:: python

  from pyopenms import *
  help(MSSpectrum)

We now set several of these properties in a current MSSpectrum:

.. code-block:: python
    :linenos:

    from pyopenms import *
    spectrum = MSSpectrum()
    spectrum.setDriftTime(25) # 25 ms
    spectrum.setRT(205.2) # 205.2 s
    spectrum.setMSLevel(3) # MS3
    p = Precursor()
    p.setIsolationWindowLowerOffset(1.5)
    p.setIsolationWindowUpperOffset(1.5) 
    p.setMZ(600) # isolation at 600 +/- 1.5 Th
    p.setActivationEnergy(40) # 40 eV
    p.setCharge(4) # 4+ ion
    spectrum.setPrecursors( [p] )

    fda = FloatDataArray()
    fda.setName("Signal to Noise Array")
    fda.push_back(15)
    sda = StringDataArray()
    sda.setName("Peak annotation")
    sda.push_back("y15++")
    spectrum.setFloatDataArrays( [fda] )
    spectrum.setStringDataArrays( [sda] )
    spectrum.set_peaks( ([401.5], [900]) )

    # Store as mzML
    exp = MSExperiment()
    exp.addSpectrum(spectrum)
    spectrum = MSSpectrum()
    spectrum.set_peaks( ([1, 2], [1, 2]) )
    exp.addSpectrum(spectrum)
    MzMLFile().store("testfile.mzML", exp)


You can now open the resulting spectrum in a spectrum viewer. We use the OpenMS
viewer ``TOPPView`` (which you will get when you install OpenMS from the
official website) and look at our MS3 spectrum:

.. image:: img/spectrum1.png

TOPPView displays our MS3 spectrum with its single peak at 401.5 *m/z* and it
also correctly displays its retention time at 205.2 seconds and precursor
isolation target of 600.0 *m/z*.  Notice how TOPPView displays the information
about the S/N for the peak (15) and its annotation as ``y15++`` in the status
bar below when the user clicks on the peak at 401.5 *m/z* as shown in the
screenshot.

Peak Map
*********

In OpenMS, LC-MS/MS injections are stored in so-called peak maps, which a
container of series of ``MSSpectrum`` object. The ``MSExperiment`` object holds
such peak maps as well as meta-data about the injection. 

In the following code, we create an ``MSExperiment`` and populate it with several spectra

.. code-block:: python

    # The following examples creates a MSExperiment containing four MSSpectrum instances.
    exp = MSExperiment()
    for i in range(6):
        spectrum = MSSpectrum()
        spectrum.setRT(i)
        spectrum.setMSLevel(1)
        for mz in range(500, 900, 100):
          peak = Peak1D()
          peak.setMZ(mz + i)
          peak.setIntensity(100 - 25*abs(i-2.5) )
          spectrum.push_back(peak)
        exp.addSpectrum(spectrum)

    # Iterate over spectra
    for s in exp:
        for p in s:
            print (s.getRT(), p.getMZ(), p.getIntensity())

    # Sum intensity of all spectra between RT 2.0 and 3.0
    print(sum([p.getIntensity() for s in exp if s.getRT() >= 2.0 and s.getRT() <= 3.0 for p in s]))

We can again store the resulting spectra as mzML using the ``MSExperiment`` object:

.. code-block:: python

    # Store as mzML
    MzMLFile().store("testfile2.mzML", exp)

Again we can visualize the resulting data using ``TOPPView`` using its 3D
viewer capability, which shows the six scans over retention time:

.. image:: img/spectrum2.png

Chromatogram
************

An addition container for raw data is the ``MSChromatogram`` container, which
is highly analogous to the ``MSSpectrum`` container, but contains an array of
``ChromatogramPeak`` and is derived from ``ChromatogramSettings``:

.. code-block:: python

    from pyopenms import *
    import numpy as np

    def gaussian(x, mu, sig):
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

    chromatogram = MSChromatogram()
    rt = range(1500, 500, -100)
    i = [gaussian(rtime, 1000, 150) for rtime in rt]
    chromatogram.set_peaks([rt, i])

    # Sort the peaks according to ascending retention time
    chromatogram.sortByPosition()

    # Iterate over chromatogram of those peaks
    for p in chromatogram:
        print(p.getRT(), p.getIntensity())

    # Access a peak by index
    print(chromatogram[1].getRT(), chromatogram[1].getIntensity())

We now again add meta information to the chromatogram:

.. code-block:: python

    chromatogram.setNativeID("Trace XIC@405.2")
    p = Precursor()
    p.setIsolationWindowLowerOffset(1.5)
    p.setIsolationWindowUpperOffset(1.5) 
    p.setMZ(405.2) # isolation at 405.2 +/- 1.5 Th
    p.setActivationEnergy(40) # 40 eV
    p.setCharge(2) # 2+ ion
    p.setMetaValue("description", chromatogram.getNativeID())
    p.setMetaValue("peptide_sequence", chromatogram.getNativeID())
    chromatogram.setPrecursor(p)
    p = Product()
    p.setMZ(603.4) # transition from 405.2 -> 603.4
    chromatogram.setProduct(p)

    # Store as mzML
    exp = MSExperiment()
    exp.addChromatogram(chromatogram)
    MzMLFile().store("testfile3.mzML", exp)

Again we can visualize the resulting data using ``TOPPView`` using its chromatographic viewer
capability, which shows the peak over retention time:

.. image:: img/chromatogram1.png

Note how the annotation using precursor and production mass of our XIC
chromatogram as is displayed in the viewer.

