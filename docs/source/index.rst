.. pyOpenMS documentation master file, created by
   sphinx-quickstart on Fri Jun  1 15:50:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Summary
=======

pyOpenMS is an open-source Python library for mass spectrometry, specifically for the analysis of proteomics and metabolomics data in Python. pyOpenMS implements a set of Python bindings to the OpenMS library for computational mass spectrometry and is available for Windows, Linux and OSX.

PyOpenMS provides functionality that is commonly used in computational mass
spectrometry.  The pyOpenMS package contains Python bindings for a large part of the OpenMS
library (http://www.openms.de) for mass spectrometry based proteomics. It thus
provides facile access to a feature-rich, open-source algorithm
library for mass-spectrometry based proteomics analysis. 

pyOpenMS facilitates the execution of common tasks in proteomics (and other mass spectrometric fields) such as 

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

.. toctree::
   :maxdepth: 2
   :caption: Introduction

   introduction

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   installation
   first_steps

.. toctree::
   :maxdepth: 2
   :caption: Mass Spectrometry Concepts

   datastructures_peak
   chemistry
   aasequences
   nasequences
   theoreticalspectrumgenerator
   spectrumalignment
   digestion
   datastructures_id
   datastructures_quant

.. toctree::
   :maxdepth: 2
   :caption: OpenMS Algorithms

   parameter_handling
   algorithms
   smoothing
   centroiding
   normalization
   deisotoping
   feature_detection
   map_alignment
   feature_linking
   peptide_search
   chromatographic_analysis
   mzqc_export
   mass_decomposition

.. toctree::
   :maxdepth: 2
   :caption: Example Workflows

   id_by_mz

.. toctree::
   :maxdepth: 2
   :caption: How to contribute

   contribute

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics

   file_handling
   other_file_handling   
   mzMLFileFormat
   pandas_df_conversion
   massql
   memory_management
   pyopenms_in_r
   build_from_source
   wrap_classes
   interactive_plots
   ML_tutorial

.. toctree::
   :maxdepth: 2
   :caption: Support

   support


Indices and tables
==================

* :ref:`genindex`
