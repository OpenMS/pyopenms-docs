Identification Data
====================

In OpenMS, identifications of peptides, proteins and small molecules are stored
in dedicated data structures. These data structures are typically stored to disc
as idXML or mzIdentML file. The highest-level structure is
``ProteinIdentification``. It stores all identified proteins of an identification
run as ProteinHit objects plus additional metadata (search parameters, etc.). Each
``ProteinHit`` contains the actual protein accession, an associated score, and
(optionally) the protein sequence. 

A ``PeptideIdentification`` object stores the
data corresponding to a single identified spectrum or feature. It has members
for the retention time, m/z, and a vector of ``PeptideHit`` objects. Each ``PeptideHit``
stores the information of a specific peptide-to-spectrum match or PSM (e.g., the score
and the peptide sequence). Each ``PeptideHit`` also contains a vector of
``PeptideEvidence`` objects which store the reference to one or more (in the case the
peptide maps to multiple proteins) proteins and the position therein.

.. NOTE::
   Protein Ids are linked to Peptide Ids by a common identifier (e.g., a unique string of time and date of the search).
   The Identifier can be set using the `setIdentifier` method. Similarly `getIdentifier` can be used to check the link between them.
   With the link one can retrieve search meta data (which is stored at the protein level) for individual Peptide Ids.

   .. code-block:: python

       protein_id = ProteinIdentification()
       peptide_id = PeptideIdentification()
       
       # Sets the Identifier
       protein_id.setIdentifier("IdentificationRun1")
       peptide_id.setIdentifier("IdentificationRun1")

       # Prints the Identifier
       print("Protein Identifier -", protein_id.getIdentifier())
       print("Peptide Identifier -", peptide_id.getIdentifier())
    
   .. code-block:: output
       
       Protein Identifier - IdentificationRun1
       Peptide Identifier - IdentificationRun1

ProteinIdentification
**********************

We can create an object of type ``ProteinIdentification``  and populate it with
``ProteinHit`` objects as follows: 

.. see doc/code_examples/Tutorial_IdentificationClasses.cpp

.. code-block:: python
  :linenos:

  from pyopenms import *

  # Create new protein identification object corresponding to a single search
  protein_id = ProteinIdentification()
  protein_id.setIdentifier("IdentificationRun1")

  # Each ProteinIdentification object stores a vector of protein hits
  protein_hit = ProteinHit()
  protein_hit.setAccession("sp|MyAccession")
  protein_hit.setSequence("PEPTIDERDLQMTQSPSSLSVSVGDRPEPTIDE")
  protein_hit.setScore(1.0)
  protein_hit.setMetaValue("target_decoy", b"target") # its a target protein

  protein_id.setHits([protein_hit])

We have now added a single ``ProteinHit`` with the accession ``sp|MyAccession`` to
the ``ProteinIdentification`` object (note how on line 14 we directly added a
list of size 1).  We can continue to add meta-data for the whole identification
run (such as search parameters):

.. code-block:: python
  :linenos:

  now = DateTime.now()
  date_string = now.getDate()
  protein_id.setDateTime(now)

  # Example of possible search parameters
  search_parameters = SearchParameters() # ProteinIdentification::SearchParameters
  search_parameters.db = "database"
  search_parameters.charges = "+2"
  protein_id.setSearchParameters(search_parameters)

  # Some search engine meta data
  protein_id.setSearchEngineVersion("v1.0.0")
  protein_id.setSearchEngine("SearchEngine")
  protein_id.setScoreType("HyperScore")

  # Iterate over all protein hits
  for hit in protein_id.getHits():
    print("Protein hit accession:", hit.getAccession())
    print("Protein hit sequence:", hit.getSequence())
    print("Protein hit score:", hit.getScore())


PeptideIdentification
**********************

Next, we can also create a ``PeptideIdentification`` object and add
corresponding ``PeptideHit`` objects:

