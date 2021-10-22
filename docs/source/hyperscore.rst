Scoring spectra with HyperScore
===============================

In the event that we want to generate scores from directly comparing theoretical and experimental spectra,
we can use HyperScore.

Background
**********

HyperScore computes the (ln transformed) X!Tandem HyperScore of a theoretical spectrum,
calculated from a peptide/oligonucleotide sequence, with an experimental spectrum,
loaded from an mzML file.

    1. the dot product of peak intensities between matching peaks in experimental and theoretical spectrum is calculated
    2. the HyperScore is calculated from the dot product by multiplying by factorials of matching b- and y-ions

.. code-block:: python

    from urllib.request import urlretrieve
    from pyopenms import *
    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"
    urlretrieve (gh +"/src/data/SimpleSearchEngine_1.mzML", "searchfile.mzML")

Generate a theoretical spectrum
*******************************

We now use the TheoreticalSpectrumGenerator generate a theoretical spectrum for the sequence we are interested in,
``RPGADSDIGGFGGLFDLAQAGFR``, and compare the peaks to a spectra from our file.


.. code-block:: python

    tsg = TheoreticalSpectrumGenerator()
    thspec = MSSpectrum()
    p = Param()
    p.setValue("add_metainfo", "true")
    tsg.setParameters(p)
    peptide = AASequence.fromString("RPGADSDIGGFGGLFDLAQAGFR")
    tsg.getSpectrum(thspec, peptide, 1, 1)
    # Iterate over annotated ions and their masses
    for ion, peak in zip(thspec.getStringDataArrays()[0], thspec):
        print(ion, peak.getMZ())

    e = MSExperiment()
    MzMLFile().load("searchfile.mzML", e)
    spectrum_of_interest = e[2]
    print ("Spectrum native id", spectrum_of_interest.getNativeID() )
    mz,i = spectrum_of_interest.get_peaks()
    peaks = [(mz,i) for mz,i in zip(mz,i) if i > 1500 and mz > 300]
    for peak in peaks:
      print (peak[0], "mz", peak[1], "int")

Comparing the theoretical spectrum and the experimental spectrum for
``RPGADSDIGGFGGLFDLAQAGFR`` we can easily see that the most abundant ions in the
spectrum are y8 (877.452 m/z), b10 (926.432), y9 (1024.522 m/z) and b13
(1187.544 m/z).

Getting a score
***************

We now run HyperScore to compute the similarity of the theoretical spectrum
and the experimental spectrum and print the result 


.. code-block:: python

    hscore = HyperScore()
    fragment_mass_tolerance = 5.0
    is_tol_in_ppm = True
    result = hscore.compute(fragment_mass_tolerance, is_tol_in_ppm, spectrum_of_interest, thspec)
    result

If we didn't know ahead of time which spectrum was a match we can loop through all the spectra from our file,
 calculate scores for all of them, and print the result:

.. code-block:: python

    for f in e:
        score = hscore.compute(fragment_mass_tolerance, is_tol_in_ppm, f, thspec)
        print(f.getNativeID() + ":" + str(score) )

