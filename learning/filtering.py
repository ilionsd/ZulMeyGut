import os
import sys

CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')
REPORTS_DIR = os.path.join(PROJECT_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

# The Way of the Voice
sys.path.append( PROJECT_DIR )


import soundfile as sf
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

blocksize = 10000
channels, _, samplerate = blockreader.info(audio)
samplerate_cc = samplerate // 100
sample_0 = blockreader.align_floor(blocksize, samplerate_cc * start_cc)
sample_n = blockreader.align_ceil (blocksize, samplerate_cc * end_cc  )
samples =  sample_n - sample_0

signal   = np.empty( (samples, channels), dtype=np.float64 )
filtered_band2 = np.empty( (samples, channels), dtype=np.float64 )
filtered_band5 = np.empty( (samples, channels), dtype=np.float64 )

band2 = ( 500, 1000)
band5 = (3000, 4000)
butterworth_order = 6

with sf.SoundFile(audio, mode='r') as file :
    print( 'Format: "{}", Subtype: "{}"'.format(file.format, file.subtype_info) )
    
reader_float64 = blockreader.BlockReader(audio, sample_0, sample_n, blocksize, 
                                 dtype='float64', zeropadding=False, retindex=True)
zf_band2, zf_band5 = None, None
for block, index in reader_float64 :
    b, e = blocksize * index, blocksize * (index + 1)
    signal[b:e, ...] = block
    filtered_band2[b:e, ...], zf_band2 = processing.butterworth_bandpass(block, samplerate, band2, 
                   butterworth_order, axis=0, zi=zf_band2)
    filtered_band5[b:e, ...], zf_band5 = processing.butterworth_bandpass(block, samplerate, band5, 
                   butterworth_order, axis=0, zi=zf_band5)
    
report = Report(FIGURES_DIR, helper.dataset(audio), start, end)

fig0 = report.linplot([signal.T[0], filtered_band2.T[0]], 
                      'Signal|Band2 channel 0')
fig1 = report.linplot([signal.T[1], filtered_band2.T[1]], 
                      'Signal|Band2 channel 1')
fig2 = report.linplot([signal.T[0], filtered_band5.T[0]], 
                      'Signal|Band5 channel 0')
fig3 = report.linplot([signal.T[1], filtered_band5.T[1]], 
                      'Signal|Band5 channel 1')



























 
