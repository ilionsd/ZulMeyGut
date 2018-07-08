import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')
REPORTS_DIR = os.path.join(PROJECT_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

# The Way of the Voice
sys.path.append(PROJECT_DIR)


import numpy as np

from zulmeygut.voicepack import processing
from zulmeygut.voicepack import activity
from zulmeygut.subspack import time
from zulmeygut.subspack import script
from zulmeygut.utility.graphics.report import Report
from zulmeygut.utility import linereader
from zulmeygut.utility import blockreader

from helper import helper


if __name__ == '__main__':
    about = ('Voice Activity Detection in Noisy Environments Based on'
            'Double-Combined Fourier Transform and Line Fitting')
    args = helper.arguments(sys.argv[1:], about)
    audio, subtitles = args.audio, args.subtitles
    start, end = args.start, args.end

audio, subtitles = str(audio), str(subtitles)
start_cc, end_cc = time.tup_to_raw(start), time.tup_to_raw(end)

channels, _, samplerate = blockreader.info(audio)
samplerate_cc = samplerate // 100
Ntropy = 3
Nfft = samplerate_cc
fpb = 300
blocksize = Nfft * fpb
sample_0 = blockreader.align_floor(blocksize, samplerate_cc * start_cc)
sample_n = blockreader.align_ceil (blocksize, samplerate_cc * end_cc  )
samples = sample_n - sample_0
frames = samples // Nfft

second_spectrogram = np.empty((Nfft, frames, channels), dtype=np.float64)
speech = np.full(frames, False, dtype=np.bool)

reader = blockreader.BlockReader(audio, sample_0, sample_n, blocksize, retindex=True, zeropadding=False)
for block, index in reader:
    b, e = fpb * index, fpb * (index + 1)
    block = block.reshape((Nfft, -1, channels))
    second_spectrogram[:, b:e, :] = processing.spectrum(block, axis=0, ret=(False, True))


lines = linereader.read_all(subtitles)
df_all = script.load_dataframe(lines, section='[Events]')
df_speech = df_all[(df_all.Style == 'Default') | (df_all.Style == 'Alternate')]
for _, subtitle in df_speech.iterrows():
    b, e = subtitle['Start'], subtitle['End']
    if b < start_cc:
        b = start_cc
    if e > end_cc:
        e = end_cc
    speech[b - start_cc:e - start_cc] = True

report = Report(FIGURES_DIR, helper.dataset(audio), start, end)

fig0 = report.linmesh(second_spectrogram.T[0], 'Second spectrogram0')
fig1 = report.linmesh(second_spectrogram.T[1], 'Second spectrogram1')
