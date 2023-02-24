Memory Management
==================

On order to save memory, we can avoid loading the whole file into memory and
use the :py:class:`~.OnDiscMSExperiment` for reading data.

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
the :term:`mzML` may not get written to disk (and the consumer is still waiting for new
data).

