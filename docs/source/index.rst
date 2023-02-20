.. pyOpenMS documentation master file, created by
   sphinx-quickstart on Fri Jun  1 15:50:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Index
=======

:term:`pyOpenMS` is an open-source Python library for :term:`mass spectrometry`, specifically for the analysis of
:term:`proteomics` and :term:`metabolomics` data in Python. :term:`pyOpenMS` implements a set of Python bindings to
the OpenMS library for computational :term:`mass spectrometry` and is available for Windows, Linux and OSX.

PyOpenMS provides functionality that is commonly used in computational :term:`mass
spectrometry`. The :term:`pyOpenMS` package contains Python bindings for a large part of the `OpenMS <openms.de>`_
library for :term:`mass spectrometry` based :term:`proteomics`. It thus provides access to a feature-rich, open-source algorithm
library for mass-spectrometry based :term:`proteomics` analysis.

:term:`pyOpenMS` facilitates the execution of common tasks in :term:`proteomics` (and other fields of :term:`mass spectrometry`) such as

- File handling (:term:`mzXML`, :term:`mzML`, TraML, mzTab, :term:`FASTA`, pepxml, protxml, mzIdentML among others)
- Chemistry (mass calculation, peptide fragmentation, isotopic abundances)
- Signal processing (smoothing, filtering, de-isotoping, retention time correction and peak-picking)
- Identification analysis (including peptide search, PTM analysis, cross-linked analytes, FDR control, RNA oligonucleotide search and small molecule search tools)
- Quantitative analysis (including label-free, metabolomics, :term:`SILAC`, :term:`iTRAQ` and :term:`SWATH`/DIA analysis tools)
- :term:`Chromatogram<chromatogram>` analysis (chromatographic peak picking, smoothing, elution profiles and peak scoring for :term:`SRM`/MRM/PRM/:term:`SWATH`/DIA data)
- Interaction with common tools in :term:`proteomics` and metabolomics

  - Search engines such as Comet, Crux, Mascot, MSGFPlus, MSFragger, Myrimatch, OMSSA, Sequest, SpectraST, XTandem
  - Post-processing tools such as percolator, MSStats, Fido
  - Metabolomics tools such as SIRIUS, CSI:FingerId

.. toctree::
   :maxdepth: 2
   :caption: Introduction

   background

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   installation
   first_steps
   introduction

.. toctree::
   :maxdepth: 2
   :caption: Mass Spectrometry Concepts

   ms_data
   chemistry
   peptides_proteins
   oligonucleotides_rna
   fragment_spectrum_generation
   spectrum_alignment
   digestion
   identification_data
   quantitative_data

.. toctree::
   :maxdepth: 2
   :caption: OpenMS Algorithms

   parameter_handling
   algorithms
   smoothing
   centroiding
   spectrum_normalization
   charge_isotope_deconvolution
   feature_detection
   map_alignment
   feature_linking
   peptide_search
   chromatographic_analysis
   quality_control
   mass_decomposition
   export_files_GNPS

.. toctree::
   :maxdepth: 2
   :caption: Example Workflows

   identification_accurate_mass
   untargeted_metabolomics_preprocessing

.. toctree::
   :maxdepth: 2
   :caption: How to contribute

   contribute

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics

   reading_raw_ms_data
   other_ms_data_formats
   mzml_files
   scoring_spectra_hyperscore
   export_pandas_dataframe
   query_msexperiment_massql
   memory_management
   pyopenms_in_r
   build_from_source
   wrapping_workflows_new_classes
   interactive_plots
   interfacing_ml_libraries
   
.. toctree::
   :maxdepth: 2
   :caption: Full API documentation

   apidoc   

.. toctree::
   :maxdepth: 2
   :caption: Support

   support
   faq
   glossary


Indices and Tables
==================

* :ref:`genindex`
