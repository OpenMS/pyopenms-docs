Introduction
============

As indicated in the summary, pyOpenMS is a python library for Liquid Chromatography-Mass Spectrometry (LC-MS) data analsis.

This introduction is aimed at users new to the field of LC-MS data analysis and will cover some basics in terms of data generation.

How to handle the data analysis, available data structures, algorithms and more is covered in the various subsections of this documentation.

Liquid Chromatography
---------------------
The aim of LC is to reduce the complexity of the measured sample. A LC system is comprised of solvent/eluent, pump, injection valve, column and a dectector. The column (stationary phase) has certain physicochemical properties and is used in combination with a solvent/eluent (mobile phase). The method is very versatile due to the various combination of stationary and mobile phases. In most cases reverse-phase chromatography is used in Proteomics (study of peptides and proteins) and Metabolomics (study of small molecues). Here, separation is based on hydrophobicity using a hydrophobic material as a stationary phase (e.g. C18) and a hydrophilic mobile phase (e.g. Acetonitrile). Hydrophobic analytes interact stronger with the column and therefore are retained longer. These interactions are reflected in the retention time of a certain analyte. Nowadays, this setup is enhanced by using pressure in combination with small diameter columns, also called high-performance liquid chromatography (HPCL). The mobile phase is pumped with very high pressure in a small diameter leads to an increase in sensitivity by increasing the singal-to-noise ratio. The resolution of the chromatography is basically dependent on column length, inner diamter, praticle size, stationary phase, flow rate, pressure and temperature, as well as the composition of the mobile phase. In addition different gradients can be used which vary in time and the concentration slope of the solvent/eluent, which can be optimized to fit the experimental needs.

.. image:: img/introduction_LC.png

Mass Spectrometry 
-----------------
A mass spectrometer (MS) measures ionized particles in mass-to-charge (m/z) space.  It consists of an ion source, a mass analyzer and an ion detector. The MS can be coupled to a LC System (LC-MS) to reduce the sample complexity before measuring the analyte. We will shortly explain the function based on a qTof instrument. It consists of an electrospray ionization (ESI) ion source, three quandrupole (Q1-3) mass analyzers coupled to a time-of-flight (TOF) detector. 

A MS instrument is able to measure charged particles, there, the ESI comes into play, which ionizes the analytes. The instrument discussed here has three quadrupole mass analyzers. A quadrupole consits of four parallel metal rods, were an oscillating electric field is applied. The ionized particles are piped to the the mass analyzer, which stabilizes the flight path of charged particles with a specific mass-to-charge ratio. Ions with a different mass-to-charge will be expelled, due to their instable trajectories, unless the frequency is changed to allow these ions through the quadrupole. In case of the qTOF the filtered ions are forwarded to a time-of-flight (TOF) detector. It records the time of flight between the extraction pulse and the hit onto the detector. The charge and mass can be calculated from the flight time and the applied acceleration voltage.

A sample is measured over the retention time of the chromatography and the mass-to-charge span on the instrumental. The measurment of one sample is a MS run and produces a MS map. 

.. image:: img/introduction_MS.png

% TODO: add explanation MS1 and MS2 and their usage (quantification/identification)