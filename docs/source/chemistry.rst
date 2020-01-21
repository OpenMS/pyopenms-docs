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
    for iso in isotopes.getContainer():
        print ("Oxygen isotope", iso.getMZ(), "has abundance", iso.getIntensity()*100, "%")

    sulfur = edb.getElement("S")
    sulfur.getName()
    sulfur.getSymbol()
    sulfur.getMonoWeight()
    isotopes = sulfur.getIsotopeDistribution()
    for iso in isotopes.getContainer():
        print ("Sulfur isotope", iso.getMZ(), "has abundance", iso.getIntensity()*100, "%")

As we can see, OpenMS knows common elements like Oxygen and Sulfur as well as
their isotopic distribution. These values are stored in ``Elements.xml`` in the
OpenMS share folder and can, in principle, be modified. The current values in
the file are average abundances found in nature. The above code outputs the
isotopes of oxygen and sulfur as well as their abundance:

.. code-block:: python

		Oxygen isotope 15.994915 has abundance 99.75699782371521 %
		Oxygen isotope 16.999132 has abundance 0.03800000122282654 %
		Oxygen isotope 17.999169 has abundance 0.20500000100582838 %

		Sulfur isotope 31.97207073 has abundance 94.92999911308289 %
		Sulfur isotope 32.971458 has abundance 0.7600000128149986 %
		Sulfur isotope 33.967867 has abundance 4.2899999767541885 %
		Sulfur isotope 35.967081 has abundance 0.019999999494757503 %



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
    ethanol = EmpiricalFormula("CH2") + methanol
    print("Ethanol chemical formula:", ethanol.toString())
    print("Ethanol composition:", ethanol.getElementalComposition())
    print("Ethanol has", ethanol.getElementalComposition()[b"H"], "hydrogen atoms")

which produces

.. code-block:: python

    Ethanol chemical formula: C2H6O1
    Ethanol composition: {b'C': 2, b'H': 6, b'O': 1}
    Ethanol has 6 hydrogen atoms


Note how in line 5 we were able to make a new molecule by adding existing
molecules (for example by adding two ``EmpiricalFormula`` objects). 

Isotopic Distributions
**********************

OpenMS can also generate theoretical isotopic distributions from analytes
represented as ``EmpiricalFormula``. Currently there are two algorithms
implemented, CoarseIsotopePatternGenerator which produces unit mass isotope
patterns and FineIsotopePatternGenerator which is based on the IsoSpec
algorithm [1]_ :

.. code-block:: python

    from pyopenms import *

    methanol = EmpiricalFormula("CH3OH")
    ethanol = EmpiricalFormula("CH2") + methanol

    print("Coarse Isotope Distribution:")
    isotopes = ethanol.getIsotopeDistribution( CoarseIsotopePatternGenerator(4) )
    prob_sum = sum([iso.getIntensity() for iso in isotopes.getContainer()])
    print("This covers", prob_sum, "probability")
    for iso in isotopes.getContainer():
        print ("Isotope", iso.getMZ(), "has abundance", iso.getIntensity()*100, "%")

    print("Fine Isotope Distribution:")
    isotopes = ethanol.getIsotopeDistribution( FineIsotopePatternGenerator(1e-3) )
    prob_sum = sum([iso.getIntensity() for iso in isotopes.getContainer()])
    print("This covers", prob_sum, "probability")
    for iso in isotopes.getContainer():
        print ("Isotope", iso.getMZ(), "has abundance", iso.getIntensity()*100, "%")

which produces

.. code-block:: python

    Coarse Isotope Distribution:
    This covers 0.9999999753596569 probability
    Isotope 46.0418651914 has abundance 97.56630063056946 %
    Isotope 47.045220029199996 has abundance 2.21499539911747 %
    Isotope 48.048574867 has abundance 0.2142168115824461 %
    Isotope 49.0519297048 has abundance 0.004488634294830263 %

    Fine Isotope Distribution:
    This covers 0.9994461630121805 probability
    Isotope 46.0418651914 has abundance 97.5662887096405 %
    Isotope 47.0452201914 has abundance 2.110501006245613 %
    Isotope 47.0481419395 has abundance 0.06732848123647273 %
    Isotope 48.046119191399995 has abundance 0.20049810409545898 %


The result calculated with the ``FineIsotopePatternGenerator``
contains the hyperfine isotope structure with heavy isotopes of Carbon and 
Hydrogen clearly distinguished while the coarse (unit resolution)
isotopic distribution contains summed probabilities for each isotopic peak
without the hyperfine resolution.  The hyperfine algorithm will for example
compute two peaks for the nominal mass of 47: one at 47.045 for the
incorporation of one heavy C13 with a delta mass of 1.003355 and one at 47.048
for the incorporation of one heavy deuterium with a delta mass of 1.006277.
These two peaks also have two different abundances (the heavy carbon one has
2.1% abundance and the deuterium one has 0.07% abundance). This makes sense
given that there are 2 carbon atoms and the natural abundance of C13 is about
1.1% and the molecule has six hydrogen atoms and the natural abundance of
deuterium is about 0.02%. The fine isotopic generator will not generate the
peak at nominal mass 49 since we specified our cutoff at 0.1% total abundance
and the four peaks above cover 99.9% of the
isotopic abundance.

