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

    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"
    urlretrieve (gh + "/src/data/tiny.mzML", "test.mzML")

    exp = MSExperiment()
    gf = GaussFilter()
    exp = MSExperiment()
    MzMLFile().load('test.mzML', exp)    
    gf.filterExperiment(exp)
    # MzMLFile().store("test.filtered.mzML", exp)



Spectra Merge Algorithm
*************************

The pyOpenMS spectra merge algorithms allows the merge of several spectra by either increasing S/N ratio (for MS1 and above) or merging scans which stem from similar precursors (for MS2 and above). In any case, the number of scans will be reduced. In addition, pyOpenMS provides the method to average spectra. 

Different spectra merge algorithms are available in pyOpenMS:
- mergeSpectraBlockWise
- mergeSpectraPrecursors
- average (over neighbouring spectra for MS1 or above)

In order to have a better picture of the algorithms, each one will be introduced by an example below. We will use another example file compared to above and start with an example of merging spectra blockwise:

.. code-block:: python

    # retrieve data 
    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"
    urlretrieve(gh + "/src/data/small.mzML", "test.mzML")

    # load MS data and store as MSExperiment object
    exp = MSExperiment()
    MzMLFile().load('test.mzML', exp)

    spectra = exp.getSpectra()
    print(f"There are {len(spectra)} spectra before merging.\n")

    # merges blocks of MS or MS2 spectra
    sm = SpectraMerger()
    sm.mergeSpectraBlockWise(exp)

    spectraMB = exp.getSpectra()
    print(f"There are {len(spectraMB)} spectra after merge")


.. code-block:: output 
  
    There are 236 spectra before merging.

    There are 90 spectra after merging. 


As predicated, the number of scans decreased after merged MS spectra. The modified data structure can be stored on disk:

.. code-block:: python

    MzMLFile().store("mergedBlockWise.mzML", exp)


The merging of spectra with similar precursors progresses likewise:

.. code-block:: python 

    # load MS data and store as MSExperiment object
    exp = MSExperiment()
    MzMLFile().load('test.mzML', exp)

    spectra = exp.getSpectra()
    print(f"The number of spectra before merge is {len(spectra)}")

    # merge spectra with similar precursors 
    sm = SpectraMerger()
    sm.mergeSpectraPrecursors(exp)

    spectraMP = exp.getSpectra()
    print(f"The number of spectra after merge is {len(spectraMP)}")

    # store modified data 
    # MzMLFile().store("mergedBlockWise.mzML", exp)


``SpectraMerger`` presents a method to average experimental data over neighbouring spectra. The averaging types to be used by the method are either "gaussian" or "tophat":

.. code-block:: python 

    # load MS data and store as MSExperiment object
    exp = MSExperiment()
    MzMLFile().load('test.mzML', exp)

    # average spectra with gaussian
    sm = SpectraMerger()
    sm.average(exp, "gaussian")  

    # store modified data 
    # MzMLFile().store("mergedBlockWise.mzML", exp)

The OpenMS documentation lists the `parameters <https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Documentation/release/latest/html/classOpenMS_1_1SpectraMerger.html#a714276597bcee3d240e385e32717a6b3>`_ in``SpectraMerger``. More information about parameter handling can be found in the :index: `section before`. 