.. code-block:: python
  :linenos:

  peptide_id = PeptideIdentification()

  peptide_id.setRT(1243.56)
  peptide_id.setMZ(440.0)
  peptide_id.setScoreType("ScoreType")
  peptide_id.setHigherScoreBetter(False)
  peptide_id.setIdentifier("IdentificationRun1")

  # define additional meta value for the peptide identification
  peptide_id.setMetaValue("AdditionalMetaValue", "Value")

  # create a new PeptideHit (best PSM, best score)
  peptide_hit = PeptideHit()
  peptide_hit.setScore(1.0)
  peptide_hit.setRank(1)
  peptide_hit.setCharge(2)
  peptide_hit.setSequence(AASequence.fromString("DLQM(Oxidation)TQSPSSLSVSVGDR"))
  
  ev = PeptideEvidence()
  ev.setProteinAccession("sp|MyAccession")
  ev.setAABefore(b"R")
  ev.setAAAfter(b"P")
  ev.setStart(123) # start and end position in the protein
  ev.setEnd(141)
  peptide_hit.setPeptideEvidences([ev])

  # create a new PeptideHit (second best PSM, lower score)
  peptide_hit2 = PeptideHit()
  peptide_hit2.setScore(0.5)
  peptide_hit2.setRank(2)
  peptide_hit2.setCharge(2)
  peptide_hit2.setSequence(AASequence.fromString("QDLMTQSPSSLSVSVGDR"))
  peptide_hit2.setPeptideEvidences([ev])
  
  # add PeptideHit to PeptideIdentification
  peptide_id.setHits([peptide_hit, peptide_hit2])
  
This allows us to represent single spectra (``PeptideIdentification`` at *m/z*
440.0 and *rt* 1234.56) with possible identifications that are ranked by score.
In this case, apparently two possible peptides match the spectrum which have
the first three amino acids in a different order "DLQ" vs "QDL").

We can now display the peptides we just stored:

.. code-block:: python

  # Iterate over PeptideIdentification
  peptide_ids = [peptide_id]
  for peptide_id in peptide_ids:
    # Peptide identification values
    print ("Peptide ID m/z:", peptide_id.getMZ())
    print ("Peptide ID rt:", peptide_id.getRT())
    print ("Peptide ID score type:", peptide_id.getScoreType())
    # PeptideHits
    for hit in peptide_id.getHits():
      print(" - Peptide hit rank:", hit.getRank())
      print(" - Peptide hit sequence:", hit.getSequence())
      print(" - Peptide hit score:", hit.getScore())
      print(" - Mapping to proteins:", [ev.getProteinAccession() 
                                          for ev in hit.getPeptideEvidences() ] )



Storage on disk
***************

Finally, we can store the peptide and protein identification data in a
``idXML`` file (a OpenMS internal file format which we have previously
discussed `here
<other_file_handling.html#identification-data-idxml-mzidentml-pepxml-protxml>`_)
which we would do as follows:

.. code-block:: python
  :linenos:

  # Store the identification data in an idXML file  
  IdXMLFile().store("out.idXML", [protein_id], peptide_ids)
  # and load it back into memory
  prot_ids = []; pep_ids = []
  IdXMLFile().load("out.idXML", prot_ids, pep_ids)

  # Iterate over all protein hits
  for protein_id in prot_ids:
    for hit in protein_id.getHits():
      print("Protein hit accession:", hit.getAccession())
      print("Protein hit sequence:", hit.getSequence())
      print("Protein hit score:", hit.getScore())
      print("Protein hit target/decoy:", hit.getMetaValue("target_decoy"))

  # Iterate over PeptideIdentification
  for peptide_id in pep_ids:
    # Peptide identification values
    print ("Peptide ID m/z:", peptide_id.getMZ())
    print ("Peptide ID rt:", peptide_id.getRT())
    print ("Peptide ID score type:", peptide_id.getScoreType())
    # PeptideHits
    for hit in peptide_id.getHits():
      print(" - Peptide hit rank:", hit.getRank())
      print(" - Peptide hit sequence:", hit.getSequence())
      print(" - Peptide hit score:", hit.getScore())
      print(" - Mapping to proteins:", [ev.getProteinAccession() for ev in hit.getPeptideEvidences() ] )

You can inspect the ``out.idXML`` XML file produced here, and you will find a ``<ProteinHit>`` entry for the protein that we stored and two ``<PeptideHit>`` entries for the two peptides stored on disk.
