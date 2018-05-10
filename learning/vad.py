import os
import sys

CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')
REPORTS_DIR = os.path.join(PROJECT_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

# The Way of the Voice
sys.path.append( PROJECT_DIR )


import numpy as np

from zulmeygut.voicepack import processing
from zulmeygut.voicepack import activity
from zulmeygut.subspack import time
from zulmeygut.utility.graphics.report import Report
from zulmeygut.utility import blockreader

from helper import helper


if __name__ == '__main__' :
    args = helper.arguments(sys.argv[1:], 'Voice Activity Detection learning')
    audio, subtitles = args.audio, args.subtitles
    start, end = args.start, args.end

audio, subtitles = str(audio), str(subtitles)
start_cc, end_cc = time.incenties(start), time.incenties(end)

Ntropy = 3
Nfft = 512
fpb = 300
blocksize = Nfft * fpb
channels, _, samplerate = blockreader.info(audio)
samplerate_cc = samplerate // 100
sample_0 = blockreader.align_floor(blocksize, samplerate_cc * start_cc)
sample_n = blockreader.align_ceil (blocksize, samplerate_cc * end_cc  )
samples =  sample_n - sample_0
frames = samples // Nfft

vad_envelope = np.empty( (frames, channels), dtype=np.float64 )
vad_variance = np.empty( (frames, channels), dtype=np.float64 )

for block, index in blockreader.BlockReader(audio, sample_0, sample_n, blocksize, retindex=True, zeropadding=False) :
    b, e = fpb * index, fpb * (index + 1) 
    block = block.reshape( (Nfft, -1, channels) )
    vad_envelope[b:e, ...] = activity.envelope_stat(block, samplerate, axis=0)
    spectre = processing.spectrogram(block, axis=0)
    vad_variance[b:e, ...] = activity.variance_stat(spectre, Ntropy, samplerate, axis=(1, 0))

fusion_alpha = 0.5
vad_fusion = fusion_alpha * vad_envelope + (1. - fusion_alpha) * vad_variance

print( vad_envelope.nonzero() )

formatter = event.TimeFormatter('SSA')
report = Report(FIGURES_DIR, helper.dataset(audio), formatter.format(start), formatter.format(end))

fig0 = report.linplot(vad_envelope.T[0], 'VAD envelope channel 0')
fig1 = report.linplot(vad_envelope.T[1], 'VAD envelope channel 1')

fig2 = report.linplot(vad_variance.T[0], 'VAD variance channel 0')
fig3 = report.linplot(vad_variance.T[1], 'VAD variance channel 1')

fig4 = report.linplot(vad_fusion.T[0], 'VAD fusion channel 0')
fig5 = report.linplot(vad_fusion.T[1], 'VAD fusion channel 1')



















    