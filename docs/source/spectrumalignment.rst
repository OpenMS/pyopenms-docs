Spectrum alignment
==================

OpenMS provides several ways to find matching peaks between two spectra.
The most basic one SpectrumAlignment returns a list of matching peak indices between a query and target spectrum.
In this example, we take an observed (measured) spectrum and align a theoretical spectrum to it.

First we load a (chemically modified) peptide:

.. code-block:: python
    :linenos:

    from urllib.request import urlretrieve
    from pyopenms import *
    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-docs/master"
    urlretrieve (gh + "/src/data/YIC(Carbamidomethyl)DNQDTISSK.mzML", "observed.mzML")

    exp = MSExperiment()
    # Load mzML file and obtain spectrum for peptide YIC(Carbamidomethyl)DNQDTISSK
    MzMLFile().load("observed.mzML", exp)
    
    # Get first spectrum
    spectra = exp.getSpectra()
    observed_spectrum = spectra[0]


Now we generate the theoretical spectrum of that peptide:

.. code-block:: python
    :linenos:

    tsg = TheoreticalSpectrumGenerator()
    theo_spectrum = MSSpectrum()
    p = tsg.getParameters()
    p.setValue("add_y_ions", "true")
    p.setValue("add_b_ions", "true")
    p.setValue("add_metainfo", "true")
    tsg.setParameters(p)
    peptide = AASequence.fromString("YIC(Carbamidomethyl)DNQDTISSK")
    tsg.getSpectrum(theo_spectrum, peptide, 1, 2)        

Now we can plot the observed and theoretical spectrum as a mirror plot:

.. code-block:: python
    :linenos:

    from matplotlib import pyplot as plt

    mirror_plot_spectrum(observed_spectrum, theo_spectrum, spectrum_bottom_kws={"annotate_ions": False})
    plt.show()

which produces

.. image:: img/spec_alignment_1.png

Now we want to find matching peaks between observed and theoretical spectrum.

.. code-block:: python
    :linenos:

      alignment = []
      spa = SpectrumAlignment()
      p = spa.getParameters()
      # use 0.5 Da tolerance (Note: for high-resolution data we could also use ppm by setting the is_relative_tolerance value to true)
      p.setValue("tolerance", 0.5)
      p.setValue("is_relative_tolerance", "false")
      spa.setParameters(p)
      # align both spectra
      spa.getSpectrumAlignment(alignment, theo_spectrum, observed_spectrum)

The alignment contains a list of matched peak indices. We can simply inspect matching peaks with:

.. code-block:: python
    :linenos:

    # Print matching ions and mz from theoretical spectrum
    print("Number of matched peaks: " + str(len(alignment)))
    t = []
    for theo_idx, obs_idx in alignment:
        ion_name = theo_spectrum.getStringDataArrays()[0][theo_idx].decode()
        ion_charge = theo_spectrum.getIntegerDataArrays()[0][theo_idx]
        t.append([
            ion_name, str(ion_charge),
            str(theo_spectrum[theo_idx].getMZ()), str(observed_spectrum[obs_idx].getMZ())
        ])
    print(tabulate(t, headers=["ion", "charge", "theo. m/z", "observed m/z"]))

.. code-block:: output

    Number of matched peaks: 16
    ion      charge    theo. m/z    observed m/z
    -----  --------  -----------  --------------
    y2+           1      234.145         234.123
    y5++          2      268.158         268.105
    b2+           1      277.155         277.246
    y3+           1      321.177         321.297
    y4+           1      434.261         434.288
    b3+           1      437.185         437.291
    y5+           1      535.309         535.189
    b4+           1      552.212         552.338
    b9++          2      562.24          562.421
    y10++         2      584.251         584.412
    y11++         2      640.793         640.954

The mirror plot can also be used to visualize the aligned spectrum:

.. code-block:: python
    :linenos:

      from matplotlib import pyplot as plt

      mirror_plot_spectrum(observed_spectrum, theo_spectrum, alignment=alignment, spectrum_bottom_kws={"annotate_ions": False})
      plt.show()

which produces

.. image:: img/spec_alignment_2.png
