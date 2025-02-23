Digestion
=========

In ``top-down proteomics``, whole proteins are measured in the mass spec.
It is a hard problem to know the exact protein sequence, since proteins
can be very large, i.e. have a very long sequence of constituing amino acids.

However, in an orthogonal approach called ``bottom-up proteomics``,
it is usually more beneficial to first cut proteins into smaller
chunks at defined positions by using enzymatic digestion. The resulting peptides
are lighter in mass, have less charge, and their sequence can be readily determined
using MS/MS in many cases. In a subsequent step, one needs to infer which proteins
were present in the sample, given a set of peptide sequences - a process called protein inference.
The usual enzyme of choice for bottom-up proteomics is ``Trypsin`` (sometimes in combination with Lys-C).

We will now learn how to do digestion of protein sequences in-silico, so you can predict which
peptides you can expect to observe in the data and even generate theoretical spectra for them.

Proteolytic Digestion with Trypsin
**********************************

OpenMS has classes for proteolytic digestion which can be used as follows:

.. code-block:: python

    import pyopenms as oms
    from urllib.request import urlretrieve

    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-docs/master"
    urlretrieve(gh + "/src/data/P02769.fasta", "bsa.fasta")

    dig = oms.ProteaseDigestion()
    dig.getEnzymeName()  # Trypsin
    bsa = "".join([l.strip() for l in open("bsa.fasta").readlines()[1:]])
    bsa = oms.AASequence.fromString(bsa)
    # create all digestion products
    result = []
    dig.digest(bsa, result)
    print(result[4].toString())
    len(result)  # 82 peptides

Very short peptides or even single amino acid digestion products are often discarded as they usually contain little information (e.g., are shared by many proteins making them useless to identify specific proteins or will not be detected in a real mass spectrum, since their peptide mass is below the usual minimal recorded mass).
We now only generate digestion products with a length of :math:`7` to :math:`40`.

.. code-block:: python

    # only create peptides of length 7-40
    dig.digest(bsa, result, 7, 40)
    # print the results
    for s in result:
        print(s.toString())

Enzymatic digestion is often not perfect and sometimes enzymes miss cutting position (aka cleavage site), resulting in some larger peptides. These are a sequence of two or even more consecutive peptides within the protein sequence.
We now allow up to two missed cleavages.

.. code-block:: python

    # Allow two missed cleavages
    dig.setMissedCleavages(2)
    # only create peptides of length 7-40
    dig.digest(bsa, result, 7, 40)
    # print the results
    for s in result:
        print(s.toString())

Proteolytic Digestion with Lys-C
********************************

In the previous example we used Trypsin as our enzyme of choice.
We can of course also use different enzymes, these are defined in the ``Enzymes.xml``
file and can be accessed using the :py:class:`~.EnzymesDB` object

.. code-block:: python

    names = []
    oms.ProteaseDB().getAllNames(names)
    len(names)  # at least 25 by default
    e = oms.ProteaseDB().getEnzyme("Lys-C")
    e.getRegExDescription()
    e.getRegEx()


Now that we have learned about the other enzymes available, we can use it to
cut our protein of interest:

.. code-block:: python

    from urllib.request import urlretrieve

    gh = "https://raw.githubusercontent.com/OpenMS/pyopenms-docs/master"
    urlretrieve(gh + "/src/data/P02769.fasta", "bsa.fasta")

    dig = oms.ProteaseDigestion()
    dig.setEnzyme("Lys-C")
    bsa = "".join([l.strip() for l in open("bsa.fasta").readlines()[1:]])
    bsa = oms.AASequence.fromString(bsa)
    result = []
    dig.digest(bsa, result)
    print(result[4].toString())
    len(result)  # 57 peptides

We now get different digested peptides (:math:`57` vs :math:`82`) and the fourth peptide is now
``GLVLIAFSQYLQQCPFDEHVK`` instead of ``DTHK`` as with Trypsin (see above).

Oligonucleotide Digestion
**************************

There are multiple cleavage enzymes available for oligonucleotides, these are defined ``Enzymes_RNA.xml``
file and can be accessed using the :py:class:`~.RNaseDB` object

.. code-block:: python

    db = oms.RNaseDB()
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

    oligo = oms.NASequence.fromString("pAUGUCGCAG")

    dig = oms.RNaseDigestion()
    dig.setEnzyme("RNase_T1")

    result = []
    dig.digest(oligo, result)
    for fragment in result:
        print(fragment)

    print("Looking closer at", result[0])
    print(" Five Prime modification:", result[0].getFivePrimeMod().getCode())
    print(" Three Prime modification:", result[0].getThreePrimeMod().getCode())
    for ribo in result[0]:
        print(ribo.getCode(), ribo.getMonoMass(), ribo.isModified())

