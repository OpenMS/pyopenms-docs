Mass Decomposition
==================

Fragment mass to amino acid composition
***************************************

One challenge often encountered in mass spectrometry is the question of the
composition of a specific mass fragment only given its mass. For example, for
the internal fragment mass ``262.0953584466`` there are three different
interpretations within a narrow mass band of 0.05 Th:

.. code-block:: python

    >>> AASequence.fromString("MM").getMonoWeight(Residue.ResidueType.Internal, 0)
    262.08097003420005
    >>> AASequence.fromString("VY").getMonoWeight(Residue.ResidueType.Internal, 0)
    262.1317435742
    >>> AASequence.fromString("DF").getMonoWeight(Residue.ResidueType.Internal, 0)
    262.0953584466

As you can see, already for relatively simple two-amino acid combinations,
multiple explanations may exist. OpenMS provides an algorithm to compute all
potential amino acid combitions that explain a certain mass in the
``MassDecompositionAlgorithm`` class:

.. code-block:: python


    from pyopenms import *
    md_alg = MassDecompositionAlgorithm()
    param = md_alg.getParameters()
    param.setValue("tolerance", 0.05)
    param.setValue("residue_set", b"Natural19WithoutI")
    md_alg.setParameters(param)
    decomps = []
    md_alg.getDecompositions(decomps, 262.0953584466)
    for d in decomps:
      print(d.toExpandedString().decode()) 

Which outputs the three potential compositions for the mass ``262.0953584466``.
Note that every single combination of amino acids is only printed once, e.g.
only ``DF`` is reported while the isobaric ``FD`` is not reported. This makes
the algorithm more efficient.

Naive algorithm
***************

We can compare this result with a more naive algorithm which simply iterates
through all combinations of amino acid residues until the sum of of all
residues equals the target mass:

.. code-block:: python

    mass = 262.0953584466
    residues = ResidueDB().getResidues(b"Natural19WithoutI")
    def recursive_mass_decomposition(mass_sum, peptide):
      if abs(mass_sum - mass) < 0.05:
        print(peptide + "\t" + str(mass_sum))
      for r in residues:
        new_mass = mass_sum + r.getMonoWeight(Residue.ResidueType.Internal)
        if new_mass < mass + 0.05:
          recursive_mass_decomposition(new_mass, peptide + r.getOneLetterCode().decode())
      
    print("Mass explanations by naive algorithm:")
    recursive_mass_decomposition(0, "")

Note that this approach is substantially slower than the OpenMS algorithm and
also does not treat ``DF`` and ``FD`` as equivalent, instead outputting them
both as viable solutions.

Stand-alone Program
*******************

We can use pyOpenMS to write a short program that takes a mass and outputs all
possible amino acid combinations for that mass within a given tolerance:

.. code-block:: python
    :linenos:

    from pyopenms import *
    import sys

    # Example for mass decomposition (mass explanation)
    # Internal residue masses (as observed e.g. as mass shifts in tandem mass spectra)
    # are decomposed in possible amino acid strings that match in mass.

    mass = float(sys.argv[1])
    tol = float(sys.argv[2])

    md_alg = MassDecompositionAlgorithm()
    param = md_alg.getParameters()
    param.setValue("tolerance", tol)
    param.setValue("residue_set", b"Natural19WithoutI")
    md_alg.setParameters(param)
    decomps = []
    md_alg.getDecompositions(decomps, mass)
    for d in decomps:
      print(d.toExpandedString().decode()) 

If we copy the above code into a script, for example ``mass_decomposition.py``,
we will have a stand-alone software that takes two arguments: first the mass to
be de-composed and secondly the tolerance to be used (which are collected on
line 8 and 9). We can call it as follows:

.. code-block:: bash

    python mass_decomposition.py 999.4773990735001 1.0
    python mass_decomposition.py 999.4773990735001 0.001

Try to change the tolerance parameter. The parameter has a very large influence
on the reported results, for example for ``1.0`` tolerance, the algorithm will
produce 80 463 results while for a ``0.001`` tolerance, only 911 results are
expected.

Spectrum Tagger
**************

.. code-block:: python
    :linenos:

    from pyopenms import *

    tsg = TheoreticalSpectrumGenerator()
    param = tsg.getParameters()
    param.setValue("add_metainfo", "false")
    param.setValue("add_first_prefix_ion", "true")
    param.setValue("add_a_ions", "true")
    param.setValue("add_losses", "true")
    param.setValue("add_precursor_peaks", "true")
    tsg.setParameters(param)

    # spectrum with charges +1 and +2
    test_sequence = AASequence.fromString("PEPTIDETESTTHISTAGGER")
    spec = MSSpectrum()
    tsg.getSpectrum(spec, test_sequence, 1, 2)
    
    print(spec.size()) # should be 357

    # tagger searching only for charge +1
    tags = []
    tagger = Tagger(2, 10.0, 5, 1, 1, [], [])
    tagger.getTag(spec, tags)
    
    print(len(tags)) # should be 890

    b"EPTID" in tags  # True
    b"PTIDE" in tags  # True
    b"PTIDEF" in tags # False

