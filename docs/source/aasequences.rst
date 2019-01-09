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

    print(seq.toString())
    print(concat.toString())
    print(suffix.toString())
    seq.getMonoWeight() # weight of M
    seq.getMonoWeight(Residue.ResidueType.Full, 2) # weight of M+2H
    mz = seq.getMonoWeight(Residue.ResidueType.Full, 2) / 2.0 # m/z of M+2H
    concat.getMonoWeight()
    
    print("Monoisotopic m/z of (M+2H)2+ is", mz)
    
Which will produce

.. code-block:: python

    DFPIANGER
    DFPIANGERDFPIANGER
    ANGER
    Monoisotopic m/z of (M+2H)2+ is 509.751258535

Molecular Formula
~~~~~~~~~~~~~~~~~

Note howe we can easily calculate the charged weight of a ``(M+2H)2+`` ion on line 11
and compute *m/z* on line 12 -- simply dividing by the charge.
We can now combine our knowledge of ``AASequence`` with what we learned above
about ``EmpiricalFormula`` to get accurate mass and isotope distributions from
the amino acid sequence:

.. code-block:: python
    :linenos:

    seq_formula = seq.getFormula()
    print("Peptide", seq.toString(), "has molecular formula", seq_formula.toString())
    print("="*35)

    isotopes = seq_formula.getIsotopeDistribution( CoarseIsotopePatternGenerator(6) )
    for iso in isotopes.getContainer():
            print ("Isotope", iso.getMZ(), ":", iso.getIntensity())

    suffix = seq.getSuffix(3) # y3 ion "GER"
    print("="*35)
    print("y3 ion :", suffix.toString())
    y3_formula = suffix.getFormula(Residue.ResidueType.YIon, 2) # y3++ ion
    suffix.getMonoWeight(Residue.ResidueType.YIon, 2) / 2.0 # CORRECT
    suffix.getMonoWeight(Residue.ResidueType.XIon, 2) / 2.0 # CORRECT
    suffix.getMonoWeight(Residue.ResidueType.BIon, 2) / 2.0 # INCORRECT

    print("y3 mz :", suffix.getMonoWeight(Residue.ResidueType.YIon, 2) / 2.0 )
    print(y3_formula.toString())
    print(seq_formula.toString())

Which will produce

.. code-block:: python

		Peptide DFPIANGER has molecular formula C44H67N13O15
		===================================
		Isotope 1017.48796414 : 0.568165123463
		Isotope 1018.49131898 : 0.305291324854
		Isotope 1019.49467381 : 0.0980210453272
		Isotope 1020.49802865 : 0.0232920628041
		Isotope 1021.50138349 : 0.00449259625748
		Isotope 1022.50473833 : 0.000737829308491
		===================================
		y3 ion : GER
		y3 mz : 181.09514385
		C13H24N6O6
		C44H67N13O15


Note on lines 13 to 15 we need to remember that we are dealing with an ion of
the x/y/z series since we used a suffix of the original peptide and using any
other ion type will produce a different mass-to-charge ratio (and while "GER"
would also be a valid "x3" ion, note that it *cannot* be a valid ion from the
a/b/c series and therefore the mass on line 15 cannot refer to the same input
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

        print(AASequence.fromString("DFPIAM(UniMod:35)GER").toString())
        print(AASequence.fromString("DFPIAM[+16]GER").toString())
        print(AASequence.fromString("DFPIAM[+15.99]GER").toString())
        print(AASequence.fromString("DFPIAM[147]GER").toString())
        print(AASequence.fromString("DFPIAM[147.035405]GER").toString())

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
approach may or may not.

N- and C-terminal modifications are represented by brackets to the right of the dots
terminating the sequence. For example, ``".(Dimethyl)DFPIAMGER."`` and
``".DFPIAMGER.(Label:18O(2))"`` represent the labelling of the N- and C-terminus
respectively, but ``".DFPIAMGER(Phospho)."`` will be interpreted as a
phosphorylation of the last arginine at its side chain:

.. code-block:: python

        from pyopenms import *
        s = AASequence.fromString(".(Dimethyl)DFPIAMGER.")
        print(s.toString(), s.hasNTerminalModification())
        s = AASequence.fromString(".DFPIAMGER.(Label:18O(2))")
        print(s.toString(), s.hasCTerminalModification())
        s = AASequence.fromString(".DFPIAMGER(Phospho).")
        print(s.toString(), s.hasCTerminalModification())

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
    peptide = AASequence.fromString("DFPIANGER")
    # standard behavior is adding b- and y-ions of charge 1
    p = Param()
    p.setValue(b"add_b_ions", b"false", b"Add peaks of b-ions to the spectrum")
    tsg.setParameters(p)
    tsg.getSpectrum(spec1, peptide, 1, 1)
    p.setValue(b"add_b_ions", b"true", b"Add peaks of a-ions to the spectrum")
    p.setValue(b"add_metainfo", b"true", "")
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

