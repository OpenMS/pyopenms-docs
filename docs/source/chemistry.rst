Chemistry
=========

Elements
********

OpenMS has representations for various chemical concepts including molecular
formulas, isotopes, amino sequences and modifications. First, we look at how
elements are stored in OpenMS:

.. code-block:: python

    from pyopenms import *

    edb = ElementDB()

    edb.hasElement("O")
    edb.hasElement("S")

    oxygen = edb.getElement("O")
    oxygen.getName()
    oxygen.getSymbol()
    oxygen.getMonoWeight()
    isotopes = oxygen.getIsotopeDistribution()

    sulfur = edb.getElement("S")
    sulfur.getName()
    sulfur.getSymbol()
    sulfur.getMonoWeight()
    isotopes = sulfur.getIsotopeDistribution()
    for iso in isotopes.getContainer():
        print (iso)

As we can see, OpenMS knows common elements like Oxygen and Sulfur as well as
their isotopic distribution. These values are stored in ``Elements.xml`` in the
OpenMS share folder and can, in principle, be modified.

Molecular Formula
*****************

Elements can be combined to molecular formulas (``EmpiricalFormula``) which can
be used to describe small molecules or peptides.  The class supports a large
number of operations like addition and subtraction. A simple example is given
in the next few lines of code.

.. code-block:: python

    from pyopenms import *

    methanol = EmpiricalFormula("CH3OH")
    water = EmpiricalFormula("H2O")
    wm = water + methanol
    print(wm)

    isotopes = wm.getIsotopeDistribution(3)
    for iso in isotopes.getContainer():
        print (iso)

which produces

.. code-block:: python

    C1H6O2
    (50, 0.9838702160434344)
    (51, 0.012069784261989644)
    (52, 0.004059999694575987)


AA Residue
**********

An amino acid residue is represented in OpenMS by the class ``Residue``. It provides a
container for the amino acids as well as some functionality. The class is able
to provide information such as the isotope distribution of the residue, the
average and monoisotopic weight. The residues can be identified by their full
name, their three letter abbreviation or the single letter abbreviation. The
residue can also be modified, which is implemented in the ``Modification`` class.
Additional less frequently used parameters of a residue like the gas-phase
basicity and pk values are also available.

.. code-block:: python

    >>> from pyopenms import *
    >>> lys = ResidueDB().getResidue("Lysine")
    >>> lys.getName()
    'Lysine'
    >>> lys.getThreeLetterCode()
    'LYS'
    >>> lys.getOneLetterCode()
    'K'
    >>> lys.getAverageWeight()
    146.18788276708443
    >>> lys.getMonoWeight()
    146.1055284466
    >>> lys.getPka()
    2.16


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

.. TODO


Modifications
************

The ``AASequence`` class can also handle modifications:

.. code-block:: python

    >>> from pyopenms import *
    >>> seq = AASequence.fromString("PEPTIDESEKUEM(Oxidation)CER", True)
    >>> print(seq.toString())
    PEPTIDESEKUEM(Oxidation)CER
    >>> print(seq.toUnmodifiedString())
    PEPTIDESEKUEMCER
    >>> print(seq.toBracketString())
    PEPTIDESEKUEM[147]CER
    >>> print(seq.toBracketString(False, []))
    PEPTIDESEKUEM[147.0354000171]CER
    >>> print(seq.toUniModString())
    PEPTIDESEKUEM(UniMod:35)CER

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

