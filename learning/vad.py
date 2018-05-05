import os
import sys

CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')

# The Way of the Voice
sys.path.append( PROJECT_DIR )


import numpy as np

from zulmeygut.voicepack import processing
from zulmeygut.voicepack import activity
from zulmeygut.subspack import event
from zulmeygut.utility.graphics import plot
from zulmeygut.utility import blockreader

from helper.arguments import arguments


if __name__ == '__main__' :
    audio, subtitles, start, end = arguments(sys.argv[1:], 'Voice Activity Detection learning')
    
audio, subtitles = str(audio), str(subtitles)
start, end = event.incenties(start), event.incenties(end)

Ntropy = 3
Nfft = 1024
fpb = 100
blocksize = Nfft * fpb
channels, _, samplerate = blockreader.info(audio)
samplerate_cc = samplerate // 100
sample_0 = blockreader.align_floor(blocksize, samplerate_cc * start) 
sample_n = blockreader.align_ceil (blocksize, samplerate_cc * end  )
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
vad_fusion = fusion_alpha * vad_envelope + (1. - fusion_alpha) * np.log10(vad_variance)

print( vad_envelope.nonzero() )
fig0 = plot.linplot(vad_envelope.T[0], 'VAD envelope channel 0')
fig1 = plot.linplot(vad_envelope.T[1], 'VAD envelope channel 1')

fig2 = plot.linplot(vad_fusion.T[0], 'VAD fusion channel 0')
fig3 = plot.linplot(vad_fusion.T[1], 'VAD fusion channel 1')




















    