Oligonucleotides: RNA
=====================

Nucleic Acid Sequences
**********************

OpenMS also supports the representation of RNA oligonucleotides using the
``NASequence`` class:

.. code-block:: python
    :linenos:

    from pyopenms import *
    oligo = NASequence.fromString("AAUGCAAUGG")
    prefix = oligo.getPrefix(4)
    suffix = oligo.getSuffix(4)

    print(oligo)
    print(prefix)
    print(suffix)
    print()

    print("Oligo length", oligo.size())
    print("Total precursor mass", oligo.getMonoWeight())
    print("y1+ ion mass of", str(prefix), ":", prefix.getMonoWeight(NASequence.NASFragmentType.YIon, 1))
    print()

    seq_formula = oligo.getFormula()
    print("RNA Oligo", oligo, "has molecular formula", seq_formula)
    print("="*35)
    print()

    isotopes = seq_formula.getIsotopeDistribution( CoarseIsotopePatternGenerator(6) )
    for iso in isotopes.getContainer():
      print ("Isotope", iso.getMZ(), ":", iso.getIntensity())


Which will output

.. code-block:: python


    AAUGCAAUGG
    AAUG
    AUGG

    Oligo length 10
    Total precursor mass 3206.4885302061
    y1+ ion mass of AAUG : 1248.2298440331

    RNA Oligo AAUGCAAUGG has molecular formula C97H119N42O66P9
    ===================================

    Isotope 3206.4885302061 : 0.25567981600761414
    Isotope 3207.4918850439003 : 0.31783154606819153
    Isotope 3208.4952398817004 : 0.23069815337657928
    Isotope 3209.4985947195 : 0.12306403368711472
    Isotope 3210.5019495573 : 0.053163252770900726
    Isotope 3211.5053043951 : 0.01956319250166416



The ``NASequence`` object also allows iterations directly in Python:

.. code-block:: python
    :linenos:

    from pyopenms import *
    oligo = NASequence.fromString("AAUGCAAUGG")
    print("The oligonucleotide", str(oligo), "consists of the following nucleotides:")
    for ribo in oligo:
      print(ribo.getName())

Fragment ions
~~~~~~~~~~~~~

Similarly to before for amino acid sequences, we can also generate internal fragment ions:

.. code-block:: python
    :linenos:

    from pyopenms import *
    oligo = NASequence.fromString("AAUGCAAUGG")
    suffix = oligo.getSuffix(4)

    oligo.size()
    oligo.getMonoWeight()

    charge = 2
    mass = suffix.getMonoWeight(NASequence.NASFragmentType.WIon, charge)
    w4_formula = suffix.getFormula(NASequence.NASFragmentType.WIon, charge)
    mz = mass / charge

    print("="*35)
    print("RNA Oligo w4++ ion", suffix, "has mz", mz)
    print("RNA Oligo w4++ ion", suffix, "has molecular formula", w4_formula)

Modified oligonucleotides
*************************

Modified nucleotides can also represented by the ``Ribonucleotide`` class and
are specified using a unique string identifier present in the
``RibonucleotideDB`` in square brackets. For example, ``[m1A]`` represents
1-methyladenosine. We can create a ``NASequence`` object by parsing a modified
sequence as follows:

.. code-block:: python
    :linenos:

    from pyopenms import *
    oligo_mod = NASequence.fromString("A[m1A][Gm]A")
    seq_formula = oligo_mod.getFormula()
    print("RNA Oligo", oligo_mod, "has molecular formula", 
      seq_formula, "and length", oligo_mod.size())
    print("="*35)

    oligo_list = [oligo_mod[i].getOrigin() for i in range(oligo_mod.size())]
    print("RNA Oligo", oligo_mod.toString(), "has unmodified sequence", "".join(oligo_list))

    r = oligo_mod[1]
    r.getName()
    r.getHTMLCode()
    r.getOrigin()

    for i in range(oligo_mod.size()):
      print (oligo_mod[i].isModified())


DNA, RNA and Protein
********************

We can also work with DNA and RNA sequences in combination with the BioPython
library (you can install BioPython with ``pip install biopython``):

.. code-block:: python
    :linenos:

    from pyopenms import *
    from Bio.Seq import Seq
    from Bio.Alphabet import IUPAC
    bsa = FASTAEntry()
    bsa.sequence = 'ATGAAGTGGGTGACTTTTATTTCTCTTCTCCTTCTCTTCAGCTCTGCTTATTCCAGGGGTGTGTTTCGT'
    bsa.description = "BSA Bovine Albumin (partial sequence)"
    bsa.identifier = "BSA"

    entries = [bsa]

    f = FASTAFile()
    f.store("example_dna.fasta", entries)

    coding_dna = Seq(bsa.sequence, IUPAC.unambiguous_dna)    
    coding_rna = coding_dna.transcribe()
    protein_seq = coding_rna.translate()

    oligo = NASequence.fromString(str(coding_rna))
    aaseq = AASequence.fromString(str(protein_seq))

    print("The RNA sequence", str(oligo), "has mass", oligo.getMonoWeight(), "and \n"
      "translates to the protein sequence", str(aaseq), "which has mass", aaseq.getMonoWeight() )

.. image:: ./img/launch_binder.jpg
   :target: https://mybinder.org/v2/gh/OpenMS/pyopenms-extra/master+ipynb?urlpath=lab/tree/docs/source/nasequences.ipynb
   :alt: Launch Binder