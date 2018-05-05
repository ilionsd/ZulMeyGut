# -*- coding: utf-8 -*-
import os
import sys

CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')

# The Way of the Voice
sys.path.append( PROJECT_DIR )


import numpy as np
from scipy import signal as dsp

from zulmeygut.voicepack import feature
from zulmeygut.subspack import event
from zulmeygut.utility.graphics import plot
from zulmeygut.utility import blockreader

from helper.arguments import arguments


if __name__ == '__main__' :
    audio, subtitles, start, end = arguments(sys.argv[1:])

audio, subtitles = str(audio), str(subtitles)
start, end = event.incenties(start), event.incenties(end)

Nfft = 512
fpb = 100
blocksize = Nfft * fpb
channels, _, samplerate = blockreader.info(audio)
samplerate_cc = samplerate // 100
sample_0 = blockreader.align_floor(blocksize, samplerate_cc * start)
sample_n = blockreader.align_ceil (blocksize, samplerate_cc * end  )
samples =  sample_n - sample_0
frames = samples // Nfft

envelope = np.empty( (samples, channels), dtype=np.float64 )
vad_envelope = np.empty( (frames, channels), dtype=np.float64 )

for block, index in blockreader.BlockReader(audio, sample_0, sample_n, blocksize, retindex=True, zeropadding=False) :
    b, e = blocksize * index, blocksize * (index + 1)
    envelope[b:e, ...] = feature.envelope(block, axis=0)
    
    
    
fig0 = plot.linplot(envelope.T[0], 'Envelope Channel 0')
fig1 = plot.linplot(envelope.T[1], 'Envelope Channel 1')
    

    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 