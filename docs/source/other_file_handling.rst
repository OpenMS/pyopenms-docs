Reading MS data formats
=======================

Identification data (idXML, mzIdentML, pepXML, protXML)
-------------------------------------------------------

You can store and load identification data from an `idXML` file as follows:

.. code-block:: python

    import urllib
    from pyopenms import *
    gh = "https://raw.githubusercontent.com/OpenMS/OpenMS/develop"
    urllib.urlretrieve (gh +"/src/tests/class_tests/openms/data/IdXMLFile_whole.idXML", "test.idXML")
    protein_ids = []
    peptide_ids = []
    IdXMLFile().load("test.idXML", protein_ids, peptide_ids)
    IdXMLFile().store("test.out.idXML", protein_ids, peptide_ids)

You can store and load identification data from an `mzIdentML` file as follows:

.. code-block:: python

    import urllib
    from pyopenms import *
    gh = "https://raw.githubusercontent.com/OpenMS/OpenMS/develop"
    urllib.urlretrieve (gh + "/src/tests/class_tests/openms/data/MzIdentML_3runs.mzid", "test.mzid")
    protein_ids = []
    peptide_ids = []
    MzIdentMLFile().load("test.mzid", protein_ids, peptide_ids)
    MzIdentMLFile().store("test.out.mzid", protein_ids, peptide_ids)
..  # alternatively: -- dont do this, doesnt work
    identifications = Identification()
    MzIdentMLFile().load("test.mzid", identifications)

You can store and load identification data from a TPP `pepXML` file as follows:
    
.. code-block:: python

    import urllib
    from pyopenms import *
    gh = "https://raw.githubusercontent.com/OpenMS/OpenMS/develop"
    urllib.urlretrieve (gh + "/src/tests/class_tests/openms/data/PepXMLFile_test.pepxml", "test.pepxml")
    protein_ids = []
    peptide_ids = []
    PepXMLFile().load("test.pepxml", protein_ids, peptide_ids)
    PepXMLFile().store("test.out.pepxml", protein_ids, peptide_ids)
    

You can store and load identification data from a TPP `protXML` file as follows:

.. code-block:: python

    import urllib
    from pyopenms import *
    gh = "https://raw.githubusercontent.com/OpenMS/OpenMS/develop"
    urllib.urlretrieve (gh + "/src/tests/class_tests/openms/data/ProtXMLFile_input_1.protXML", "test.protXML")
    protein_ids = ProteinIdentification()
    peptide_ids = PeptideIdentification()
    ProtXMLFile().load("test.protXML", protein_ids, peptide_ids)
    # storing protein XML file is not yet supported
..    ProtXMLFile().store("test.out.protXML", protein_ids, peptide_ids, "doc_id_42")


note how each data file produces two vectors of type ``ProteinIdentification``
and ``PeptideIdentification`` which also means that conversion between two data
types is trivial: load data from one data file and use the storage function of
the other file. 


Transition data (TraML)
-------------------------------------------------------


.. code-block:: python

    import urllib
    from pyopenms import *
    gh = "https://raw.githubusercontent.com/OpenMS/OpenMS/develop"
    urllib.urlretrieve (gh + "/src/tests/topp/ConvertTSVToTraML_output.TraML", "test.TraML")
    targeted_exp = TargetedExperiment()
    TraMLFile().load("test.TraML", targeted_exp)
    TraMLFile().store("test.out.TraML", targeted_exp)



