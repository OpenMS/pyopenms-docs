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
        print (iso)

As we can see, OpenMS knows common elements like Oxygen and Sulfur as well as
their isotopic distribution. These values are stored in ``Elements.xml`` in the
OpenMS share folder and can, in principle, be modified. The above code outputs
the isotopes of sulfur and their abundance:

.. code-block:: python

    (32, 0.9493)
    (33, 0.0076)
    (34, 0.0429)
    (36, 0.0002)


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
    wm = EmpiricalFormula(str(water) + str(methanol))
    print(wm)

    isotopes = wm.getIsotopeDistribution(3)
    for iso in isotopes.getContainer():
        print (iso)

.. Wait for pyOpenMS 2.4
.. isotopes = wm.getIsotopeDistribution( CoarseIsotopePatternGenerator(3) )
.. wm = water + methanol # only in pyOpenMS 2.4
.. ethanol = EmpiricalFormula(str("CH2") + str(methanol))
.. wm.getElementalComposition()

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
        >>> lys.getAverageWeight(Residue.ResidueType.Full)
        146.18788276708443
        >>> lys.getMonoWeight(Residue.ResidueType.Full)
        146.1055284466
        >>> lys.getPka()
        2.16


As we can see, OpenMS knows common amino acids like lysine as well as
some properties of them. These values are stored in ``Residues.xml`` in the
OpenMS share folder and can, in principle, be modified. 

Modifications
*************

An amino acid residue modification is represented in OpenMS by the class
``ResidueModification``. The known modifications are stored in the
``ModificationsDB`` object, which is capable of retrieving specific
modifications. It contains UniMod as well as PSI modifications.

.. code-block:: python

    from pyopenms import *
    ts = ResidueModification.TermSpecificity
    ox = ModificationsDB().getModification("Oxidation", "", ts.ANYWHERE)
    print(ox.getUniModAccession())
    print(ox.getUniModRecordId())
    print(ox.getDiffMonoMass())
    print(ox.getId())
    print(ox.getFullId())
    print(ox.getFullName())
    print(ox.getDiffFormula())
.. py24 : simply getModification

which outputs

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

    isotopes = ox.getDiffFormula().getIsotopeDistribution(5)
    for iso in isotopes.getContainer():
        print (iso)


In the next section, we will look at how to combine amino acids and
modifications to form amino acid sequences (peptides).
