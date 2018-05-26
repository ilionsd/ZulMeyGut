import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')
REPORTS_DIR = os.path.join(PROJECT_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

# The Way of the Voice
sys.path.append(PROJECT_DIR)

import numpy as np

from zulmeygut.subspack import model
from zulmeygut.subspack import time
from zulmeygut.subspack import script
from zulmeygut.utility.graphics.report import Report
from zulmeygut.utility import linereader
from zulmeygut.utility import blockreader


from helper import helper


if __name__ == '__main__':
    args = helper.arguments(sys.argv[1:], 'Subspack testing')
    audio, subtitles = args.audio, args.subtitles
    start, end = args.start, args.end

audio, subtitles = str(audio), str(subtitles)
start_cc, end_cc = time.incenties(start), time.incenties(end)


blocksize = 10000
channels, _, samplerate = blockreader.info(audio)
samplerate_cc = samplerate // 100
sample_0 = blockreader.align_floor(blocksize, samplerate_cc * start_cc)
sample_n = blockreader.align_ceil(blocksize, samplerate_cc * end_cc)
samples = sample_n - sample_0

signal = np.empty( (samples, channels), dtype=np.float64 )

reader = blockreader.BlockReader(audio, sample_0, sample_n, blocksize, 
                                 dtype='float64', zeropadding=False, retindex=True)
for block, index in reader:
    b, e = blocksize * index, blocksize * (index + 1)
    signal[b:e, ...] = block


events = script.FormattedSection(model.Section.EVENTS)
lines = linereader.read_all(subtitles)
events.load(lines)