We can also decrease our cutoff and ask for more isotopes to be calculated: 

.. code-block:: python

    from pyopenms import *

    methanol = EmpiricalFormula("CH3OH")
    ethanol = EmpiricalFormula("CH2") + methanol

    print("Fine Isotope Distribution:")
    isotopes = ethanol.getIsotopeDistribution( FineIsotopePatternGenerator(1e-6) )
    prob_sum = sum([iso.getIntensity() for iso in isotopes.getContainer()])
    print("This covers", prob_sum, "probability")
    for iso in isotopes.getContainer():
        print ("Isotope", iso.getMZ(), "has abundance", iso.getIntensity()*100, "%")

which produces

.. code-block:: python

  Fine Isotope Distribution:
  This covers 0.9999993089130612 probability
  Isotope 46.0418651914 has abundance 97.5662887096405 %
  Isotope 47.0452201914 has abundance 2.110501006245613 %
  Isotope 47.046082191400004 has abundance 0.03716550418175757 %
  Isotope 47.0481419395 has abundance 0.06732848123647273 %
  Isotope 48.046119191399995 has abundance 0.20049810409545898 %
  Isotope 48.0485751914 has abundance 0.011413302854634821 %
  Isotope 48.0494371914 has abundance 0.0008039440217544325 %
  Isotope 48.0514969395 has abundance 0.0014564131561201066 %
  Isotope 49.049474191399995 has abundance 0.004337066275184043 %
  Isotope 49.0523959395 has abundance 0.00013835959862262825 %

Here we can observe more peaks and now also see the heavy oxygen peak at
47.04608 with a delta mass of 1.004217 (difference between O16 and O17) at an
abundance of 0.04%, which is what we would expect for a single oxygen atom.
Even though the natural abundance of deuterium (0.02%) is lower than O17
(0.04%), since there are six hydrogen atoms in the molecule and only one
oxygen, it is more likely that we will see a deuterium peak than a heavy oxygen
peak. Also, even for a small molecule like ethanol, the differences in mass
between the hyperfine peaks can reach more than 110 ppm (48.046 vs 48.051).
Note that the FineIsotopePatternGenerator will generate peaks until the total
error has decreased to 1e-6, allowing us to cover 0.999999 of the probability.

OpenMS can also produce isotopic distribution with masses rounded to the
nearest integer:

.. code-block:: python

    isotopes = ethanol.getIsotopeDistribution( CoarseIsotopePatternGenerator(5, True) )
    for iso in isotopes.getContainer():
        print ("Isotope", iso.getMZ(), "has abundance", iso.getIntensity()*100, "%")

    Isotope 46.0 has abundance 97.56627082824707 %
    Isotope 47.0 has abundance 2.214994840323925 %
    Isotope 48.0 has abundance 0.214216741733253 %
    Isotope 49.0 has abundance 0.0044886332034366205 %
    Isotope 50.0 has abundance 2.64924580051229e-05 %


Amino Acid Residue
******************

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
    >>> lys.getFormula().toString()
    u'C6H14N2O2'

As we can see, OpenMS knows common amino acids like lysine as well as
some properties of them. These values are stored in ``Residues.xml`` in the
OpenMS share folder and can, in principle, be modified.

Amino Acid Modifications
************************

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

Which will print the isotopic pattern of the modification (Oxygen):

.. code-block:: python

  15.994915 : 0.9975699782371521
  16.998269837800002 : 0.0003800000122282654
  18.0016246756 : 0.002050000010058284


Ribonucleotide
***************

A ribonucleotide describes one of the building blocks of DNA and RNA. In
OpenMS, a ribonucleotide in its modified or unmodified form is represented by
the ``Ribonucleotide`` class in OpenMS.  The class is able to provide
information such as the isotope distribution of the residue, the average and
monoisotopic weight. The residues can be identified by their full name, their
three letter abbreviation or the single letter abbreviation. Modified
ribonucleotides are represented by the same class. Currently, support for RNA
is implemented.

.. code-block:: python

    >>> from pyopenms import *
    >>> uridine = RibonucleotideDB().getRibonucleotide(b"U")
    >>> uridine.getName()
    'uridine'
    >>> uridine.getCode()
    'U'
    >>> uridine.getAvgMass()
    244.2043
    >>> uridine.getMonoMass()
    244.0695
    >>> uridine.getFormula().toString()
    'C9H12N2O6'
    >>> uridine.isModified()
    False
    >>>
    >>> methyladenosine = RibonucleotideDB().getRibonucleotide(b"m1A")
    >>> methyladenosine.getName()
    '1-methyladenosine'
    >>> methyladenosine.isModified()
    True

.. We could also showcase the "get alternatives" method
.. for alt in RibonucleotideDB().getRibonucleotideAlternatives(b"mmA?"):  print(alt.getName())


.. [1] Łącki MK, Startek M, Valkenborg D, Gambin A.
    IsoSpec: Hyperfast Fine Structure Calculator.
    Anal Chem. 2017 Mar 21;89(6):3272-3277. `doi: 10.1021/acs.analchem.6b01459. <http://doi.org/10.1021/acs.analchem.6b01459>`_
