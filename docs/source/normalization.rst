Spectrum normalization 
======================

Another very basic spectrum processing step is normalization by base peak intensity (the maximum intensity of a spectrum).

Let's first load the raw data.

.. code-block:: python

  from urllib.request import urlretrieve
  from pyopenms import *
  import matplotlib.pyplot as plt

  gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-docs/master"
  urlretrieve (gh + "/src/data/peakpicker_tutorial_1_baseline_filtered.mzML", "tutorial.mzML")
  exp = MSExperiment()
  MzMLFile().load("tutorial.mzML", exp)
  plt.bar(exp.getSpectrum(0).get_peaks()[0], exp.getSpectrum(0).get_peaks()[1], snap=False)


Now we apply the normalization.

.. code-block:: python

  normalizer = Normalizer()
  param = normalizer.getParameters()
  param.setValue("method", "to_one")
  normalizer.setParameters(param)

  normalizer.filterPeakMap(exp)
  plt.bar(exp.getSpectrum(0).get_peaks()[0], exp.getSpectrum(0).get_peaks()[1], snap=False)  


Another way of normalizing is by TIC (total ion count) of the spectrum, which scales intensities
so they add up to 1.0 in each spectrum.
Try it out for yourself by setting: param.setValue("method", "to_TIC").
