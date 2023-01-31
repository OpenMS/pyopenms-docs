Algorithms 
==========

Many signal processing algorithms follow a similar pattern in OpenMS.

.. code-block:: pseudocode

  algorithm = NameOfTheAlgorithmClass()
  exp = MSExperiment()
  # populate exp, for example load from file
  algorithm.filterExperiment(exp)

In many cases, the processing algorithms have a set of parameters that can be
adjusted. These are accessible through ``getParameters()`` and yield a
``Param`` object (see `Parameter handling <parameter_handling.html>`_) which can
be manipulated. After changing parameters, one can use ``setParameters()`` to
propagate the new parameters to the algorithm:

.. code-block:: pseudocode

  algorithm = NameOfTheAlgorithmClass()
  param = algorithm.getParameters()
  param.setValue("algo_parameter", "new_value")
  algorithm.setParameters(param)

  exp = MSExperiment()
  # populate exp, for example load from file
  algorithm.filterExperiment(exp)

Since they work on a single MSExperiment object, little input is needed to
execute a filter directly on the data. Examples of filters that follow this
pattern are ``GaussFilter``, ``SavitzkyGolayFilter`` as well as the spectral filters
``BernNorm``, ``MarkerMower``, ``NLargest``, ``Normalizer``, ``ParentPeakMower``, ``Scaler``,
``SpectraMerger``, ``SqrtMower``, ``ThresholdMower``, ``WindowMower``.

Using the same example file as before, we can execute a GaussFilter on our test data as follows: 

.. code-block:: python

    from pyopenms import *
    from urllib.request import urlretrieve

    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-docs/master"
    urlretrieve(gh + "/src/data/tiny.mzML", "test.mzML")

    exp = MSExperiment()
    gf = GaussFilter()
    exp = MSExperiment()
    MzMLFile().load("test.mzML", exp)
    gf.filterExperiment(exp)
    # MzMLFile().store("test.filtered.mzML", exp)

