Feature Detection
=================

One very common task in mass spectrometry is the detection of 2-dimensional
patterns in m/z and time (RT) dimension from a series of MS1 scans. These
patterns are called ``Features`` and they exhibit a chromatographic elution
profile in the time dimension and an isotopic pattern in the m/z dimension (see 
`previous section <deisotoping.html>`_ for the 1-dimensional problem).
OpenMS has multiple tools that can identify these features in 2-dimensional
data, these tools are called `FeatureFinder`.  Currently the following
FeatureFinders are available in pyOpenMS:

  - FeatureFinderMultiplexAlgorithm (e.g., SILAC, Dimethyl labeling, (and label-free), identification free feature detection of peptides)
  - FeatureFinderAlgorithmPicked (Label-free, identification free feature detection of peptides)
  - FeatureFinderIdentificationAlgorithm (Label-free identification-guided feature detection of peptides)
  - FeatureFinderAlgorithmIsotopeWavelet (old instruments)
  - FeatureFindingMetabo (Label-free, identification free feature detection of metabolites)
  - FeatureFinderAlgorithmMetaboIdent (Label-free, identification guided feature detection of metabolites)

All of the algorithms above are for proteomics data with the exception of
FeatureFindingMetabo, FeatureFinderMetaboIdent and FeatureFinderMetaboIdentCompound which work on metabolomics data. Two of the most commonly
used FeatureFinders in OpenMS are the FeatureFinder and FeatureFinderIdentificationAlgorithm which both work on (high
resolution) centroided data. We can use the following code to find ``Features``
in MS data:

.. code-block:: python

  from urllib.request import urlretrieve
  gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"
  urlretrieve (gh + "/src/data/FeatureFinderCentroided_1_input.mzML", "feature_test.mzML")

  from pyopenms import *

  # Prepare data loading (save memory by only
  # loading MS1 spectra into memory)
  options = PeakFileOptions()
  options.setMSLevels([1])
  fh = MzMLFile()
  fh.setOptions(options)

  # Load data
  input_map = MSExperiment()
  fh.load("feature_test.mzML", input_map)
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

With a few lines of Python, we are able to run powerful algorithms available in
OpenMS. The resulting data is held in memory (a ``FeatureMap`` object) and can be
inspected directly using the ``help(features)`` comment. It reveals that the
object supports iteration (through the ``__iter__`` function) as well as direct
access (through the ``__getitem__`` function). This means we write code that uses direct access and iteration in
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
