.. pyOpenMS documentation master file, created by
   sphinx-quickstart on Fri Jun  1 15:50:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Summary
=======

pyOpenMS are the Python bindings to the OpenMS library which are available for
Windows, Linux and OSX.

PyOpenMS provides functionality that is commonly used in computational mass
spectrometry.  The pyOpenMS package contains Python bindings for a large part of the OpenMS
library (http://www.open-ms.de) for mass spectrometry based proteomics. It thus
provides facile access to a feature-rich, open-source algorithm
library for mass-spectrometry based proteomics analysis. 

These Python bindings
allow raw access to the data-structures and algorithms implemented in OpenMS,
specifically those for file access (mzXML, mzML, TraML, mzIdentML among
others), basic signal processing (smoothing, filtering, de-isotoping and
peak-picking) and complex data analysis (including label-free, SILAC, iTRAQ and
SWATH analysis tools).

Please see the appendix of the official `pyOpenMS Manual
<http://proteomics.ethz.ch/pyOpenMS_Manual.pdf>`_ for a complete documentation
of the pyOpenMS API and all wrapped classes.

Note: the current documentation relates to the 2.5.0 release of pyOpenMS.


.. toctree::
   :maxdepth: 2
   :caption: Installation

   installation

.. toctree::
   :maxdepth: 2
   :caption: First steps

   getting_started
   file_handling
   mzMLFileFormat
   other_file_handling

.. toctree::
   :maxdepth: 2
   :caption: Mass Spectrometry Concepts

   datastructures
   chemistry
   aasequences
   digestion
   datastructures_id
   datastructures_quant

.. toctree::
   :maxdepth: 2
   :caption: Simple Data Manipulation

   data_manipulation

.. toctree::
   :maxdepth: 2
   :caption: OpenMS Algorithms

   parameter_handling
   algorithms
   deisotoping
   feature_detection
   peptide_search
   chromatographic_analysis

.. toctree::
   :maxdepth: 2
   :caption: R language

   pyopenms_in_r

.. toctree::
   :maxdepth: 2
   :caption: Developers

   build_from_source
   wrap_classes



Indices and tables
==================

* :ref:`genindex`
