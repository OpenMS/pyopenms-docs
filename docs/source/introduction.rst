Introduction
============

pyOpenMS is a python library for Liquid Chromatography-Mass Spectrometry (LC-MS) data analysis.

This introduction is aimed at users new to the field of LC-MS data analysis and will cover some basics in terms of data generation.

How to handle the data analysis, available data structures, algorithms and more are covered in the various subsections of this documentation.

Liquid Chromatography
---------------------
LC aims to reduce the complexity of the measured sample by separating analytes based on their physicochemical properties. Separating analytes in time ensures that a manageable amount of analytes elute at the same time. A LC system is comprised of solvent/eluent, pump, injection valve, column and a detector. The column (stationary phase) has certain physicochemical properties and is used in combination with a solvent/eluent (mobile phase). The method is very versatile due to the various combination of stationary and mobile phases. In most cases, reverse-phase chromatography is used in Proteomics (study of peptides and proteins) and Metabolomics (study of small molecules). Here, separation is based on hydrophobicity using a hydrophobic material as a stationary phase (e.g. C18) and a hydrophilic mobile phase (e.g. Acetonitrile). Hydrophobic analytes interact stronger with the column and are therefore retained longer. These interactions are reflected in the retention time of a certain analyte. Nowadays, this setup is enhanced by using pressure in combination with small diameter columns, also called high-performance liquid chromatography (HPLC). The mobile phase is pumped with very high pressure in small diameter beads to an increase in sensitivity by increasing the signal-to-noise ratio. The resolution of the chromatography is dependent on column length, inner diameter, particle size, stationary phase, flow rate, pressure and temperature, as well as the composition of the mobile phase. In addition, different gradients can be used which vary in time and the concentration slope of the solvent/eluent, which can be optimized to fit the experimental needs.

.. image:: img/introduction_LC.png


Mass Spectrometry 
-----------------
A mass spectrometer (MS) measures ionized particles in mass-to-charge (m/z) space.  It consists of an ion source, a mass analyzer and an ion detector. The MS can be coupled to an LC System (LC-MS) to reduce the sample complexity before measuring the analyte. We will shortly explain the function based on a qTof instrument. It consists of an electrospray ionization (ESI) ion source and three quadrupoles (Q1-3) mass analyzers coupled to a time-of-flight (TOF) detector.

An MS instrument can measure charged particles, there, the ESI comes into play, which ionizes the analytes. The instrument discussed here has three quadrupole mass analyzers. A quadrupole consists of four parallel metal rods, where an oscillating electric field is applied. The ionized particles are piped to the mass analyzer, which stabilizes the flight path of charged particles with a specific mass-to-charge ratio. Ions with a different mass-to-charge will be expelled, due to their unstable trajectories, unless the frequency is changed to allow these ions through the quadrupole. In the case of the qTOF, the filtered ions are forwarded to a time-of-flight (TOF) detector. It records the time of flight between the extraction pulse and the hit onto the detector. The charge and mass can be calculated from the flight time and the applied acceleration voltage.

A sample is measured over the retention time of the chromatography and the mass-to-charge span on the instrumental. The measurement of one sample is an MS run and produces an MS map.

.. image:: img/introduction_MS.png

In proteomics and metabolomics, the MS1 intensity is often used for the quantification of an analyte. Identification based on the MS1 mass-to-charge and the isotope pattern is highly ambiguous. To improve identification, tandem mass spectrometry (MS/MS) can be applied to assess the analyte substructure. To this end, the precursor ion is isolated and kinetically fragmented using an inert gas (e.g., Argon). Fragments produced by collision-induced fragmentation (CID) are stored in an MS2 (MS/MS) spectrum and provide information that helps to resolve the ambiguities in identification. Alternatively, MS/MS spectra can be used for quantification.
