Introduction
============

pyOpenMS is a python library for Liquid Chromatography-Mass Spectrometry (LC-MS) data analysis.

This introduction is aimed at users new to the field of LC-MS data analysis and will cover some basics in terms of data generation.

How to handle the data analysis, available data structures, algorithms and more are covered in the various subsections of this documentation.

Introduction
============

Proteomics and metabolomics are interdisciplinary research fields that study struc-
ture, function, and interaction of proteins and metabolites. They employ large-scale

experimental techniques that allow acquiring data at the level of cellular systems to
whole organisms. One of the main analytical method to identify, characterize or quantify
proteins and metabolites is mass spectrometry (MS) combined with chromatographic
separation.

In mass spectrometry-based proteomics and metabolomics, biological samples are
extracted, prepared, and separated to reduce sample complexity. The separated analytes
are ionized and measured in the mass spectrometer. Mass and abundance of ions are
stored in mass spectra and used to identify and quantify the analytes in the sample
using computational methods. The quantity and identity of analytes can then be used,
for instance, in biomarker discovery, medical diagnostics, or basic research.


Liquid Chromatography
---------------------
LC aims to reduce the complexity of the measured sample by separating analytes 
based on their physicochemical properties. Separating analytes in time ensures that 
a manageable amount of analytes elute at the same time.
In mass spectrometry-based proteomics, (high-pressure) liquid chromatographic
separation techniques (HPLC) are methods of choice to achieve a high degree of
separation. In HPLC, peptides are separated on a column. Solved in a pressurized liquid (mobile phase)
they are pumped through a solid adsorbent material (stationary phase) packet into a
capillary column. Physicochemical properties of each peptide determine how strongly it
interacts with the stationary phase. The most commonly HPLC technique in proteomics
and metabolomics uses reversed-phase chromatography (RPC) columns. RPC employs a hydrophobic
stationary phase like octadecyl (C18), a nonpolar carbon chain bonded to a silica base,
and a polar mobile phase. Polar molecules interact weakly with the stationary phase
and elute earlier, while non-polar molecules are retained. Interaction can be further
modulated by changing the gradient of solvent concentration in the mobile phase
over time. Elution times in LC are inherently prone to variation, for example, due
to fluctuations in the flow rate of the mobile phase or change of column. Retention
time shifts between runs may be compensated using computational chromatographic 
retention time alignment methods. In the LC-MS setup, the column is directly coupled
to the ion source of the mass spectrometer.

.. image:: img/introduction_LC.png


Mass Spectrometry 
-----------------
A mass spectrometer (MS) measures ionized particles in mass-to-charge (m/z) space.  It consists of an ion source, a mass analyzer and an ion detector. The MS can be coupled to an LC System (LC-MS) to reduce the sample complexity before measuring the analyte. We will shortly explain the function based on a qTof instrument. It consists of an electrospray ionization (ESI) ion source and three quadrupoles (Q1-3) mass analyzers coupled to a time-of-flight (TOF) detector.

An MS instrument can measure charged particles, there, the ESI comes into play, which ionizes the analytes. The instrument discussed here has three quadrupole mass analyzers. A quadrupole consists of four parallel metal rods, where an oscillating electric field is applied. The ionized particles are piped to the mass analyzer, which stabilizes the flight path of charged particles with a specific mass-to-charge ratio. Ions with a different mass-to-charge will be expelled, due to their unstable trajectories, unless the frequency is changed to allow these ions through the quadrupole. In the case of the qTOF, the filtered ions are forwarded to a time-of-flight (TOF) detector. It records the time of flight between the extraction pulse and the hit onto the detector. The charge and mass can be calculated from the flight time and the applied acceleration voltage.

A sample is measured over the retention time of the chromatography and the mass-to-charge span on the instrumental. The measurement of one sample is an MS run and produces an MS map.

.. image:: img/introduction_MS.png

In proteomics and metabolomics, the MS1 intensity is often used for the quantification of an analyte. Identification based on the MS1 mass-to-charge and the isotope pattern is highly ambiguous. To improve identification, tandem mass spectrometry (MS/MS) can be applied to assess the analyte substructure. To this end, the precursor ion is isolated and kinetically fragmented using an inert gas (e.g., Argon). Fragments produced by collision-induced fragmentation (CID) are stored in an MS2 (MS/MS) spectrum and provide information that helps to resolve the ambiguities in identification. Alternatively, MS/MS spectra can be used for quantification.
