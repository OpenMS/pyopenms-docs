Digestion
=========

Proteolytic Digestion with Trypsin
**********************************

OpenMS has classes for proteolytic digestion which can be used as follows:

.. code-block:: python

    from pyopenms import *
    from urllib.request import urlretrieve
    # from urllib import urlretrieve  # use this code for Python 2.x
    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"
    urlretrieve (gh + "/src/data/P02769.fasta", "bsa.fasta")

    dig = ProteaseDigestion()
    dig.getEnzymeName() # Trypsin
    bsa = "".join([l.strip() for l in open("bsa.fasta").readlines()[1:]])
    bsa = AASequence.fromString(bsa)
    result = []
    dig.digest(bsa, result)
    print(result[4].toString())
    len(result) # 82 peptides


Proteolytic Digestion with Lys-C
********************************

We can of course also use different enzymes, these are defined in the ``Enzymes.xml``
file and can be accessed using the ``EnzymesDB`` object

.. code-block:: python

    from pyopenms import *
    names = []
    ProteaseDB().getAllNames(names)
    len(names) # at least 25 by default
    e = ProteaseDB().getEnzyme('Lys-C')
    e.getRegExDescription()
    e.getRegEx()


Now that we have learned about the other enzymes available, we can use it to
cut our protein of interest:

.. code-block:: python

    from pyopenms import *
    from urllib.request import urlretrieve
    # from urllib import urlretrieve  # use this code for Python 2.x
    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-extra/master"
    urlretrieve (gh + "/src/data/P02769.fasta", "bsa.fasta")

    dig = ProteaseDigestion()
    dig.setEnzyme('Lys-C')
    bsa = "".join([l.strip() for l in open("bsa.fasta").readlines()[1:]])
    bsa = AASequence.fromString(bsa)
    result = []
    dig.digest(bsa, result)
    print(result[4].toString())
    len(result) # 57 peptides

We now get different digested peptides (57 vs 82) and the fourth peptide is now
``GLVLIAFSQYLQQCPFDEHVK`` instead of ``DTHK`` as with Trypsin (see above).

Oligonucleotide Digestion
**************************

There are multiple cleavage enzymes available for oligonucleotides, these are defined ``Enzymes_RNA.xml``
file and can be accessed using the ``RNaseDB`` object

.. code-block:: python

    from pyopenms import *
    db = RNaseDB()
    names = []
    db.getAllNames(names)
    names
    # Will print out all available enzymes:
    # ['RNase_U2', 'RNase_T1', 'RNase_H', 'unspecific cleavage', 'no cleavage', 'RNase_MC1', 'RNase_A', 'cusativin']
    e = db.getEnzyme("RNase_T1")
    e.getRegEx()
    e.getThreePrimeGain() 

We can now use it to cut an oligo:

.. code-block:: python

    from pyopenms import *
    oligo = NASequence.fromString("pAUGUCGCAG");

    dig = RNaseDigestion()
    dig.setEnzyme("RNase_T1")

    result = []
    dig.digest(oligo, result)
    for fragment in result:
      print (fragment)

    print("Looking closer at", result[0])
    print(" Five Prime modification:", result[0].getFivePrimeMod().getCode())
    print(" Three Prime modification:", result[0].getThreePrimeMod().getCode())
    for ribo in result[0]:
      print (ribo.getCode(), ribo.getMonoMass(), ribo.isModified())

.. image:: ./img/launch_binder.jpg
   :class: ignore
   :target: https://mybinder.org/v2/gh/OpenMS/pyopenms-extra/master+ipynb?urlpath=lab/tree/docs/source/digestion.ipynb
   :alt: Launch Binder


