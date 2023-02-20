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

    MS2
    MS/MS
    tandem mass spectrometry
        Tandem MS is a technique where two or more mass analyzers are coupled together using an additional reaction step to increase their abilities to analyse chemical samples.

    TOF
    time-of-flight
        Time-of-flight (TOF) is the time taken by an object, particle of wave (be it acoustic, electromagnetic, e.t.c) to travel a distance through a medium.

    quadrupole
        A mass filter allowing one mass channel at a time to reach the detector as the mass range is scanned.

    orbitrap
        In MS, an ion trap mass analyzer consisting of an outer barrel-like electrode and a coaxial inner
        spindle-like electrode that traps ions in an orbital motion around the spindle.
        A high resolution MS analyzer.

    MS1
        Mass spectra of a sample from a single fragmentation step.

    MS3
        Multi-stage MS

    CID
    collision-induced dissociation
        Collision-induced dissociation is a MS technique to induce fragmentation of selected ions in the gas phase.

    TOPP
        The OpenMS Pipeline is a set of chainable tools to create pipelines for mass spectrometry analysis.

    MSGFPlusAdapter
        Adapter for the MS-GF+ protein identification (database search) engine. More information is available in the
        `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_MSGFPlusAdapter.html>`__.

    LuciphorAdapter
        Adapter for the LuciPHOr2: a site localisation tool of generic post-translational modifications from tandem mass
        spectrometry data. More information is available in the `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_LuciphorAdapter.html>`__.

    TOPP tools
        OpenMS provides a number of functions that process MS data called :term:`TOPP` tools. All :term:`TOPP`
        tools are described in the `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_documentation.html>`__.

    UTILS
        Besides :term:`TOPP tools`, OpenMS offers a range of other tools. They are not included in :term:`TOPP` as they
        are not part of typical analysis pipelines. More information is present in `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/UTILS_documentation.html>`__.

    TOPPView
        TOPPView is a viewer for MS and HPLC-MS data.

    nightly snapshot
        Untested installers and containers are known as the nightly snapshot.

    MascotAdapter
        Used to identifies peptides in MS2 spectra. Read more about MascotAdapter in the `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_MascotAdapter.html>`__.

    high performance liquid chromatography
    HPLC
        In high performance liquid chromatography (HPLC), analytes are dissolved in a pressurized solvent (mobile phase)
        and pumped through a solid adsorbent material (stationary phase) packed into a
        capillary column. Physicochemical properties of the analyte determine how strongly it
        interacts with the stationary phase.

    mzML
    mzml
        The mzML format is an open, XML-based format for mass spectrometer output files, developed with the full participation
        of vendors and researchers in order to create a single open format that would be supported by all software.

    mzData
    mzdata
        mzData was the first attempt by the Proteomics Standards Initiative (PSI) from the Human Proteome Organization (HUPO)
        to create a standardized format for MS data. This format is now deprecated, and replaced by mzML.

    mzXML
    mzxml
        mzXML is an open data format for storage and exchange of mass spectroscopy data, developed at the SPC/Institute for
        Systems Biology.

    ProteoWizard
        ProteoWizard is a set of open-source, cross-platform tools and libraries for proteomics data analyses.
        It provides a framework for unified MS data file access and performs standard chemistry and LCMS dataset computations.

    PepNovo
        PepNovo is a de :term:`de novo peptide sequencing` algorithm for :term:`MS2` spectra.

    de novo peptide sequencing
        A peptide’s amino acid sequence is inferred directly from the precursor peptide mass and tandem
        mass spectrum (:term:`MS2` or :term:`MS3`) fragment ions, without comparison to a reference proteome.

    TOPPAS
        An assistant for GUI-driven :term:`TOPP` workflow design. It is recommended to use OpenMS through the KNIME plugins.

    KNIME
        An advanced workflow editor which OpenMS provides a plugin for.

    SILAC
    stable isotope labeling with amino acids in cell culture
        Stands for Stable isotope labeling using amino acids in cell culture.

    iTRAQ
        Stands for isobaric tags for relative and absolute quantitation.

    TMT
        Tandem Mass Tag (TMT) is a MS based system designed to identify and quantify proteins in different samples.

    SRM
        Selected reaction monitoring is a MS technique for small molecule analysis.

    SWATH
        Stands for sequential acquisition of all theoretical fragment ion spectra.

    OpenMS API
        An interface that allows developers to use OpenMS core library classes and methods.

    feature maps
    feature map
        A feature map is a collection of features identified in a mass spectrum from a single experiment.
        One feature map can contain many features. OpenMS represents a feature map using the class `FeatureMap <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1FeatureMap.html>`_.

    consensus features
    consensus feature
        Features from replicate experiments with similar retention times and m/z values are linked and considered a consensus feature.
        A consensus feature contains information on the common retention time and m/z values as well as intensities for each sample. OpenMS represents a consensus feature using the class `ConsensusFeature <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1ConsensusFeature.html>`_.

    consensus maps
    consensus map
        A consensus map is a collection of :term:`consensus features` identified from mass spectra across replicate experiments.
        One consensus map can contain many consensus features. OpenMS represents a consensus map using the class `ConsensusMap <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1ConsensusMap.html>`_.
