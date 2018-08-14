Peptides and Proteins
=====================

AA Sequences
************

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
    seq = AASequence.fromString("DFPIANGER", True)
    prefix = seq.getPrefix(4)
    suffix = seq.getSuffix(5)
    concat = seq + seq

    print(seq)
    print(concat)
    print(suffix)
    seq.getMonoWeight(Residue.ResidueType.Full, 0)
    seq.getMonoWeight(Residue.ResidueType.Full, 2) / 2.0
    concat.getMonoWeight(Residue.ResidueType.Full, 0)

We can now combine our knowledge of ``AASequence`` with what we learned above
about ``EmpiricalFormula`` to get accurate mass and isotope distributions from
the amino acid sequence:

.. code-block:: python
    :linenos:

    seq_formula = seq.getFormula(Residue.ResidueType.Full, 0)
    print(seq_formula)

    isotopes = seq_formula.getIsotopeDistribution(6)
    for iso in isotopes.getContainer():
        print (iso)

    suffix = seq.getSuffix(3) # y3 ion "GER"
    print(suffix)
    y3_formula = suffix.getFormula(Residue.ResidueType.YIon, 2) # y3++ ion
    suffix.getMonoWeight(Residue.ResidueType.YIon, 2) / 2.0 # CORRECT
    suffix.getMonoWeight(Residue.ResidueType.XIon, 2) / 2.0 # CORRECT
    suffix.getMonoWeight(Residue.ResidueType.BIon, 2) / 2.0 # INCORRECT
    print(y3_formula)
    print(seq_formula)

..  isotopes = seq_formula.getIsotopeDistribution( CoarseIsotopePatternGenerator(6) )
    for iso in isotopes.getContainer():
        print (iso.getMZ(), iso.getIntensity())

Note on lines 11 to 13 we need to remember that we are dealing with an ion of
the x/y/z series since we used a suffix of the original peptide and using any
other ion type will produce a different mass-to-charge ratio (and while "GER"
would also be a valid "x3" ion, note that it *cannot* be a valid ion from the
a/b/c series and therefore the mass on line 13 cannot refer to the same input
peptide "DFPIANGER" since its "b3" ion would be "DFP" and not "GER").

Modified AA Sequences
*********************

The ``AASequence`` class can also handle modifications, 
modifications are specified using a unique string identifier present in the
``ModificationsDB`` in round brackets after the modified amino acid or by providing
the mass of the residue in square brackets. For example
``AASequence.fromString(".DFPIAM(Oxidation)GER.", True)`` creates an instance of the
peptide "DFPIAMGER" with an oxidized methionine. There are multiple ways to specify modifications, and
``AASequence.fromString("DFPIAM(UniMod:35)GER", True)``,
``AASequence.fromString("DFPIAM[+16]GER", True)`` and
``AASequence.fromString("DFPIAM[147]GER", True)`` are all equivalent). 

N- and C-terminal modifications are represented by brackets to the right of the dots
terminating the sequence. For example, ``".(Dimethyl)DFPIAMGER."`` and
``".DFPIAMGER.(Label:18O(2))"`` represent the labelling of the N- and C-terminus
respectively, but ``".DFPIAMGER(Phospho)."`` will be interpreted as a
phosphorylation of the last arginine at its side chain.

.. code-block:: python

        from pyopenms import *
        seq = AASequence.fromString("PEPTIDESEKUEM(Oxidation)CER", True)
        print(seq.toString())
        print(seq.toUnmodifiedString())
        print(seq.toBracketString(True, []))
        print(seq.toBracketString(False, []))

        print(AASequence.fromString("DFPIAM(UniMod:35)GER", True))
        print(AASequence.fromString("DFPIAM[+16]GER", True))
        print(AASequence.fromString("DFPIAM[+15.99]GER", True))
        print(AASequence.fromString("DFPIAM[147]GER", True))
        print(AASequence.fromString("DFPIAM[147.035405]GER", True))

..    print(seq.toUniModString()) # with 2.4

The above code outputs:

.. code-block:: python

    PEPTIDESEKUEM(Oxidation)CER
    PEPTIDESEKUEMCER
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
approach may or may not.

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
        alb.description = "ABL Human Albumin (partial sequence)"
        alb.identifier = "ABL"

        entries = [bsa, alb]

        f = pyopenms.FASTAFile()
        f.store("example.fasta", entries)

Afterwards, the protein sequences can be read again using:

.. code-block:: python

        from pyopenms import *
        entries = []
        f = FASTAFile()
        f.load("example.fasta", entries)
        print( len(entries) )
        for e in entries:
          print (e.identifier, e.sequence)


TheoreticalSpectrumGenerator
****************************

This class implements a simple generator which generates tandem MS spectra from
a given peptide charge combination. There are various options which influence
the occurring ions and their intensities.

.. code-block:: python

    from pyopenms import *

    tsg = TheoreticalSpectrumGenerator()
    spec1 = MSSpectrum()
    spec2 = MSSpectrum()
    peptide = AASequence.fromString("DFPIANGER", True)
    # standard behavior is adding b- and y-ions of charge 1
    p = Param()
    p.setValue("add_b_ions", "false", "Add peaks of b-ions to the spectrum")
    tsg.setParameters(p)
    tsg.getSpectrum(spec1, peptide, 1, 1)
    p.setValue("add_b_ions", "true", "Add peaks of a-ions to the spectrum")
    p.setValue("add_metainfo", "true", "")
    tsg.setParameters(p)
    tsg.getSpectrum(spec2, peptide, 1, 2)
    print("Spectrum 1 has", spec1.size(), "peaks.")
    print("Spectrum 2 has", spec2.size(), "peaks.")

    # Iterate over annotated ions and their masses
    for ion, peak in zip(spec2.getStringDataArrays()[0], spec2):
        print(ion, peak.getMZ())

which outputs:

.. code-block:: python

        Spectrum 1 has 8 peaks.
        Spectrum 2 has 30 peaks.

        y1++ 88.0631146901
        b2++ 132.05495569
        y2++ 152.584411802
        y1+ 175.118952913
        [...]

The example shows how to put peaks of a certain type, y-ions in this case, into
a spectrum. Spectrum 2 is filled with a complete spectrum of all peaks (a-, b-,
y-ions and losses). The ``TheoreticalSpectrumGenerator`` has many parameters
which have a detailed description located in the class documentation. For the
first spectrum, no b ions are added. Note how the ``add_metainfo`` parameter
in the second example populates the ``StringDataArray`` of the output
spectrum, allowing us to iterate over annotated ions and their masses.

