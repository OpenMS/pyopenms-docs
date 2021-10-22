Spectrum alignment
==================

OpenMS provides several ways to find matching peaks between two spectra.
The most basic one SpectrumAlignment returns a list of matching peak indices between a query and target spectrum.
In this example, we take an observed (measured) spectrum and align a theoretical spectrum to it.

First we load a (chemically modified) peptide:

.. code-block:: python
    from urllib.request import urlretrieve
    from pyopenms import *
    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"
    urlretrieve (gh + "/src/data/YIC(Carbamidomethyl)DNQDTISSK.mzML", "observed.mzML")

    exp = MSExperiment()
    # Load mzML file and obtain spectrum for peptide YIC(Carbamidomethyl)DNQDTISSK
    MzMLFile().load("observed.mzML", exp)
    
    # Get first spectrum
    spectra = exp.getSpectra()
    observed_spectrum = spectra[0]


Now we generate the theoretical spectrum of that peptide:

.. code-block:: python
    tsg = TheoreticalSpectrumGenerator()
    theo_spectrum = MSSpectrum()
    p = tsg.getParameters()
    p.setValue("add_y_ions", "true")
    p.setValue("add_b_ions", "true")
    p.setValue("add_metainfo", "true")
    tsg.setParameters(p)
    peptide = AASequence.fromString("YIC(Carbamidomethyl)DNQDTISSK")
    tsg.getSpectrum(theo_spectrum, peptide, 1, 2)        


Now we want to find matching peaks between observed and theoretical spectrum.

.. code-block:: python
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
  # Print matching ions and mz from theoretical spectrum
  print("Number of matched peaks: " + str(len(alignment)))
  print("ion\ttheo. m/z\tobserved m/z")

  for theo_idx, obs_idx in alignment:
      ion_name = theo_spectrum.getStringDataArrays()[0][theo_idx].decode()
      ion_charge = theo_spectrum.getIntegerDataArrays()[0][theo_idx]
      print(ion_name + "\t" + str(ion_charge) + "\t"
        + str(theo_spectrum[theo_idx].getMZ())
        + "\t" + str(observed_spectrum[obs_idx].getMZ()))
        
              
