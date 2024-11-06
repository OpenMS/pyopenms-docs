OpenMS Glossary
===============

A glossary of common terms used throughout OpenMS documentation.

.. glossary::
    :sorted:

    peptide-spectrum match
    PSM
        A method used in proteomics to identify proteins from a complex mixture. Involves comparing the
        mass spectra of peptide fragments generated from a protein sample with a database of predicted
        spectra, in order to identify the protein that produced the observed peptides.

    LC-MS
    LCMS
        :term:`Liquid chromatography<liquid chromatography>`-coupled mass spectrometry.

    LC-MS/MS
    liquid chromatography coupled :term:`tandem mass spectrometry`
        See :term:`LC-MS` and :term:`MS2`.

    liquid chromatography
    LC
        An analytical technique used to separate molecules of interest.

    FASTA
        A text-based format for representing nucleotide or amino acid sequences.

    C18
    octadecyl
        Octadecyl (C18) is an alkyl radical C(18)H(37) derived from an octadecane by removal of one hydrogen atom.

    ESI
    electrospray ionization
        Electrospray ionization (ESI) is a technique used in MS to produce ions.

    TOF
    time-of-flight
        Time-of-flight (TOF) is the time taken by an object, particle or wave (be it acoustic, electromagnetic, e.t.c) to travel a distance through a medium.
        TOF analyzers can obtain good, but not ultra-high resolution, such as an :term:`orbitrap`.

    quadrupole
        A mass filter allowing one mass channel at a time to reach the detector as the mass range is scanned. A low resolution MS analyzer.

    orbitrap
        In MS, an ion trap mass analyzer consisting of an outer barrel-like electrode and a coaxial inner
        spindle-like electrode that traps ions in an orbital motion around the spindle.
        An ultra-high resolution MS analyzer, capable of resolving fine-isotope structure.

    Mass Spectrometry
    MS
        An analytical technique to measure the mass over charge (m/z) ratio of ions along with their abundance. This gives rise to a mass spectrum (with m/z on the x-axis and abundance on the y-axis).
        
    mass spectrum
        A visual or numerical representation of a measurement from an MS instrument. A spectrum contains (usually many) pairs of mass-over-charge(m/z)+intensity values.

    MS1
        Mass spectra of a sample where only precursor ions (i.e. no fragment ions) can be observed.
        Usually MS1 spectra are recorded to select targets for MS2 fragmentation.

    MS2
    MS/MS
    tandem mass spectrometry
        Tandem MS is a technique where two or more mass analyzers are coupled together using an additional, usually destructive, reaction step to generate fragment ions which increases their abilities to analyse chemical samples.

    MS3
        Multi-stage MS

    CID
    collision-induced dissociation
        Collision-induced dissociation is an MS technique to induce fragmentation of selected ions in the gas phase, which are subjected to a subsequent measurement (see :term:`MS2`).

    TOPP
       'TOPP - The OpenMS PiPeline' is a pipeline for the analysis of HPLC-MS data. It consists of several small applications that can be chained to create analysis pipelines tailored for a specific problem. See :term:`TOPP tools`.

    MSGFPlusAdapter
        Adapter for the MS-GF+ protein identification (database search) engine. More information is available in the
        `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_MSGFPlusAdapter.html>`__.

    LuciphorAdapter
        Adapter for the LuciPHOr2: a site localisation tool of generic post-translational modifications from tandem mass
        spectrometry data. More information is available in the `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_LuciphorAdapter.html>`__.

    TOPP tools
        OpenMS provides a number of applications (executable files) that are chainable in a pipeline/script and each process MS data.
        These tools are subdivided into different categories, such as 'File Handling' or 'Peptide Identification'.
        All :term:`TOPP` tools are described in the `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_documentation.html>`__.

    UTILS
        [deprecated since OpenMS 3.1] Besides :term:`TOPP tools`, OpenMS offers a range of other tools. They are not included in :term:`TOPP` as they
        are not part of typical analysis pipelines. Since OpenMS 3.1 all UTILS are :term:`TOPP tools` under the 'Utilities' category.

    TOPPView
        TOPPView is a viewer for MS and HPLC-MS data and shipped with every OpenMS release.

    nightly snapshot
        Untested installers and containers which are created regularly between official releases and reflect the current development state.

    MascotAdapter
        Used to identify peptides in :term:`MS2` spectra. Read more about MascotAdapter in the `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_MascotAdapter.html>`__.

    high performance liquid chromatography
    HPLC
        In high performance liquid chromatography (HPLC), analytes are dissolved in a pressurized solvent (mobile phase)
        and pumped through a solid adsorbent material (stationary phase) packed into a
        capillary column. Physicochemical properties of the analyte determine how strongly it
        interacts with the stationary phase.

    mzML
    mzml
        The mzML format is an open, XML-based format for mass spectrometer output files, developed by the Proteomics Standard Initiative (PSI)
        with the full participation of vendors and researchers in order to create a single open format that would be supported by all software.

    mzData
    mzdata
        mzData was the first attempt by the Proteomics Standards Initiative (PSI) from the Human Proteome Organization (HUPO)
        to create a standardized format for MS data. This format is now deprecated, and replaced by mzML.

    mzXML
    mzxml
        mzXML is an open data format for storage and exchange of mass spectroscopy data, developed at the SPC/Institute for
        Systems Biology. This format is now deprecated, and replaced by mzML.

    ProteoWizard
        ProteoWizard is a set of open-source, cross-platform tools and libraries for proteomics data analyses.
        It provides a framework for unified MS data file access and performs standard chemistry and LCMS dataset computations.

    PepNovo
        PepNovo is a de :term:`de novo peptide sequencing` algorithm for :term:`MS2` spectra.

    de novo peptide sequencing
        A peptide’s amino acid sequence is inferred directly from the precursor peptide mass and tandem
        mass spectrum (:term:`MS2` or :term:`MS3`) fragment ions, without comparison to a reference proteome.

    TOPPAS
        An assistant for GUI-driven :term:`TOPP` workflow design, build into OpenMS. See `TOPPAS tutorial <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPPAS_tutorial.html>` for details.

    KNIME
        An advanced workflow editor which OpenMS provides a plugin for.

    SILAC
    stable isotope labeling with amino acids in cell culture
        Stands for Stable isotope labeling using amino acids in cell culture.

    iTRAQ
        Isobaric tags for relative and absolute quantitation (iTRAQ) is a MS based multiplexing technique designed to identify and quantify proteins from different samples in one single measurement.

    TMT
        Tandem Mass Tag (TMT) is a MS based multiplexing technique designed to identify and quantify proteins from different samples in one single measurement.

    SRM
        Selected reaction monitoring (SRM) is a MS technique for targeted small molecule analysis.

    SWATH
        Sequential acquisition of all theoretical fragment ion spectra (SWATH) uses parially overlapping MS2 scans with wide isolation windows to capture all fragment ions in a data independent analysis (DIA).

    OpenMS API
        A C++ interface that allows developers to use OpenMS core library classes and methods.

    feature
    features
        A feature, in the OpenMS terminology, subsumes all m/z signals originating from a single compound at a certain charge state. This includes the isotope pattern and usually spans multiple spectra in retention time (the elution profile).
        
    feature maps
    feature map
        A feature map is a collection of :term:`feature`\ s identified from a single experiment.
        One feature map usually contains many features. OpenMS represents a feature map using the class `FeatureMap <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1FeatureMap.html>`_.

    consensus features
    consensus feature
        Features from replicate experiments with similar retention times and m/z values are linked and considered a consensus feature.
        A consensus feature contains information on the common retention time and m/z values as well as intensities for each sample. OpenMS represents a consensus feature using the class `ConsensusFeature <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1ConsensusFeature.html>`_.

    consensus maps
    consensus map
        A consensus map is a collection of :term:`consensus features` identified from mass spectra across replicate experiments, usually by combining multiple :term:`feature maps`.
        One consensus map usually contains many consensus features. OpenMS represents a consensus map using the class `ConsensusMap <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1ConsensusMap.html>`_.
