"""
--------------------------------------------------------------------------
                  OpenMS -- Open-Source Mass Spectrometry
--------------------------------------------------------------------------
Copyright The OpenMS Team -- Eberhard Karls University Tuebingen,
ETH Zurich, and Freie Universitaet Berlin 2002-2013.

This software is released under a three-clause BSD license:
 * Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
 * Neither the name of any author or any participating institution
   may be used to endorse or promote products derived from this software
   without specific prior written permission.
For a full list of authors, refer to the file AUTHORS.
--------------------------------------------------------------------------
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL ANY OF THE AUTHORS OR THE CONTRIBUTING
INSTITUTIONS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import re

import pyopenms


def convertToRichMSSpectrum(input_):
    rs = pyopenms.RichMSSpectrum()
    for p in input_:
        rp = pyopenms.RichPeak1D()
        rp.setMZ(p.getMZ())
        rp.setIntensity(p.getIntensity())
        rs.push_back(rp)
    return rs


def convertToMSSpectrum(input_):
    spectrum = pyopenms.MSSpectrum()
    for p in input_:
        rp = pyopenms.Peak1D()
        rp.setMZ(p.getMZ())
        rp.setIntensity(p.getIntensity())
        spectrum.push_back(rp)
    return spectrum


"""
Two phospho scorers, the interface is available through the "score" function:

- Input:
  - PeptideHit (pyopenms.PeptideHit)
  - Spectrum (pyopenms.MSSpectrum)
  - [Scorer massDelta]

- Output:
    [ Score, NewSequence ]
"""


class PhosphoScorerAScore:
    def score(self, phit, spectrum, massDelta=0.5):
        nr_sites = phit.getSequence().toString().count("Phospho")
        rs = convertToRichMSSpectrum(spectrum)
        newhit = pyopenms.AScore().compute(phit, rs, massDelta, nr_sites)
        return [newhit.getScore(), newhit.getSequence()]


class PhosphoScorerSimple:
    def score(self, phit, spectrum):
        nr_sites = phit.getSequence().toString().count("Phospho")
        if nr_sites != 1:
            return [-1, pyopenms.AASequence()]
        return self.simplisticBinnedScoring(phit, spectrum)

    def simplisticBinnedScoring(self, phit, spectrum):
        """Simplistic phospho-scoring of a spectrum against a peptide hit.

        This function enumerates all possible locations for the
        phosphorylation and computes a similarity score between the
        experimental spectrum and the theoretical spectrum for each
        possibility.
        """
        seq = phit.getSequence().toString()
        seq = seq.replace("(Phospho)", "")
        possibilities = []
        spectrum_b = self.binSpectrum(spectrum)
        charge = 1
        # Iterate over all possible phosphosites
        for m in re.finditer("[STY]", seq):
            new_sequence = \
                seq[: m.start() + 1] + "(Phospho)" + seq[m.start() - 1:]
            new_aaseq = pyopenms.AASequence(new_sequence)
            # Generate theoretical spectrum
            spectrum_generator = pyopenms.TheoreticalSpectrumGenerator()
            rs = pyopenms.RichMSSpectrum()
            try:
                spectrum_generator.addPeaks(
                    rs, new_aaseq, pyopenms.Residue.ResidueType.YIon, charge
                )
                spectrum_generator.addPeaks(
                    rs, new_aaseq, pyopenms.Residue.ResidueType.BIon, charge
                )
            except AttributeError:
                # 1.11
                spectrum_generator.addPeaks(
                    rs, new_aaseq, pyopenms.ResidueType.YIon, charge
                )
                spectrum_generator.addPeaks(
                    rs, new_aaseq, pyopenms.ResidueType.BIon, charge
                )
            theor = convertToMSSpectrum(rs)
            theor_b = self.binSpectrum(theor)
            # Compare theoretical spectrum to experimental spectrum
            comp_score = self.compare_binnedSpectra(spectrum_b, theor_b)
            possibilities.append([comp_score, new_aaseq])

        # Sort the result by score, return the best scoring result
        possibilities.sort(lambda x, y: -cmp(x[0], y[0]))
        return possibilities[0]

    def compare_binnedSpectra(self, sp1, sp2):
        """Compare two binned spectra, return a similarity score

        The two binned spectra should be created by a call to binSpectrum."""

        start = max(min(sp1.keys()), min(sp2.keys()))
        end = min(max(sp1.keys()), max(sp2.keys())) + 1

        # Normalize input
        import math

        magnitude1 = math.sqrt(sum([v * v for v in sp1.values()]))
        magnitude2 = math.sqrt(sum([v * v for v in sp2.values()]))

        sp1_norm = dict([(k, v / magnitude1) for k, v in sp1.iteritems()])
        sp2_norm = dict([(k, v / magnitude2) for k, v in sp2.iteritems()])

        # Compute similarity score
        score = 0
        for i in range(start, end):
            score += sp1_norm[i] * sp2_norm[i]
        return score

    def binSpectrum(self, sp):
        """Bin a spectrum into single, 1 m/z wide bins"""
        assert sp.isSorted()
        peaks = sp.get_peaks()
        mz = sp.get_peaks()[:, 0]
        bins = {}
        start = int(min(mz))
        end = int(max(mz)) + 1
        for i in range(start, end):
            bins[i] = sum([p[1] for p in peaks if int(p[0]) == i])
        return bins


if __name__ == "__main__":
    print
    "This file is intended as library and not as Python executable,"
    "please do not execute it directly."
