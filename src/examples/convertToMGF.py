###########################################################################
## Example script to convert any file to MGF
###########################################################################

# Read input
import pyopenms, sys
if len(sys.argv) <= 2:
    print "Usage: convertToMGF.py inputfile outputfile"
    sys.exit()

msdata = pyopenms.MSExperiment()
pyopenms.FileHandler().loadExperiment(sys.argv[1], msdata)
outfile = open(sys.argv[2], "w")

# Create header
outfile.write("COM=Testfile\n")
outfile.write("ITOL=1\n")
outfile.write("ITOLU=Da\n")
outfile.write("CLE=Trypsin\n")
outfile.write("CHARGE=1,2,3\n")

# Iterate through all spectra, skip all MS1 spectra and then write mgf format
nr_ms2_spectra = 0
for spectrum in msdata:
    if spectrum.getMSLevel() == 1:
        continue
    nr_ms2_spectra += 1
    outfile.write("\nBEGIN IONS\n")
    outfile.write("TITLE=%s\n" % spectrum.getNativeID())
    outfile.write("RTINSECONDS=%s\n" % spectrum.getRT())
    try:
        outfile.write("PEPMASS=%s\n" % spectrum.getPrecursors()[0].getMZ())
        ch = spectrum.getPrecursors()[0].getCharge()
        if ch > 0:
            outfile.write("CHARGE=%s\n" % ch)
    except IndexError:
        outfile.write("PEPMASS=unknown\n")
    for peak in spectrum:
        outfile.write("%s %s\n" % (peak.getMZ(), peak.getIntensity() ))
    outfile.write("END IONS\n")

if nr_ms2_spectra == 0:
    print("Did not find any MS2 spectra in your input, thus the output file is empty!")

