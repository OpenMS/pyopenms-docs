.. pyOpenMS documentation master file, created by
   sphinx-quickstart on Fri Jun  1 15:50:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Summary
=======

pyOpenMS is an open-source Python library for mass spectrometry, specifically for the analysis of proteomics and metabolomics data in Python. pyOpenMS implements a set of Python bindings to the OpenMS library for computational mass spectrometry and is available for Windows, Linux and OSX.

PyOpenMS provides functionality that is commonly used in computational mass
spectrometry.  The pyOpenMS package contains Python bindings for a large part of the OpenMS
library (http://www.open-ms.de) for mass spectrometry based proteomics. It thus
provides facile access to a feature-rich, open-source algorithm
library for mass-spectrometry based proteomics analysis. 

pyOpenMS facilitates the execution of common tasks in protoemics (and other mass spectrometric fields) such as 

- file handling (mzXML, mzML, TraML, mzTab, fasta, pepxml, protxml, mzIdentML among others)
- chemistry (mass calculation, peptide fragmentation, isotopic abundances)
- signal processing (smoothing, filtering, de-isotoping, retention time correction and peak-picking) 
- identification analysis (including peptide search, PTM analysis, Cross-linked analytes, FDR control, RNA oligonucleotide search and small molecule search tools)
- quantitative analysis (including label-free, metabolomics, SILAC, iTRAQ and SWATH/DIA analysis tools)
- chromatogram analysis (chromatographic peak picking, smoothing, elution profiles and peak scoring for SRM/MRM/PRM/SWATH/DIA data)
- interaction with common tools in proteomics and metabolomics 

  - search engines such as Comet, Crux, Mascot, MSGFPlus, MSFragger, Myrimatch, OMSSA, Sequest, SpectraST, XTandem
  - post-processing tools such as percolator, MSStats, Fido
  - metabolomics tools such as SIRIUS, CSI:FingerId

Please see the appendix of the official `pyOpenMS Manual
<http://proteomics.ethz.ch/pyOpenMS_Manual.pdf>`_ for a complete documentation
of the pyOpenMS API and all wrapped classes.

Note: the current documentation relates to the 2.6.0 release of pyOpenMS.


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
   :caption: Mass Spectrometry Concepts

   datastructures
   chemistry
   aasequences
   nasequences
   theoreticalspectrumgenerator
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
   smoothing
   mass_decomposition
   deisotoping
   feature_detection
   peptide_search
   chromatographic_analysis
   metabolomics_targeted_feature_extraction

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics
   
   mzMLFileFormat


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

.. image:: ./img/launch_binder.jpg
   :target: https://mybinder.org/v2/gh/OpenMS/pyopenms-extra/master+ipynb?urlpath=lab/tree/docs/source/index.ipynb
   :alt: Launch Binder