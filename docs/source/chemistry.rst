Chemistry
=========

Elements
********

OpenMS has representations for various chemical concepts including molecular
formulas, isotopes, amino acid sequences and modifications. First, we look at how
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
        print (iso.getMZ(), ":", iso.getIntensity())

As we can see, OpenMS knows common elements like Oxygen and Sulfur as well as
their isotopic distribution. These values are stored in ``Elements.xml`` in the
OpenMS share folder and can, in principle, be modified. The above code outputs
the isotopes of sulfur and their abundance:

.. code-block:: python

  31.97207073 : 0.949299991131
  32.971458 : 0.00760000012815
  33.967867 : 0.0428999997675
  35.967081 : 0.000199999994948


Molecular Formula
*****************

Elements can be combined to molecular formulas (``EmpiricalFormula``) which can
be used to describe small molecules or peptides.  The class supports a large
number of operations like addition and subtraction. A simple example is given
in the next few lines of code.

.. code-block:: python
    :linenos:

    from pyopenms import *

    methanol = EmpiricalFormula("CH3OH")
    water = EmpiricalFormula("H2O")
    ethanol = EmpiricalFormula(str("CH2") + str(methanol))
    wm = water + methanol
    print(wm)
    print(wm.getElementalComposition())

    isotopes = wm.getIsotopeDistribution( CoarseIsotopePatternGenerator(3) )
    for iso in isotopes.getContainer():
        print (iso.getMZ(), ":", iso.getIntensity())

which produces

.. code-block:: python

    C1H6O2
    {'H': 6, 'C': 1, 'O': 2}
    50.0367801914 : 0.983870208263
    51.0401350292 : 0.0120697841048
    52.043489867 : 0.00405999971554

Note how in lines 5 and 6 we were able to make new molecules by adding existing
molecules (either  by adding two ``EmpiricalFormula`` objects or by adding
simple strings). Also, we are able to produce rounded masses if we prefer:

.. code-block:: python

    isotopes = wm.getIsotopeDistribution( CoarseIsotopePatternGenerator(3, True) )
    for iso in isotopes.getContainer():
        print (iso.getMZ(), ":", iso.getIntensity())

    50.0 : 0.983870208263
    51.0 : 0.0120697841048
    52.0 : 0.00405999971554


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

As we can see, OpenMS knows common amino acids like lysine as well as
some properties of them. These values are stored in ``Residues.xml`` in the
OpenMS share folder and can, in principle, be modified. 


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
*************

An amino acid residue modification is represented in OpenMS by the class
``ResidueModification``. The known modifications are stored in the
``ModificationsDB`` object, which is capable of retrieving specific
modifications. It contains UniMod as well as PSI modifications.

.. code-block:: python

    from pyopenms import *
    ox = ModificationsDB().getModification("Oxidation")
    print(ox.getUniModAccession())
    print(ox.getUniModRecordId())
    print(ox.getDiffMonoMass())
    print(ox.getId())
    print(ox.getFullId())
    print(ox.getFullName())
    print(ox.getDiffFormula())

.. code-block:: python

    UniMod:35
    35
    15.994915
    Oxidation
    Oxidation (N)
    Oxidation or Hydroxylation
    O1

thus providing information about the "Oxidation" modification. As above, we can
investigate the isotopic distribution of the modification (which in this case
is identical to the one of Oxygen by itself):

.. code-block:: python

    isotopes = ox.getDiffFormula().getIsotopeDistribution(CoarseIsotopePatternGenerator(5))
    for iso in isotopes.getContainer():
        print (iso.getMZ(), ":", iso.getIntensity())

In the next section, we will look at how to combine amino acids and
modifications to form amino acid sequences (peptides).

