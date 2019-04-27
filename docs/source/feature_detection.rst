Feature Detection
=================

One very common task in Mass Spectrometric research is the detection of 2D features in a series of MS1 scans (MS1 feature detection). OpenMS has multiple tools that can achieve these tasks, these tools are called `FeatureFinder`. Currently the following FeatureFinders are available in OpenMS:

  - FeatureFinderMultiplex
  - FeatureFinderMRM
  - FeatureFinderCentroided      
  - FeatureFinderIdentification  
  - FeatureFinderIsotopeWavelet  
  - FeatureFinderMetabo   
  - FeatureFinderSuperHirn

All of the algorithms above are for proteomics data with the exception of
FeatureFinderMetabo which works on metabolomics data. One of the most commonly
used FeatureFinders is the FeatureFinderCentroided which works on (high
resolution) centroided data. We can use the following code to find ``Features``
in MS data:

.. code-block:: python

  from pyopenms import *

  # Prepare data loading (save memory by only
  # loading MS1 spectra into memory)
  options = PeakFileOptions()
  options.setMSLevels([1])
  fh = MzMLFile()
  fh.setOptions(options)

  # Load data
  input_map = MSExperiment()
  fh.load("test.mzML", input_map)
  input_map.updateRanges()

  ff = FeatureFinder()
  ff.setLogType(LogType.CMD)

  # Run the feature finder
  name = "centroided"
  features = FeatureMap() 
  seeds = FeatureMap()
  params = FeatureFinder().getParameters(name)
  ff.run(name, input_map, features, params, seeds)

  features.setUniqueIds()
  fh = FeatureXMLFile()
  fh.store("output.featureXML", features)
  print("Found", features.size(), "features")

You can get a sample file for analysis directly from `here <https://raw.githubusercontent.com/OpenMS/OpenMS/develop/src/tests/topp/FeatureFinderCentroided_1_input.mzML>`_.

With a few lines of Python, we are able to run powerful algorithms available in
OpenMS. The resulting data is held in memory (a ``FeatureMap`` object) and can be
inspected directly using the ``help(features)`` comment. It reveals that the
object supports iteration (through the ``__iter__`` function) as well as direct
access (through the ``__getitem__`` function).  We can also inspect the entry
for ``FeatureMap`` in the `pyOpenMS manual
<http://proteomics.ethz.ch/pyOpenMS_Manual.pdf>`_ and learn about the same
functions. This means we write code that uses direct access and iteration in
Python as follows:

.. code-block:: python

  f0 = features[0]
  for f in features:
      print (f.getRT(), f.getMZ())


Each entry in the ``FeatureMap`` is a so-called ``Feature`` and allows direct
access to the `m/z` and `RT` value from Python. Again, we can lear this by
inspecting ``help(f)`` or by consulting the Manual.

Note: the output file that we have written (``output.featureXML``) is an
OpenMS-internal XML format for storing features. You can learn more about file
formats in the `Reading MS data formats <other_file_handling.html>`_ section.

