.. pyOpenMS documentation master file, created by
   sphinx-quickstart on Fri Jun  1 15:50:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Summary
=======

pyOpenMS are the Python bindings to the OpenMS library.

The pyOpenMS package contains Python bindings for a large part of the OpenMS library (http://www.open-ms.de) for mass spectrometry based proteomics. It thus provides providing facile access to a feature-rich, open-source algorithm library for mass-spectrometry based proteomics analysis. These Python bindings allow raw access to the data-structures and algorithms implemented in OpenMS, specifically those for file access (mzXML, mzML, TraML, mzIdentML among others), basic signal processing (smoothing, filtering, de-isotoping and peak-picking) and complex data analysis (including label-free, SILAC, iTRAQ and SWATH analysis tools).

The pyOpenMS package runs - like OpenMS - on Windows, Linux and OSX.


.. toctree::
   :maxdepth: 2
   :caption: Installation

   installation

.. toctree::
   :maxdepth: 2
   :caption: First steps

   getting_started
   file_handling
   other_file_handling

.. toctree::
   :maxdepth: 2
   :caption: Mass Spectrometry Concepts:

   datastructures
   chemistry
   digestion

.. toctree::
   :maxdepth: 2
   :caption: OpenMS Algorithms:

   parameter_handling
   algorithms
   feature_detection

.. toctree::
   :maxdepth: 2
   :caption: Developers

   wrap_classes


Indices and tables
==================

* :ref:`genindex`
