Digestion
=========

Proteolytic Digestion with Trypsin
**********************************

OpenMS has classes for proteolytic digestion which can be used as follows:

.. code-block:: python

    from pyopenms import *
    import urllib
    urllib.urlretrieve ("http://www.uniprot.org/uniprot/P02769.fasta", "bsa.fasta")

    dig = ProteaseDigestion()
    dig.getEnzymeName() # Trypsin
    bsa = "".join([l.strip() for l in open("bsa.fasta").readlines()[1:]])
    bsa = AASequence.fromString(bsa, True)
    result = []
    dig.digest(bsa, result)
    print(result[4])
    len(result) # 82 peptides


Proteolytic Digestion with Lys-C
********************************

We can of course also use different enzymes, these are defined ``Enzyme.xml``
file and can be accessed using the ``EnzymesDB``

.. code-block:: python

    names = []
    ProteaseDB().getAllNames(names)
    len(names) # at least 25 by default
    e = ProteaseDB().getEnzyme('Lys-C')
    e.getRegExDescription()
    e.getRegEx()


Now that we have learned about the other enzymes available, we can use it to
cut out protein of interest:

.. code-block:: python

    from pyopenms import *
    import urllib
    urllib.urlretrieve ("http://www.uniprot.org/uniprot/P02769.fasta", "bsa.fasta")

    dig = ProteaseDigestion()
    dig.setEnzyme('Lys-C')
    bsa = "".join([l.strip() for l in open("bsa.fasta").readlines()[1:]])
    bsa = AASequence.fromString(bsa, True)
    result = []
    dig.digest(bsa, result)
    print(result[4])
    len(result) # 57 peptides

We now get different digested peptides (57 vs 82) and the fourth peptide is now
``GLVLIAFSQYLQQCPFDEHVK`` instead of ``DTHK`` as with Trypsin (see above).

