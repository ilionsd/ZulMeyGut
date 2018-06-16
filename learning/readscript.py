import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')
REPORTS_DIR = os.path.join(PROJECT_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

# The Way of the Voice
sys.path.append(PROJECT_DIR)

import numpy as np
import pandas as pd

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
start_cc, end_cc = time.tup_to_raw(start), time.tup_to_raw(end)


blocksize = 10000
channels, _, samplerate = blockreader.info(audio)
samplerate_cc = samplerate // 100
sample_0 = blockreader.align_floor(blocksize, samplerate_cc * start_cc)
sample_n = blockreader.align_ceil(blocksize, samplerate_cc * end_cc)
samples = sample_n - sample_0

signal = np.empty((samples, channels), dtype=np.float64)
speech = np.full(end_cc - start_cc, False, dtype=np.bool)

reader = blockreader.BlockReader(audio, sample_0, sample_n, blocksize, 
                                 dtype='float64', zeropadding=False, retindex=True)
for block, index in reader:
    b, e = blocksize * index, blocksize * (index + 1)
    signal[b:e, ...] = block


lines = linereader.read_all(subtitles)
fields, events, length = script.load_formatted(lines, section='[Events]')
events['Start'] = [time.tup_to_raw(time.parse_ssa(t)) for t in events['Start']]
events['End'] = [time.tup_to_raw(time.parse_ssa(t)) for t in events['End']]
print(fields)
df_all = pd.DataFrame(events)
df_speech = df_all[(df_all.Style == 'Default') | (df_all.Style == 'Alternate')]

for _, subtitle in df_speech.iterrows():
    b, e = subtitle['Start'], subtitle['End']
    if b < start_cc:
        b = start_cc
    if e > end_cc:
        e = end_cc
    speech[b - start_cc:e - start_cc] = True
speech = np.repeat(speech, samplerate_cc)

report = Report(FIGURES_DIR, helper.dataset(audio), start, end)

fig0 = report.linplot([signal.T[0], speech], 'Signal channel 0 | Speech')
fig1 = report.linplot([signal.T[1], speech], 'Signal channel 1 | Speech')
