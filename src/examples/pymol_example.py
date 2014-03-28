# Example of displaying a Streptococcal protein and showing peptide coverage
import pymol
import pyopenms
print("Starting pymol")
pymol.finish_launching()
pepxml_file = "data/4D8B.pepXML"

def get_peptides_protein_seq():

    # Read in PepXML
    protein_ids = []
    peptide_ids = []
    pyopenms.PepXMLFile().load(pepxml_file, protein_ids, peptide_ids)
    peptides = [pid.getHits()[0].getSequence().toString() for pid in peptide_ids]

    # Sequence could be from FASTA file (or just provided here)
    sequence = "".join("""
    MNKKKLGIRLLSLLALGGFVLANPVFADQNFARNEKEAKDSAITFIQKSAAIKAGARSAE
    DIKLDKVNLGGELSGSNMYVYNISTGGFVIVSGDKRSPEILGYSTSGSFDANGKENIASF
    MESYVEQIKENKKLDTTYAGTAEIKQPVVKSLLNSKGIHYNQGNPYNLLTPVIEKVKPGE
    QSFVGQHAATGCVATATAQIMKYHNYPNKGLKDYTYTLSSNNPYFNHPKNLFAAISTRQY
    NWNNILPTYSGRESNVQKMAISELMADVGISVDMDYGPSSGSAGSSRVQRALKENFGYNQ
    SVHQINRSDFSKQDWEAQIDKELSQNQPVYYQGVGKVGGHAFVIDGADGRNFYHVNWGWG
    GVSDGFFRLDALNPSALGTGGGAGGFNGYQSAVVGIKP
    """.split())
    return peptides, sequence

print("Plotting Protein 4D8B")
pymol.cmd.window("show")
pymol.cmd.fetch("4D8B")
pymol.cmd.hide("everything")
pymol.cmd.show("cartoon")

peptides, protein_sequence = get_peptides_protein_seq()
# select which residues to color (set of peptides, on protein sequence)
res_str = ""
for peptide in peptides:
    found_at = protein_sequence.find(peptide)
    res_str += " res %s-%s" % (found_at, found_at + len(peptide))

print("Superimposing MS-identified peptides .. please wait")
pymol.cmd.color("bluewhite")
pymol.cmd.bg_color("white")
pymol.cmd.color("wheat", res_str)

# Do raytracing 
pymol.cmd.set("orthoscopic")
pymol.cmd.set("ray_trace_mode", 1)
pymol.cmd.ray(1920,1440)

print("Printing output image")
pymol.cmd.png("4D8B_coverage_white_5_ray_ortho_mode1.png", dpi=600)

