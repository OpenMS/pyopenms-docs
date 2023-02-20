OpenMS Glossary
===============

A glossary of common terms used throughout OpenMS documentation.

.. glossary::
    :sorted:

    peptide-spectrum match
    PSM
        A method used in :term:`proteomics` to identify proteins from a complex mixture. Involves comparing the
        :term:`mass spectra<mass spectrum>` of peptide fragments generated from a protein sample with a database of predicted
        :term:`spectra`, in order to identify the protein that produced the observed peptides.

    metabolomics
        Metabolomics is the study of the small molecules, or metabolites, produced by living organisms. It aims to
        identify and measure the complete set of metabolites in a biological sample and understand how they change in
        response to various factors. Metabolomics can provide insights into disease mechanisms, drug efficacy,
        and other aspects of human health and biology.

    mass spectrometer
        An instrument that measures the mass-to-charge ratio of ions in a sample, producing a :term:`mass spectrum`
        (see :term:`mass spectrometry`).

    LC-MS
    LCMS
        :term:`Liquid chromatography<liquid chromatography>`-coupled mass spectrometry.

    LC-MS/MS
    liquid chromatography coupled :term:`tandem mass spectrometry`
        See :term:`LC-MS` and :term:`MS2`.

    liquid chromatography
    LC
        An analytical technique used to separate molecules of interest.

    mass spectrometry
    MS
        Mass spectrometry is an analytical technique used to identify and quantify molecules of interest.

    FASTA
        A text-based format for representing nucleotide or amino acid sequences.

    C18
    octadecyl
        Octadecyl (C18) is an alkyl radical C(18)H(37) derived from an octadecane by removal of one hydrogen atom.

    ESI
    electrospray ionization
        Electrospray ionization (ESI) is a technique used in :term:`MS` to produce ions.

    MS2
    MS/MS
    tandem mass spectrometry
        Tandem :term:`MS` is a technique where two or more mass analyzers are coupled together using an additional reaction step to increase their abilities to analyse chemical samples.

    TOF
    time-of-flight
        Time-of-flight (TOF) is the time taken by an object, particle of wave (be it acoustic, electromagnetic, e.t.c) to travel a distance through a medium.

    quadrupole
        A mass filter allowing one mass channel at a time to reach the detector as the mass range is scanned.

    orbitrap
        In :term:`MS`, an ion trap mass analyzer consisting of an outer barrel-like electrode and a coaxial inner
        spindle-like electrode that traps ions in an orbital motion around the spindle.
        A high resolution :term:`MS` analyzer.

    MS1
        :term:`Mass spectra<mass spectrum>` of a sample from a single fragmentation step.

    MS3
        Multi-stage :term:`MS`

    CID
    collision-induced dissociation
        Collision-induced dissociation is a :term:`MS` technique to induce fragmentation of selected ions in the gas phase.

    TOPP
        The OpenMS Pipeline is a set of chainable tools to create pipelines for :term:`mass spectrometry` analysis.

    MSGFPlusAdapter
        Adapter for the MS-GF+ protein identification (database search) engine. More information is available in the
        `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_MSGFPlusAdapter.html>`__.

    LuciphorAdapter
        Adapter for the LuciPHOr2: a site localisation tool of generic post-translational modifications from tandem mass
        spectrometry data. More information is available in the `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_LuciphorAdapter.html>`__.

    pyopenms
    pyOpenMS
        pyOpenMS is an open-source Python library for :term:`MS`, specifically for the analysis of :term:`proteomics` and
        metabolomics data in Python.

    TOPP tools
        OpenMS provides a number of functions that process :term:`MS` data called :term:`TOPP` tools. All :term:`TOPP`
        tools are described in the `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/TOPP_documentation.html>`__.

    UTILS
        Besides :term:`TOPP tools`, OpenMS offers a range of other tools. They are not included in :term:`TOPP` as they
        are not part of typical analysis pipelines. More information is present in `OpenMS API reference documentation <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/UTILS_documentation.html>`__.

    TOPPView
        TOPPView is a viewer for MS and HPLC-MS data.

    nightly snapshot
        Untested installers and containers are known as the nightly snapshot.

    proteomics
        Proteomics is the large-scale study of proteins.

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
        The mzML format is an open, XML-based format for :term:`mass spectrometer` output files, developed with the full participation
        of vendors and researchers in order to create a single open format that would be supported by all software.

    mzData
    mzdata
        mzData was the first attempt by the Proteomics Standards Initiative (PSI) from the Human Proteome Organization (HUPO)
        to create a standardized format for :term:`MS` data. This format is now deprecated, and replaced by mzML.

    mzXML
    mzxml
        mzXML is an open data format for storage and exchange of mass spectroscopy data, developed at the SPC/Institute for
        Systems Biology.

    spectra
    spectrum
    mass spectrum
        A mass spectrum is a plot of the ion signal as a function of the mass-to-charge ratio. A mass spectrum
        is produced by a single :term:`MS` run. These spectra are used to determine the elemental or isotopic signature
        of a sample, the masses of particles and of molecules, and to elucidate the chemical identity or structure of
        molecules and other chemical compounds. OpenMS represents a one dimensional mass spectrum using the class `MSSpectrum <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1MSSpectrum.html>`_.

    ProteoWizard
        ProteoWizard is a set of open-source, cross-platform tools and libraries for :term:`proteomics` data analyses.
        It provides a framework for unified :term:`MS` data file access and performs standard chemistry and LCMS dataset computations.

    PepNovo
        PepNovo is a de :term:`de novo peptide sequencing` algorithm for :term:`MS2` :term:`spectra`.

    de novo peptide sequencing
        A peptide’s amino acid sequence is inferred directly from the precursor peptide mass and tandem
        :term:`mass spectrum` (:term:`MS2` or :term:`MS3`) fragment ions, without comparison to a reference proteome.

    TOPPAS
        An assistant for GUI-driven :term:`TOPP` workflow design. It is recommended to use OpenMS through the KNIME plugins.

    chromatograms
    chromatogram
        A two-dimensional plot that describes the amount of analyte eluted from a chromatography versus the analyte's
        retention time. OpenMS represents a chromatogram using the class `MSChromatogram <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/structOpenMS_1_1Interfaces_1_1Chromatogram.html>`_.

    KNIME
        An advanced workflow editor which OpenMS provides a plugin for.

    SILAC
    stable isotope labeling with amino acids in cell culture
        Stands for Stable isotope labeling using amino acids in cell culture.

    iTRAQ
        Stands for isobaric tags for relative and absolute quantitation.

    TMT
        Tandem Mass Tag (TMT) is a :term:`MS` based system designed to identify and quantify proteins in different samples.

    SRM
        Selected reaction monitoring is a :term:`MS` technique for small molecule analysis.

    SWATH
        Stands for sequential acquisition of all theoretical fragment ion spectra.

    OpenMS API
        An interface that allows developers to use OpenMS core library classes and methods.

    features
    feature
        An :term:`LC-MS` feature represents the combined isotopic mass traces of a detected chemical compound.
        The chromatographic peak shape of a feature is defined by the interaction of the analyte with the LC column.
        Each feature contains information on retention time, mass-to-charge ratio, intensity and overall quality.
        OpenMS represents a feature using the class `Feature <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1Feature.html>`_.

    feature maps
    feature map
        A feature map is a collection of :term:`features` identified in a :term:`mass spectrum` from a single experiment.
        One feature map can contain many :term:`features`. OpenMS represents a feature map using the class `FeatureMap <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1FeatureMap.html>`_.

    consensus features
    consensus feature
        Features from replicate experiments with similar retention times and m/z values are linked and considered a consensus feature.
        A consensus feature contains information on the common retention time and m/z values as well as intensities for each sample. OpenMS represents a consensus feature using the class `ConsensusFeature <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1ConsensusFeature.html>`_.

    consensus maps
    consensus map
        A consensus map is a collection of :term:`consensus features` identified from mass :term:`spectra` across replicate experiments.
        One consensus map can contain many consensus :term:`features`. OpenMS represents a consensus map using the class `ConsensusMap <https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/nightly/html/classOpenMS_1_1ConsensusMap.html>`_.
