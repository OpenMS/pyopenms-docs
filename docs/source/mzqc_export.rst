Quality Control 
===============

With ``MzQCFile`` pyOpenMS provides a tool to export quality control data from an experiment to a mzQC file following the
`HUPO-PSI specifications
<https://github.com/HUPO-PSI/mzQC>`_. MzQC is a reporting and exchange format for mass spectrometry
quality control data in JSON format.

``MzQCFile.store()`` requires, besides the ``input_file`` and ``output_file`` path, at least a ``MSExperiment``. Optionally, 
a ``FeatureMap`` and/or lists of ``ProteinIdentification`` and ``PeptideIdentification`` can be provided to calculate additional
proteomics and metabolomics quality metrics.

.. code-block:: python

    from pyopenms import *

    from urllib.request import urlretrieve
    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"

    # minimal required informations are input_file, output_file and a MSExperiment
    input_file = 'QCCalculator_input.mzML'
    output_file = 'result.mzQC'

    # load mzML file in MSExperiment
    urlretrieve (gh + "/src/data/QCCalculator_input.mzML", 'input.mzML')
    exp = MSExperiment()
    MzMLFile().load('input.mzML', exp)

    # prepare metadata for the mzQC file (optional but recommended)
    contact_name = 'name of the person creating the mzQC file'
    contact_address = 'contact address (mail/e-mail or phone) of the person creating the mzQC file'
    description = 'description and comments about the mzQC file contents'
    label = 'unique and informative label for the run'

    feature_map = FeatureMap()
    # OPTIONAL: load featureXML file in FeatureMap()
    urlretrieve (gh + "/src/data/FeatureFinderMetaboIdent_1_output.featureXML", 'features.featureXML')
    FeatureXMLFile().load('features.featureXML', feature_map)

    prot_ids = [] # list of ProteinIdentification()
    pep_ids = [] # list of PeptideIdentification()
    # OPTIONAL: get protein and peptide identifications from idXML file
    urlretrieve (gh + "/src/data/OpenPepXL_output.idXML", 'ids.idXML')
    IdXMLFile().load('ids.idXML', prot_ids, pep_ids)

    # create MzQCFile object and use store() to calculate and write the mzQC file
    mzqc = MzQCFile()
    mzqc.store(input_file, output_file, exp, # minimal required information
            contact_name, contact_address, description, label, # optional, but recommended, can be empty
            feature_map, prot_ids, pep_ids) # optional, can be empty
