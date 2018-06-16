Digestion
=========

Proteolytic Digestion with Trypsin
**********************************

OpenMS has classes for proteolytic digestion which can be used as follows:

.. code-block:: python

    from pyopenms import *
    import urllib
    urllib.urlretrieve ("http://www.uniprot.org/uniprot/P02769.fasta", "bsa.fasta")

    dig = EnzymaticDigestion()
    dig.getEnzymeName() # Trypsin
    bsa = "".join([l.strip() for l in open("bsa.fasta").readlines()[2:]])
    bsa = AASequence.fromString(bsa, True)
    result = []
    dig.digest(bsa, result)
    print(result[4])
    len(result) # 74 peptides


.. in 2.4 : 
    dig = ProteaseDigestion()
    dig.digest(bsa, result, 1, 0)

Proteolytic Digestion with Lys-C
********************************

We can of course also use different enzymes, these are defined ``Enzyme.xml``
file and can be accessed using the ``EnzymesDB``

.. code-block:: python

    names = []
    EnzymesDB().getAllNames(names)
    len(names) # 25 by default
    e = EnzymesDB().getEnzyme('Lys-C')
    e.getRegExDescription()
    e.getRegEx()

.. in 2.4 : 
    ProteaseDB()

Now that we have learned about the other enzymes available, we can use it to
cut out protein of interest:

.. code-block:: python

    from pyopenms import *
    import urllib
    urllib.urlretrieve ("http://www.uniprot.org/uniprot/P02769.fasta", "bsa.fasta")

    dig = EnzymaticDigestion()
    dig.setEnzyme('Lys-C')
    bsa = "".join([l.strip() for l in open("bsa.fasta").readlines()[2:]])
    bsa = AASequence.fromString(bsa, True)
    result = []
    dig.digest(bsa, result)
    print(result[4])
    len(result) # 53 peptides

.. in 2.4 : 
    dig = ProteaseDigestion()
    dig.digest(bsa, result, 1, 0)

We now get different digested peptides (53 vs 74) and the fourth peptide is now
``VASLRETYGDMADCCEK`` instead of ``VASLR`` as with Trypsin (see above).

