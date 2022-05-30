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

Spectra merge algorithms merge several spectra to e.g., improve spectrum quality by increasing S/N ratio.
Merging is usually done block wise (for MS1 and above) or (for MS2 and above) based on similar precursors.
Some methods allow to smooth or average spectra. 

Different spectra merge algorithms are available in pyOpenMS:

- mergeSpectraBlockWise
- mergeSpectraPrecursors
- average (over neighbouring spectra for MS1 or above)

Let's take a look at the different algorithms in the examples below. 

Our first example merges MS1 spectra blockwise:

.. code-block:: python

    # retrieve data 
    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"
    urlretrieve(gh + "/src/data/small.mzML", "test.mzML")

    # load MS data and store as MSExperiment object
    exp = MSExperiment()
    MzMLFile().load('test.mzML', exp)

    spectra = exp.getSpectra()
    spectra_ms1 = [s for s in spectra if s.getMSLevel() == 1]
    print(f'Number of MS1 spectra before merge are {len(spectra_ms1)}')

    # merges blocks of MS1
    merger = SpectraMerger()

    merger.mergeSpectraBlockWise(exp)

    spectraMerged = exp.getSpectra()
    spectra_ms1 = [s for s in spectra if s.getMSLevel() == 1]
    print(f'Number of MS1 spectra after merge are {len(spectra_ms1)}')


.. code-block:: output 
  
    Number of MS1 spectra before merge are 183

    Number of MS1 spectra after merge are 37


Per default, the method ``mergeSpectraBlockWise`` of SpectraMerger merges 5 consectutive MS1 spectra into a block. Before the merge, we had 183 MS1 spectra. Now, we have 37 MS1 spectra left. In any case, the number of scans will be reduced. 

The modified data structure can be stored on disk:

.. code-block:: python

    MzMLFile().store("mergedBlockWise.mzML", exp)


SpectraMerger includes the method ``mergeSpectraPrecursors`` which allows the merging of spectra with similar precursors. Note: the data needs to contain MS2 spectra with annotated precursor information.

.. code-block:: python 

    # load MS data and store as MSExperiment object
    exp = MSExperiment()
    MzMLFile().load('test.mzML', exp)

    spectra = exp.getSpectra()

    # spectra with ms_level = 2
    spectra_ms2 = [s for s in spectra if s.getMSLevel() == 2]
    print(f'Number of MS2 spectra before merge are {len(spectra_ms2)}')

    # merge spectra with similar precursors 
    merger = SpectraMerger()
    merger.mergeSpectraPrecursors(exp)

    spectraMerged = exp.getSpectra()
    spectra_ms2 = [s for s in spectra if s.getMSLevel() == 2]
    print(f'Number of MS2 spectra after merge are {len(spectra_ms2)}')

    # store modified data 
    # MzMLFile().store("mergedSimiPrecursors.mzML", exp)

.. code-block:: output

    Number of MS2 spectra before merge are 53

    Number of MS2 spectra after merge are 53

In this example the number of MS2 spectra before and after the merge do not change. This means that precursors were to dissimilar in RT and m/z. 


SpectraMerger presents a method ``average`` to average experimental data over neighbouring spectra. The block of neighbouring spectra depends on the averaging type: ``gaussian`` or ``tophat``. The gaussian type checks for a weight < cutoff value, whereas tophat averages over a range (by default a window of 5 scans left and right from each current scan). Per default SpectraMerger averages MS1 spectra. 

.. code-block:: python 

    # load MS data and store as MSExperiment object
    exp = MSExperiment()
    MzMLFile().load('test.mzML', exp)

    # number of MS1 spectra before averaging
    spectra_ms1 = [s for s in spectra if s.getMSLevel() == 1]
    print(f'Number of MS1 spectra before averaging are {len(spectra_ms1)}')

    # example MS1 spectrum 
    spectrumIdx = 12
    observed_spectrum = exp.getSpectra()[spectrumIdx]
    obs_mz, obs_int = observed_spectrum.get_peaks()
    print(f'Number of peaks: {len(obs_int)}')
    print(f'Intensity of unchanged spectrum {obs_int}')
    print(f'M/Z of unchanged spectrum {obs_mz} \n')

    # average spectra with gaussian
    merger = SpectraMerger()
    merger.average(exp, "gaussian")

    # number of MS1 spectra after averaging
    spectra_ms1 = [s for s in spectra if s.getMSLevel() == 1]
    print(f'Number of MS1 spectra after averaging are {len(spectra_ms1)}')

    # example MS1 spectrum after averaging
    averaged_spectrum = exp.getSpectra()[spectrumIdx]
    avg_mz, avg_int = averaged_spectrum.get_peaks()
    print(f'Number of peaks: {len(avg_int)}')
    print(f'Intensity of averaged spectrum {avg_int}')
    print(f'M/Z of averaged spectrum {avg_mz}')  

    # store modified data 
    # MzMLFile().store("averagedData.mzML", exp)

.. code-block:: output

    Number of MS1 spectra before averaging are 183
    Number of peaks: 1691
    Intensity of unchanged spectrum [1278.0497 1913.4033 2004.5872 ... 2452.4668 2296.3455 2902.3096]
    M/Z of unchanged spectrum [ 360.04589844  361.04638672  361.2098999  ... 1451.59777832 1470.85119629
     1474.65161133] 

    Number of MS1 spectra after averaging are 183
    Number of peaks: 24575
    Intensity of averaged spectrum [134.91116    38.43053    89.57599   ...   3.5365791 152.8209
      12.315695 ]
    M/Z of averaged spectrum [ 360.04589844  360.12536621  360.1282959  ... 1498.15087891 1498.69824219
     1498.99194336]

If averaging is used, the the number of spectra doesn't change. Instead, m/z's and intensities of the example MS1 spectrum have been changed. The method calculates an average spectrum by averaging MS1 spectra over a selected number of neighbouring spectra. Note: Weights follow a gaussian distribution (add up to 1.0). 

The OpenMS documentation lists the `parameters <https://abibuilder.informatik.uni-tuebingen.de/archive/openms/Documentation/release/latest/html/classOpenMS_1_1SpectraMerger.html#a714276597bcee3d240e385e32717a6b3>`_ in ``SpectraMerger``. More information about parameter handling can be found in the `section before <parameter_handling.html>`_. 
