Introduction
============

pyOpenMS is a python library for Liquid Chromatography-Mass Spectrometry (:term:`LC-MS`) data analysis.

Note: This introduction is aimed at users new to the field of :term:`LC-MS` data analysis and will introduce some basics terms
and concepts. How to handle the data analysis, available data structures, algorithms and more are covered in the
various subsections of this documentation.

Background
============

Proteomics and metabolomics are interdisciplinary research fields that study the
function and interaction of proteins and metabolites. They employ large-scale
experimental techniques that allow acquiring data at the level of cellular systems to
whole organisms. One of the main analytical method to identify, characterize or quantify
proteins and metabolites is mass spectrometry (MS) combined with chromatographic
separation.

In mass spectrometry-based proteomics and metabolomics, biological samples are
extracted, prepared, and separated to reduce sample complexity. The separated analytes
are ionized and measured in the mass spectrometer. Mass and abundance of ions are
stored in mass spectra and used to identify and quantify the analytes in the sample
using computational methods. The quantity and identity of analytes can then be used,
in biomarker discovery, medical diagnostics, or basic research.


:term:`Liquid Chromatography<liquid chromatography>` (:term:`LC`)
-----------------------------------------------------------------
:term:`LC` reduces the complexity of a sample by separating analytes
based on their physicochemical properties. Separating analytes in time ensures that 
a manageable amount of analytes elute at the same time. Ideally, the amount is
such that each peak in the mass spectrum corresponds to one single analyte.
In mass spectrometry-based proteomics, :term:`high performance liquid chromatography`
separation techniques (:term:`HPLC`) achieve a high degree of
separation. In :term:`HPLC`, analytes are dissolved in a pressurized solvent (mobile phase)
and pumped through a solid adsorbent material (stationary phase) packed into a
capillary column. Physicochemical properties of the analyte determine how strongly it
interacts with the stationary phase. The most common :term:`HPLC` technique in proteomics
and metabolomics uses reversed-phase chromatography (RPC). RPC employs a hydrophobic
stationary phase like :term:`octadecyl` (:term:`C18`), a nonpolar carbon chain bonded to a silica base,
and a polar mobile phase (solvent). Polar molecules interact weakly with the stationary phase
and elute earlier, while non-polar molecules are retained. Interaction can be further
modulated by changing the gradient of solvent concentration in the mobile phase
over time. Elution times in :term:`LC` are inherently prone to variation, for example, due
to fluctuations in the flow rate of the mobile phase or change of the column. Retention time shifts between runs may be compensated using computational chromatographic
retention time alignment methods. In the :term:`LC-MS` setup, the column is directly coupled
to the ion source of the mass spectrometer.

.. image:: img/introduction_LC.png


Mass Spectrometry (MS)
---------------------------------------------------------

MS is an analytical technique used to determine the mass of molecules. In order to
achieve accurate and sensitive mass measurements at the atomic scale, mass spectrometer
manipulate charged ions using magnetic and electrostatic fields.

.. image:: img/introduction_MS.png

In a typical mass spectrometer, three principal components can be identified:

* Ion Source: A mass spectrometer only handles ions. Thus, charge needs first be transferred to uncharged analytes. The component responsible for the ionization is the ion source. Different types of ion sources and ionization techniques exist with :term:`electrospray ionization` (:term:`ESI`) being currently the most widely used ionization technique.

* Mass Analyzer: the most most commonly used mass analyzers are :term:`time-of-flight` (:term:`TOF`), :term:`quadrupole` mass, and :term:`orbitrap` analyzers. In :term:`TOF` mass analyzers, the ions are accelerated in an electric field. The flight time of an ion is used to calculate the mass-to-charge ratio (m/z). Varying the electric field allows filtering certain mass-to-charge ratios before they enter the detector. In :term:`quadrupole` mass filters, ions pass through an oscillating electric field created by four parallel rods. For a particular field, only ions in a certain mass-to-charge range will reach the detector. The :term:`orbitrap` traps ions in orbital motion between a barrel-like outer electrode and a spindle-like central electrode allowing for prolonged mass measurement. As a result of the prolonged measurement, a high mass resolution can be achieved at the expense of a smaller throughput.

* Detector: The last component of the mass spectrometer is the detector. It determines the abundance of ions that passed through the mass analyzer. Ion intensities (a value that relates to its abundance) and the mass-to-charge ratio are recorded in a mass spectrum.

A sample is measured over the retention time of the chromatography typically resulting in tens of thousands of mass spectra. The measurement of one sample is called an MS run and the set of mass spectra called an MS or peak map.

.. figure:: img/spectrum_peakmap.png

            Left: mass spectrum with peaks (m/z and intensity values), Right: mass spectra stacked in retention time yield a peak map. The mass spectrum in the peak map at the retention time indicated by the red line in the right panel is plotted as a mass spectrum (intensity over m/z) in the left panel.

Identification of an analyte based on the mass spectrum (mass-to-charge ratio and isotope pattern) can be ambiguous. To improve identification, :term:`tandem mass spectrometry` (:term:`MS2`) can be applied to assess the analyte substructure. With :term:`MS2` spectrometry, an ion is isolated, fragmented using an inert gas by collision-induced fragmentation (CID) and a second mass spectrum is recorded from the ion fragments. In this context, the primary ion is called the precursor ion, the primary spectrum is called an :term:`MS1` spectrum and and the spectrum from the fragments is called an :term:`MS2` spectrum. :term:`MS2` is especially useful for linear polymers like proteins, RNA and DNA and the fragments typically break the polymer into two parts. For example, peptides (short strands of amino acids, part of a protein) typically break between each of the amino acids, leading to a so-called ion ladder where the distance between each peak in the :term:`MS2` spectrum reveals the identity of the amino acid, as most amino acids have different masses.
