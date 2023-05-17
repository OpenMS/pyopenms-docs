Scoring Spectra with HyperScore
===============================

In the chapter on spectrum alignment we showed how to determine matching peaks between theoretical and experimental spectra.
For many use cases we might actually not be interested in obtaining the list of matched peaks but would like to have
a simple, single score that indicates how "well" the two spectra matched.
The :py:class:`~.HyperScore` is a method to assign a score to :term:`peptide-spectrum matches<peptide-spectrum match>`.


Background
**********


:py:class:`~.HyperScore` computes the (ln transformed) ``HyperScore`` of theoretical spectrum,
calculated from a peptide/oligonucleotide sequence, with an experimental spectrum,
loaded from an :term:`mzML` file.

    1. the dot product of peak intensities between matching peaks in experimental and theoretical spectrum is calculated
    2. the :py:class:`~.HyperScore` is calculated from the dot product by multiplying by factorials of matching b- and y-ions

.. code-block:: python

    from urllib.request import urlretrieve
    import pyopenms as oms

    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-docs/master"
    urlretrieve(gh + "/src/data/SimpleSearchEngine_1.mzML", "searchfile.mzML")

Generate a Theoretical Spectrum
*******************************


We now use the :py:class:`~.TheoreticalSpectrumGenerator` to generate a theoretical spectrum for the sequence we are interested in,
``RPGADSDIGGFGGLFDLAQAGFR``, and compare the peaks to a spectra from our file.


.. code-block:: python

    tsg = oms.TheoreticalSpectrumGenerator()
    thspec = oms.MSSpectrum()
    p = oms.Param()
    p.setValue("add_metainfo", "true")
    tsg.setParameters(p)
    peptide = oms.AASequence.fromString("RPGADSDIGGFGGLFDLAQAGFR")
    tsg.getSpectrum(thspec, peptide, 1, 1)
    # Iterate over annotated ions and their masses
    for ion, peak in zip(thspec.getStringDataArrays()[0], thspec):
        print(ion, peak.getMZ())

    e = oms.MSExperiment()
    oms.MzMLFile().load("searchfile.mzML", e)
    spectrum_of_interest = e[2]
    print("Spectrum native id", spectrum_of_interest.getNativeID())
    mz, i = spectrum_of_interest.get_peaks()
    peaks = [(mz, i) for mz, i in zip(mz, i) if i > 1500 and mz > 300]
    for peak in peaks:
        print(peak[0], "mz", peak[1], "int")

Comparing the spectrum and the experimental spectrum for
``RPGADSDIGGFGGLFDLAQAGFR`` we can easily see that the most abundant ions in the
spectrum are :chem:`y8` (:math:`877.452` m/z), :chem:`b10` (:math:`926.432`), :chem:`y9`
(:math:`1024.522` m/z) and :chem:`b13` (:math:`1187.544` m/z).

Getting a Score
***************

We now run :py:class:`~.HyperScore` to compute the similarity of the theoretical spectrum
and the experimental spectrum and print the result

.. code-block:: python

    hscore = oms.HyperScore()
    fragment_mass_tolerance = 5.0
    is_tol_in_ppm = True
    result = hscore.compute(
        fragment_mass_tolerance, is_tol_in_ppm, spectrum_of_interest, thspec
    )
    result

If we didn't know ahead of time which spectrum was a match we can loop through all the spectra from our file,
 calculate scores for all of them, and print the result:

.. code-block:: python

    for f in e:
        score = hscore.compute(fragment_mass_tolerance, is_tol_in_ppm, f, thspec)
        print(f.getNativeID() + ":" + str(score))


