Peptides and Proteins
=====================

Amino Acid Sequences
********************

The ``AASequence`` class handles amino acid sequences in OpenMS. A string of
amino acid residues can be turned into a instance of ``AASequence`` to provide
some commonly used operations and data. The implementation supports
mathematical operations like addition or subtraction. Also, average and mono
isotopic weight and isotope distributions are accessible.

Weights, formulas and isotope distribution can be calculated depending on the
charge state (additional proton count in case of positive ions) and ion type.
Therefore, the class allows for a flexible handling of amino acid strings.

A very simple example of handling amino acid sequence with AASequence is given
in the next few lines, which also calculates the weight of the ``(M)`` and ``(M+2H)2+``
ions.

.. code-block:: python
    :linenos:

    from pyopenms import *
    seq = AASequence.fromString("DFPIANGER")
    prefix = seq.getPrefix(4)
    suffix = seq.getSuffix(5)
    concat = seq + seq

    print(seq)
    print(concat)
    print(suffix)
    mfull = seq.getMonoWeight() # weight of M
    mprecursor = seq.getMonoWeight(Residue.ResidueType.Full, 2) # weight of M+2H
    mz = seq.getMonoWeight(Residue.ResidueType.Full, 2) / 2.0 # m/z of M+2H
    
    print()
    print("Monoisotopic mass of peptide [M] is", mfull)
    print("Monoisotopic mass of peptide precursor [M+2H]2+ is", mprecursor)
    print("Monoisotopic m/z of [M+2H]2+ is", mz)
    
Which prints the amino acid sequence on line 7 as well as the result of
concatenating two sequences or taking the suffix of a sequence (lines 8 and 9).
On line 10 we compute the mass of the full peptide (``[M]``), on line 11 we
compute the mass of the peptide precursor (``[M+2H]2+``) while on line 12 we
compute the ``m/z`` value of the peptide precursor (``[M+2H]2+``). The mass of
the peptide precursor is shifted by two protons that are now attached to the
molecules as charge carriers (note that the proton mass of 1.007276 u is
slightly different from the mass of an uncharged hydrogen atom at 1.007825 u).

.. code-block:: python

    DFPIANGER
    DFPIANGERDFPIANGER
    ANGER

    Monoisotopic mass of peptide [M] is 1017.4879641373001
    Monoisotopic mass of peptide precursor [M+2H]2+ is 1019.5025170708421
    Monoisotopic m/z of [M+2H]2+ is 509.7512585354211


The ``AASequence`` object also allows iterations directly in Python:

.. code-block:: python
    :linenos:

    from pyopenms import *
    seq = AASequence.fromString("DFPIANGER")

    print("The peptide", str(seq), "consists of the following amino acids:")
    for aa in seq:
      print(aa.getName(), ":", aa.getMonoWeight())
    
Which will print

.. code-block:: python

    The peptide DFPIANGER consists of the following amino acids:
    Aspartate : 133.0375092233
    Phenylalanine : 165.0789793509
    Proline : 115.0633292871
    Isoleucine : 131.0946294147
    Alanine : 89.04767922330001
    Asparagine : 132.0534932552
    Glycine : 75.0320291595
    Glutamate : 147.05315928710002
    Arginine : 174.1116764466


Fragment ions
~~~~~~~~~~~~~

Note how we can easily calculate the charged weight of a ``(M+2H)2+`` ion on line 11
and compute *m/z* on line 12 -- simply dividing by the charge.
We can now combine our knowledge of ``AASequence`` with what we learned above
about ``EmpiricalFormula`` to get accurate mass and isotope distributions from
the amino acid sequence:

.. code-block:: python
    :linenos:

    from pyopenms import *
    seq = AASequence.fromString("DFPIANGER")
    seq_formula = seq.getFormula()
    print("Peptide", seq, "has molecular formula", seq_formula)
    print("="*35)

    isotopes = seq_formula.getIsotopeDistribution( CoarseIsotopePatternGenerator(6) )
    for iso in isotopes.getContainer():
      print ("Isotope", iso.getMZ(), "has abundance", iso.getIntensity()*100, "%")

    suffix = seq.getSuffix(3) # y3 ion "GER"
    print("="*35)
    print("y3 ion sequence:", suffix)
    y3_formula = suffix.getFormula(Residue.ResidueType.YIon, 2) # y3++ ion
    suffix.getMonoWeight(Residue.ResidueType.YIon, 2) / 2.0 # CORRECT
    suffix.getMonoWeight(Residue.ResidueType.XIon, 2) / 2.0 # CORRECT
    suffix.getMonoWeight(Residue.ResidueType.BIon, 2) / 2.0 # INCORRECT

    print("y3 mz:", suffix.getMonoWeight(Residue.ResidueType.YIon, 2) / 2.0 )
    print("y3 molecular formula:", y3_formula)

Which will produce

.. code-block:: python

    Peptide DFPIANGER has molecular formula C44H67N13O15
    ===================================
    Isotope 1017.4879641373 has abundance 56.81651830673218 %
    Isotope 1018.4913189751 has abundance 30.52912950515747 %
    Isotope 1019.4946738129 has abundance 9.802105277776718 %
    Isotope 1020.4980286507 has abundance 2.3292064666748047 %
    Isotope 1021.5013834885 has abundance 0.4492596257477999 %
    Isotope 1022.5047383263 has abundance 0.07378293084912002 %
    ===================================
    y3 ion sequence: GER
    y3 mz: 181.09514385
    y3 molecular formula: C13H24N6O6


