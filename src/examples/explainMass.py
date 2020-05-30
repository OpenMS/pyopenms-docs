import pyopenms  # noqa F401
from pyopenms import *  # noqa F403
import sys

# Example for mass decomposition (mass explanation)
# Internal residue masses (as observed e.g. as mass shifts in tandem mass spectra)  # noqa E501
# are decomposed in possible amino acid strings that match in mass.

mass = float(sys.argv[1])  # provide mass as first command line parameter
residues = ResidueDB().getResidues(b"Natural19WithoutI")  # noqa F405

print("Trying to decompose " + str(mass) + " into sums of residues:")
for r in residues:
    print(
        r.getOneLetterCode().decode()
        + "\t"
        + str(r.getMonoWeight(Residue.ResidueType.Internal))  # noqa F405
    )

print("Mass explanations by fast algorithm:")
# fast algorithm based on integer mass decomposition
# returns a unique set of compositions (e.g.: only one of 'TSG' and 'GST' is reported)  # noqa E501
md_alg = MassDecompositionAlgorithm()  # noqa F405
param = md_alg.getParameters()
param.setValue("tolerance", 0.05)
param.setValue("residue_set", b"Natural19WithoutI")
md_alg.setParameters(param)
decomps = []
md_alg.getDecompositions(decomps, mass)
for d in decomps:
    print(d.toExpandedString().decode())

# for comparision:
# slow/naive algorithm to generate all decompositions (use only very small masses e.g. < 300 Da)  # noqa E501
# def recurse(mass_sum, peptide):
#  if abs(mass_sum - mass) < 0.05:
#    print(peptide + "\t" + str(mass_sum))
#  for r in residues:
#    new_mass = mass_sum + r.getMonoWeight(Residue.ResidueType.Internal)
#    if new_mass < mass + 0.05:
#      recurse(new_mass, peptide# + r.getOneLetterCode().decode())
#
# print("Mass explanations by naive algorithm:")
# recurse(0, "")
