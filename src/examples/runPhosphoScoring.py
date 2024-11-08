###########################################################################
# Biological example of phosphopeptide-scoring
###########################################################################
from PhosphoScoring import PhosphoScorerSimple, PhosphoScorerAScore
import pyopenms
import csv

pepxml_file = "data/sample_xtandem_output.pep.xml"
mzml_file = "data/sample_spectra.mzML"
output = "sample_ascore_output.csv"
fh = open(output, "w")
writer = csv.writer(fh)

# Cutoff for filtering peptide hits by their score
cutoff_score = 0.75

#
# Data I/O : load the pep.xml file and the mzXML file
#
protein_ids = []
peptide_ids = []
pyopenms.PepXMLFile().load(pepxml_file, protein_ids, peptide_ids)
exp = pyopenms.MSExperiment()
pyopenms.FileHandler().loadExperiment(mzml_file, exp)


def compute_spectrum_bins(exp):
    rt_bins = {}
    for s in exp:
        if s.getMSLevel() == 1:
            continue
        tmp = rt_bins.get(int(s.getRT()), [])
        tmp.append(s)
        rt_bins[int(s.getRT())] = tmp
    return rt_bins


def mapPeptideIdsToSpectra(peptide_ids, exp, matching_mass_tol=1.0):
    rt_bins = compute_spectrum_bins(exp)
    hit_mapping = {}
    for i, pid in enumerate(peptide_ids):
        rt = pid.getMetaValue("RT")
        mz = pid.getMetaValue("MZ")
        # identify the corresponding spectrum from the correct RT bin
        corresponding_spectras = rt_bins[int(rt)]
        for corresponding_spectrum in corresponding_spectras:
            if (
                    abs(
                        corresponding_spectrum.getPrecursors()[0].getMZ() - mz
                        ) <
                    matching_mass_tol
            ):
                hit_mapping[i] = corresponding_spectrum
        if not hit_mapping.hasKey(i):
            print
            "Could not map hit at RT %s and MZ %s" % (rt, mz)
    return hit_mapping


#
# Filter the search results and create the mapping of search results to spectra
#
filtered_ids = [p for p in peptide_ids if p.getHits()[0].getScore() >
                cutoff_score]
# For teaching purposes, only ids betwen 1200 and 1600 s in RT are kept
# (also the spectra are filtered)
filtered_ids = [
    p
    for p in filtered_ids
    if p.getMetaValue("RT") > 1200 and p.getMetaValue("RT") < 1600
]
print
"==========================================================================="
print
"Filtered: kept %s ids below the cutoff score of %s out of %s" % (
    len(filtered_ids),
    cutoff_score,
    len(peptide_ids),
)
hit_mapping = mapPeptideIdsToSpectra(filtered_ids, exp)

#
# Iterate through all peptide hits, extract the corresponding spectra and hand
# it to a scoring function.
#

# Writer CSV header
print
"Will print the original, search-engine sequence," \
    " the AScore sequence and the PhosphoScorerSimple sequence"
writer.writerow(
    [
        "Search-Engine Score",
        "AScore",
        "AScore sequence",
        "Simple Scorer sequence",
        "Old Sequence",
        "# Sites",
    ]
)
for i in range(len(filtered_ids)):
    # Retrieve the input data:
    #  - the peptide hit from the search engine (we take the first hit here)
    #  - the corresponding spectrum
    phit = filtered_ids[i].getHits()[0]
    spectrum = hit_mapping[i]
    nr_sites = phit.getSequence().toString().count("Phospho")

    # Skip non-phospho hits
    if nr_sites == 0:
        continue

    ascore_result = PhosphoScorerAScore().score(phit, spectrum)
    simple_result = PhosphoScorerSimple().score(phit, spectrum)
    print
    "====", phit.getSequence().toString(), ascore_result[
        1
    ].toString(), simple_result[1].toString()

    # Store the resulting hit in our CSV file
    row = [
        phit.getScore(),
        ascore_result[0],
        ascore_result[1].toString(),
        simple_result[1].toString(),
        phit.getSequence().toString(),
        nr_sites,
    ]
    writer.writerow(row)

fh.close()
