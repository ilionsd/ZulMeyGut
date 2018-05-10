# -*- coding: utf-8 -*-
import os
import sys

CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')
REPORTS_DIR = os.path.join(PROJECT_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

# The Way of the Voice
sys.path.append( PROJECT_DIR )


import numpy as np
from scipy import signal as dsp

from zulmeygut.voicepack import feature
from zulmeygut.subspack import event
from zulmeygut.utility.graphics.report import Report
from zulmeygut.utility import blockreader

from helper import helper


if __name__ == '__main__' :
    args = helper.arguments(sys.argv[1:], 'Envelope learning')
    audio, subtitles = args.audio, args.subtitles
    start, end = args.start, args.end

audio, subtitles = str(audio), str(subtitles)
audio, subtitles = os.path.abspath(audio), os.path.abspath(subtitles)
start_cc, end_cc = event.incenties(start), event.incenties(end)

Nfft = 512
fpb = 100
blocksize = Nfft * fpb
channels, _, samplerate = blockreader.info(audio)
samplerate_cc = samplerate // 100
sample_0 = blockreader.align_floor(blocksize, samplerate_cc * start_cc)
sample_n = blockreader.align_ceil (blocksize, samplerate_cc * end_cc  )
samples =  sample_n - sample_0
frames = samples // Nfft


signal = np.empty( (samples, channels), dtype=np.float64 )
envelope = np.empty( (samples, channels), dtype=np.float64 )

for block, index in blockreader.BlockReader(audio, sample_0, sample_n, blocksize, retindex=True, zeropadding=False) :
    b, e = blocksize * index, blocksize * (index + 1)
    signal[b:e, ...] = block
    envelope[b:e, ...] = feature.envelope(block, axis=0)

formatter = event.TimeFormatter('SSA')
report = Report(FIGURES_DIR, helper.dataset(audio), formatter.format(start), formatter.format(end))

fig0 = report.linplot([envelope.T[0], signal.T[0]], 'Envelope/Signal channel 0')
fig1 = report.linplot([envelope.T[1], signal.T[1]], 'Envelope/Signal channel 1')

    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 