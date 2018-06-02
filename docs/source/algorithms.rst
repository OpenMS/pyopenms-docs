Algorithms 
==========

Most signal processing algorithms follow a similar pattern in OpenMS.

.. code-block:: python

  filter = FilterObject()
  exp = MSExperiment()
  # populate exp
  filter.filterExperiment(exp)

Since they work on a single MSExperiment object, little input is needed to
execute a filter directly on the data. Examples of filters that follow this
pattern are ``GaussFilter``, ``SavitzkyGolayFilter`` as well as the spectral filters
``BernNorm``, ``MarkerMower``, ``NLargest``, ``Normalizer``, ``ParentPeakMower``, ``Scaler``,
``SpectraMerger``, ``SqrtMower``, ``ThresholdMower``, ``WindowMower``.


using the same example file as before in 

.. code-block:: python

    from pyopenms import *
    exp = MSExperiment()
    gf = GaussFilter()
    MzMLFile().load("test.mzML", exp)
    gf.filterExperiment(exp)
    MzMLFile().store("test.filtered.mzML", exp)


