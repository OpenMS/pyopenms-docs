from pyopenms import *

# Initialize Experiment
exp = MSExperiment()

# Load file into experiment container
MzMLFile().load("../data/YIC(Carbamidomethyl)DNQDTISSK.mzML", exp)

# Get first spectrum
spectra = exp.getSpectra()
spectrum = exp[0]

# Generate theoretical spectrum
tsg = TheoreticalSpectrumGenerator()
theo_spectrum = MSSpectrum()
p = tsg.getParameters()
p.setValue(b"add_b_ions", b"true", b"Add peaks of b-ions to the spectrum")
p.setValue(b"add_metainfo", b"true", "")
tsg.setParameters(p)
tsg.getSpectrum(
    theo_spectrum, AASequence.fromString("YIC(Carbamidomethyl)DNQDTISSK"), 1, 2
)

# Compute PSM
alignment = []
spa = SpectrumAlignment()
p = spa.getParameters()
p.setValue(b"tolerance", 0.5)
p.setValue(b"is_relative_tolerance", b"false")  # 0.5 Da tolerance
spa.setParameters(p)
spa.getSpectrumAlignment(alignment, theo_spectrum, spectrum)

# Print matching ions and mz from theoretical spectrum
print("Matched peaks: " + str(len(alignment)))
print("ion\ttheo. m/z\tobserved m/z")

for theo_idx, obs_idx in alignment:
    print(
        theo_spectrum.getStringDataArrays()[0][theo_idx].decode()
        + "\t"
        + str(theo_spectrum[theo_idx].getMZ())
        + "\t"
        + str(spectrum[obs_idx].getMZ())
    )

# Matched peaks: 16
# ion     theo. m/z       observed m/z
# y2+     234.14483407287105      234.12303161621094
# y5++    268.15794163667096      268.1054382324219
# b2+     277.154670104771        277.24560546875
# y3+     321.17686323237103      321.2969970703125
# y4+     434.26092758327104      434.2879638671875
# b3+     437.185319089971        437.291259765625
# y5+     535.308606806571        535.18896484375
# b4+     552.212263249471        552.3375244140625
# b9++    562.239866948271        562.4213256835938
# y10++   584.2509635120709       584.4120483398438
# y11++   640.7929956875209       640.9539184570312
# b11++   649.2718961077711       649.0973510742188
# y6+     650.335550966071        650.3652954101562
# b5+     666.255191440871        666.1763305664062
# y7+     778.394129221271        778.3391723632812
# b6+     794.3137696960711       794.192138671875