Note on lines 15 to 17 we need to remember that we are dealing with an ion of
the x/y/z series since we used a suffix of the original peptide and using any
other ion type will produce a different mass-to-charge ratio (and while "GER"
would also be a valid "x3" ion, note that it *cannot* be a valid ion from the
a/b/c series and therefore the mass on line 17 cannot refer to the same input
peptide "DFPIANGER" since its "b3" ion would be "DFP" and not "GER"). 

Modified Sequences
******************

The ``AASequence`` class can also handle modifications, 
modifications are specified using a unique string identifier present in the
``ModificationsDB`` in round brackets after the modified amino acid or by providing
the mass of the residue in square brackets. For example
``AASequence.fromString(".DFPIAM(Oxidation)GER.")`` creates an instance of the
peptide "DFPIAMGER" with an oxidized methionine. There are multiple ways to specify modifications, and
``AASequence.fromString("DFPIAM(UniMod:35)GER")``,
``AASequence.fromString("DFPIAM[+16]GER")`` and
``AASequence.fromString("DFPIAM[147]GER")`` are all equivalent). 


.. code-block:: python

        from pyopenms import *
        seq = AASequence.fromString("PEPTIDESEKUEM(Oxidation)CER")
        print(seq.toUnmodifiedString())
        print(seq.toString())
        print(seq.toUniModString())
        print(seq.toBracketString())
        print(seq.toBracketString(False))

        print(AASequence.fromString("DFPIAM(UniMod:35)GER"))
        print(AASequence.fromString("DFPIAM[+16]GER"))
        print(AASequence.fromString("DFPIAM[+15.99]GER"))
        print(AASequence.fromString("DFPIAM[147]GER"))
        print(AASequence.fromString("DFPIAM[147.035405]GER"))

The above code outputs:

.. code-block:: python

    PEPTIDESEKUEMCER
    PEPTIDESEKUEM(Oxidation)CER
    PEPTIDESEKUEM(UniMod:35)CER
    PEPTIDESEKUEM[147]CER
    PEPTIDESEKUEM[147.0354000171]CER

    DFPIAM(Oxidation)GER
    DFPIAM(Oxidation)GER
    DFPIAM(Oxidation)GER
    DFPIAM(Oxidation)GER
    DFPIAM(Oxidation)GER

Note there is a subtle difference between
``AASequence.fromString(".DFPIAM[+16]GER.")`` and
``AASequence.fromString(".DFPIAM[+15.9949]GER.")`` - while the former will try to
find the first modification matching to a mass difference of 16 +/- 0.5, the
latter will try to find the closest matching modification to the exact mass.
The exact mass approach usually gives the intended results while the first
approach may or may not. In all instances, it is better to use an exact description of the desired modification, such as UniMod, instead of mass differences.

N- and C-terminal modifications are represented by brackets to the right of the dots
terminating the sequence. For example, ``".(Dimethyl)DFPIAMGER."`` and
``".DFPIAMGER.(Label:18O(2))"`` represent the labelling of the N- and C-terminus
respectively, but ``".DFPIAMGER(Phospho)."`` will be interpreted as a
phosphorylation of the last arginine at its side chain:

.. code-block:: python

        from pyopenms import *
        s = AASequence.fromString(".(Dimethyl)DFPIAMGER.")
        print(s, s.hasNTerminalModification())
        s = AASequence.fromString(".DFPIAMGER.(Label:18O(2))")
        print(s, s.hasCTerminalModification())
        s = AASequence.fromString(".DFPIAMGER(Phospho).")
        print(s, s.hasCTerminalModification())

Arbitrary/unknown amino acids (usually due to an unknown modification) can be
specified using tags preceded by X: "X[weight]". This indicates a new amino
acid ("X") with the specified weight, e.g. ``"RX[148.5]T"``. Note that this tag
does not alter the amino acids to the left (R) or right (T). Rather, X
represents an amino acid on its own. Be careful when converting such AASequence
objects to an EmpiricalFormula using ``getFormula()``, as tags will not be
considered in this case (there exists no formula for them). However, they have
an influence on ``getMonoWeight()`` and ``getAverageWeight()``! 

Proteins
********

Protein sequences can be accessed through the ``FASTAEntry`` object and can be
read and stored on disk using a ``FASTAFile``:

.. code-block:: python

        from pyopenms import *
        bsa = FASTAEntry()
        bsa.sequence = "MKWVTFISLLLLFSSAYSRGVFRRDTHKSEIAHRFKDLGE"
        bsa.description = "BSA Bovine Albumin (partial sequence)"
        bsa.identifier = "BSA"
        alb = FASTAEntry()
        alb.sequence = "MKWVTFISLLFLFSSAYSRGVFRRDAHKSEVAHRFKDLGE" 
        alb.description = "ALB Human Albumin (partial sequence)"
        alb.identifier = "ALB"

        entries = [bsa, alb]

        f = FASTAFile()
        f.store("example.fasta", entries)

Afterwards, the ``example.fasta`` file can be read again from disk:

.. code-block:: python

        from pyopenms import *
        entries = []
        f = FASTAFile()
        f.load("example.fasta", entries)
        print( len(entries) )
        for e in entries:
          print (e.identifier, e.sequence)

.. image:: ./img/launch-binder.jpg
   :target: https://mybinder.org/v2/gh/OpenMS/pyopenms-extra/master+ipynb?urlpath=lab/tree/docs/source/aasequences.ipynb
   :alt: Launch Binder


