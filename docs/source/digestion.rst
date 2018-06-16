Digestion
=========

Protease
********

OpenMS has classes for proteolytic digestion which can be used as follows:

.. code-block:: python

    from pyopenms import *
    import urllib
    urllib.urlretrieve ("http://www.uniprot.org/uniprot/P02769.fasta", "bsa.fasta")

    dig = EnzymaticDigestion()
    pd.getEnzymeName() # Trypsin
    bsa = "".join([l.strip() for l in open("bsa.fasta").readlines()[2:]])
    bsa = AASequence.fromString(bsa, True)
    result = []
    dig.digest(bsa, result)
    len(result) # 74 peptides


.. in 2.4 : 
    dig = ProteaseDigestion()
    dig.digest(bsa, result, 1, 0)


