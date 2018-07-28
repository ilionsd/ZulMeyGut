# -*- coding: utf-8 -*-
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')
REPORTS_DIR = os.path.join(PROJECT_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

# The Way of the Voice
sys.path.append(PROJECT_DIR)


import numpy as np
from sklearn import mixture
from collections import Counter

from zulmeygut.voicepack import processing
from zulmeygut.voicepack import feature
from zulmeygut.subspack import time
from zulmeygut.subspack import script
from zulmeygut.utility.graphics.report import Report
from zulmeygut.utility.strides import rolling_window
from zulmeygut.utility.chainindex import ChainIndex
from zulmeygut.utility.samplereader import SampleReader
from zulmeygut.utility import blockreader

from helper import helper


if __name__ == '__main__':
    about = ('Voice recognition model '
            'based on MFCC extraction and Gaussian Mixture Models')
    args = helper.arguments(sys.argv[1:], about)
    audio, subtitles = args.audio, args.subtitles
    start, end = args.start, args.end

audio, subtitles = str(audio), str(subtitles)
start_cc, end_cc = time.tup_to_raw(start), time.tup_to_raw(end)

channels, _, samplerate = blockreader.info(audio)
samplerate_cc = samplerate // 100
Nfft = 1024
fpb = 300
blocksize = Nfft * fpb
sample_0 = blockreader.align_floor(blocksize, samplerate_cc * start_cc)
sample_n = blockreader.align_ceil (blocksize, samplerate_cc * end_cc  )
samples = sample_n - sample_0
frames = samples // Nfft
preemphasis_alpha = .97

mfcc_number = 36
freq_lower = 200
freq_upper = 8000

# Allocate features
features = dict()
# MFCC
features['MFCC'] = np.empty((mfcc_number, frames, channels), dtype=np.float64)
print('MFCC size:  ' + str(features['MFCC'].size ))
print('MFCC shape: ' + str(features['MFCC'].shape))

# Extract features
print('Extracting features')
reader = blockreader.BlockReader(audio, sample_0, sample_n, blocksize, 
                                 retindex=True, zeropadding=False)
zf = None
for data, index in reader:
    print('Processing block {} of {}'.format(index + 1, reader.size))
    b, e = fpb * index, fpb * (index + 1)
    data, zf = processing.preemphasis(data, alpha=preemphasis_alpha, axis=0, zi=zf, inplace=False)
    data = data.reshape((Nfft, -1, channels))
    data = processing.spectrum(data, axis=0, inplace=False)
    features['MFCC'][:, b:e, :] = feature.mfcc(data, mfcc_number, 
            freq_lower, freq_upper, samplerate, dc=False, axis=0)
print('Extraction completed')

report = Report(FIGURES_DIR, helper.dataset(audio), start, end)
fig0 = report.linmesh(features['MFCC'].T[0], 'MFCC channel 0')
fig1 = report.linmesh(features['MFCC'].T[1], 'MFCC channel 1')

# Training models
print('Training model')
n_components = 32
covariance_type = 'diag'
models = []
for idx in range(channels):
    model = mixture.GaussianMixture(n_components=n_components, covariance_type=covariance_type, max_iter=150)
    model.fit(features['MFCC'].T[idx, ...])
    models.append(model)
print('Training completed')

# Testing models
print('Testing model')
predictions = np.empty((0, channels, frames), dtype='int')
scores = []
for model_idx in range(channels):
    test = np.empty((0, frames), dtype='int')
    for test_idx in range(channels):
        prediction = model.predict(features['MFCC'].T[test_idx, ...])
        test = np.append(test, [prediction], axis=0)
    predictions = np.append(predictions, [test], axis=0)
    score = (test[np.arange(channels) != model_idx, :] != test[model_idx, :]).sum()
    scores.append(score)
print( 'Model score {} (lesser is better... probably)'.format(scores) )

# Filtering predictions
spoken_time_window = 0.1
spoken_frames_window = np.round(spoken_time_window * samplerate / Nfft).astype(type(Nfft))
print('Filtering predictions by most common label with window {}'.format(spoken_frames_window))

def most_common_label(ndarray):
    ndarray = np.asanyarray(ndarray)
    counter = Counter(np.ravel(ndarray))
    label_node = counter.most_common(n=1)[0]
    return label_node[0]

filtered_predictions = np.empty(predictions.shape, predictions.dtype)
for idx in np.ndindex((channels, channels)):
    rolling_prediction = rolling_window(predictions[idx], window=spoken_frames_window)
    pad = (spoken_frames_window - 1) // 2
    filtered_predictions[idx] = np.pad( np.apply_along_axis(most_common_label, axis=1, 
                        arr=rolling_prediction), (pad, spoken_frames_window - 1 - pad), 'edge')

filtered = (predictions != filtered_predictions).sum()
print('Filtered out {} labels'.format(filtered))

# Merging predictions
print('Merging predictions')
# ms time frame
time_frame = Nfft / samplerate
time_frame *= 1000
model_timing = []
for model_idx in np.ndindex((channels, channels)):
    timing = []
    prediction = filtered_predictions[model_idx]
    start = ChainIndex(prediction.shape)
    while start.is_valid:
        end = start.chain_next()
        while end.is_valid and prediction[start.index] == prediction[end.index]:
            end = end.chain_next()
        time_start = np.round(time_frame * start.index).astype(int)
        time_end = np.round(time_frame * end.index).astype(int)
        event = { 'label' : prediction[start.index], 'start' : time_start, 'end' : time_end }
        timing.append(event)
        start = end
    model_timing.append(timing)

#events = subtitles.extract_timing(SUBS_FILE)



























