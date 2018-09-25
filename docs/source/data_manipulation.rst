Simple Data Manipulation
=========================

Here we will look at a few simple data manipulation techniques on spectral
data, such as filtering. First we will download some sample data:

.. code-block:: python

    import urllib
    from pyopenms import *
    urllib.urlretrieve ("http://proteowizard.sourceforge.net/example_data/tiny.pwiz.1.1.mzML",
                        "test.mzML")


Filtering Spectra 
*******************


We will filter the "test.mzML" file by only retaining spectra that match a
certain identifier:

.. code-block:: python
  :linenos:

  from pyopenms import *
  inp = MSExperiment()
  MzMLFile().load("test.mzML", inp)

  e = MSExperiment()
  for s in inp:
    if s.getNativeID().startswith("scan="):
      e.addSpectrum(s)

  MzMLFile().store("test_filtered.mzML", e)

Filtering by MS level 
~~~~~~~~~~~~~~~~~~~~~

Similarly, we can filter the ``test.mzML`` file by MS level:

.. code-block:: python
  :linenos:

  from pyopenms import *
  inp = MSExperiment()
  MzMLFile().load("test.mzML", inp)

  e = MSExperiment()
  for s in inp:
    if s.getMSLevel() > 1:
      e.addSpectrum(s)

  MzMLFile().store("test_filtered.mzML", e)


Note that we can easily replace line 7 with more complicated criteria, such as
filtering by MS level and scan identifier at the same time:

.. code-block:: python
  :linenos:
  :lineno-start: 7

  if s.getMSLevel() > 1 and s.getNativeID().startswith("scan="):

Filtering by scan number
~~~~~~~~~~~~~~~~~~~~~~~~

Or we could use an external list of scan numbers to filter by scan numbers:

.. code-block:: python
  :linenos:

  from pyopenms import *
  inp = MSExperiment()
  MzMLFile().load("test.mzML", inp)
  scan_nrs = [0, 2, 5, 7]

  e = MSExperiment()
  for k, s in enumerate(inp):
    if k in scan_nrs and s.getMSLevel() == 1:
      e.addSpectrum(s)

  MzMLFile().store("test_filtered.mzML", e)

It would also be easy to read the scan numbers from a file where each scan
number is on its own line, thus replacing line 4 with:

.. code-block:: python
  :linenos:
  :lineno-start: 4

  scan_nrs = [int(k) for k in open("scan_nrs.txt")]


Filtering Spectra and Peaks
***************************

We can now move on to more advanced filtering, suppose you are interested in
only a part of all fragment ion spectra.
m/z. We can easily filter our data accordingly:

.. code-block:: python
  :linenos:

  from pyopenms import *
  inp = MSExperiment()
  MzMLFile().load("test.mzML", inp)

  mz_start = 6.0
  mz_end = 12.0
  e = MSExperiment()
  for s in inp:
    if s.getMSLevel() > 1:
      filtered_mz = []
      filtered_int = []
      for mz, i in zip(*s.get_peaks()):
        if mz > mz_start and mz < mz_end:
          filtered_mz.append(mz)
          filtered_int.append(i)
      s.set_peaks((filtered_mz, filtered_int))
      e.addSpectrum(s)

  MzMLFile().store("test_filtered.mzML", e)

Note that in a real-world application, we would set the ``mz_start`` and
``mz_end`` parameter to an actual area of interest, for example the area
between 125 and 132 which contains quantitative ions for a TMT experiment.

Similarly we could change line 13 to only report peaks above a certain
intensity or to only report the top N peaks in a spectrum.


Memory management 
*****************

On order to save memory, we can avoid loading the whole file into memory and
use the OnDiscMSExperiment for reading data. 

.. code-block:: python
  :linenos:

  from pyopenms import *
  od_exp = OnDiscMSExperiment()
  od_exp.openFile("test.mzML")

  e = MSExperiment()
  for k in range(od_exp.getNrSpectra()): 
    s = od_exp.getSpectrum(k)
    if s.getNativeID().startswith("scan="):
      e.addSpectrum(s)

  MzMLFile().store("test_filtered.mzML", e)

Note that using the approach the output data ``e`` is still completely in
memory and may end up using a substantial amount of memory. We can avoid that
by using

.. code-block:: python
  :linenos:

  from pyopenms import *
  od_exp = OnDiscMSExperiment()
  od_exp.openFile("test.mzML")

  consumer = PlainMSDataWritingConsumer("test_filtered.mzML")

  e = MSExperiment()
  for k in range(od_exp.getNrSpectra()): 
    s = od_exp.getSpectrum(k)
    if s.getNativeID().startswith("scan="):
      consumer.consumeSpectrum(s)

  del consumer

Make sure you do not forget ``del consumer`` since otherwise the final part of
the mzML may not get written to disk (and the consumer is still waiting for new
data).



