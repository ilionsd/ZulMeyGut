# -*- coding: utf-8 -*-
import os
import sys
import time


CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')
DATA_DIR = os.path.join(PROJECT_DIR, 'data/raw')
DATASET_DIR = os.path.join(DATA_DIR, 'Hyperdimension Neptunia')
AUDIO_NAME = '[Commie] Hyperdimension Neptunia The Animation - 01 [BD 1080p FLAC] [AEA707BB]_Audio02.flac'
AUDIO_FILE = os.path.join(DATASET_DIR, AUDIO_NAME)
SUBS_NAME  = '[Commie] Hyperdimension Neptunia The Animation - 01 [BD 1080p FLAC] [AEA707BB]_Subtitles03.ass'
SUBS_FILE  = os.path.join(DATASET_DIR, SUBS_NAME)


# The Way of the Voice
sys.path.append( PROJECT_DIR )

import numpy as np
from sklearn import mixture
from collections import Counter

from zulmeygut.voicepack.samplereader import SampleReader
from zulmeygut.voicepack import processing
from zulmeygut.voicepack import feature
from zulmeygut.subspack import subtitles
from zulmeygut.utility.strides import rolling_window
from zulmeygut.utility.chainindex import ChainIndex
from zulmeygut.utility import graphics


Nfft = 1024
preemphasis_alpha = .97
block_duration = 3

Ntropy = 3
fusion_alpha = 0.5

features_number = 36
freq_lower = 200
freq_upper = 8000


# Allocate features
features = dict()

with SampleReader(AUDIO_FILE) as reader :
    samplerate = reader.file.samplerate
    channels = reader.file.channels

blockframes = np.round(block_duration * samplerate / Nfft).astype( type(Nfft) )
blocksize = Nfft * blockframes
with SampleReader(AUDIO_FILE, blocksize) as reader :
    blocks = reader.block_number()
    
blocks = 10
samples = blockframes * blocks

# MFCC
features['MFCC'] = np.empty( (features_number, samples, channels), dtype=np.float64 )
print( 'MFCC size:  ' + str(features['MFCC'].size ) )
print( 'MFCC shape: ' + str(features['MFCC'].shape) )

# VAD_envelope
features['VAD_envelope'] = np.empty( (samples, channels), dtype=np.float64 )
print( 'VAD_envelope size:  ' + str(features['VAD_envelope'].size ) )
print( 'VAD_envelope shape: ' + str(features['VAD_envelope'].shape) )

# VAD_variance
features['VAD_variance'] = np.empty( (samples, channels), dtype=np.float64 )
print( 'VAD_variance size:  ' + str(features['VAD_variance'].size ) )
print( 'VAD_variance shape: ' + str(features['VAD_variance'].shape) )


# Extract features
with SampleReader(AUDIO_FILE, blocksize) as reader :
    print( 'Extracting features' )
    T0_PERF, T0_PROC = time.perf_counter(), time.process_time()
    percentage = 0.1
    for idx in range( blocks ) :
        b = idx * blockframes
        e = (idx + 1) * blockframes
        if not idx / blocks < percentage :
            print( 'Feature extraction [{}; {}], {}/{}'
                   .format(b, e, idx + 1, blocks) )
            percentage += 0.1
        data = reader.block(idx)
        data = processing.preemphasis(data, alpha=preemphasis_alpha, axis=0, inplace=False)
        data = data.reshape( (Nfft, -1, channels) )
        #features['VAD_envelope'][b:e, :] = feature.vad_envelope(data, samplerate, axis=0)
        data = processing.spectrogram(data, axis=0, inplace=False)
        #features['VAD_variance'][b:e, :] = feature.vad_variance(data, Ntropy, samplerate, axis=(1, 0))
        features['MFCC'][:, b:e, :] = feature.mfcc(data, features_number, 
                                                    freq_lower, freq_upper, samplerate, dc=False, axis=0)
        
    # VAD_decision
    #features['VAD_decision'] = fusion_alpha * features['VAD_envelope'] + (1. - fusion_alpha) * np.log10( features['VAD_variance'] )

    TN_PERF, TN_PROC = time.perf_counter(), time.process_time()
    print( 'Extraction completed in {} perf time and {} proc time'.format(TN_PERF - T0_PERF, TN_PROC - T0_PROC) )

fig0 = graphics.linplot(features['MFCC'].T[0], 'MFCC Channel 0')
fig1 = graphics.linplot(features['MFCC'].T[1], 'MFCC Channel 1')

        
# Training models
print( 'Training models' )
T0_PERF, T0_PROC = time.perf_counter(), time.process_time()

n_components = 32
covariance_type = 'diag'
models = []
for idx in range(channels) :
    model = mixture.GaussianMixture(n_components=n_components, covariance_type=covariance_type, max_iter=150)
    model.fit(features['MFCC'].T[idx, ...])
    models.append(model)

TN_PERF, TN_PROC = time.perf_counter(), time.process_time()
print('Training completed in {} perf time and {} proc time'.format(TN_PERF - T0_PERF, TN_PROC - T0_PROC) )


# Testing models
print( 'Testing model' )
predictions = np.empty( (0, channels, samples), dtype='int' )
scores = []
for model_idx in range(channels) :
    test = np.empty( (0, samples), dtype='int')
    for test_idx in range(channels) :
        prediction = model.predict(features['MFCC'].T[test_idx, ...])
        test = np.append( test, [prediction], axis=0 )
    predictions = np.append(predictions, [test], axis=0 )
    
    score = (test[np.arange(channels) != model_idx, :] != test[model_idx, :]).sum()
    scores.append(score)

print( 'Model score {} (lesser is better... probably)'.format(scores) )


# Filtering predictions
spoken_time_window = 0.1
spoken_frames_window = np.round(spoken_time_window * samplerate / Nfft).astype( type(Nfft) )
print( 'Filtering predictions by most common label with window {}'.format(spoken_frames_window) )

def most_common_label(ndarray) :
    ndarray = np.asanyarray(ndarray)
    counter = Counter( np.ravel(ndarray) )
    label_node = counter.most_common(n=1)[0]
    return label_node[0]

filtered_predictions = np.empty( predictions.shape, predictions.dtype ) 
for idx in np.ndindex( (channels, channels) ) :
    rolling_prediction = rolling_window(predictions[idx], window=spoken_frames_window)
    pad = (spoken_frames_window - 1) // 2
    filtered_predictions[idx] = np.pad( np.apply_along_axis(most_common_label, axis=1, 
                        arr=rolling_prediction), (pad, spoken_frames_window - 1 - pad), 'edge')
    
filtered = (predictions != filtered_predictions).sum()
print( 'Filtered out {} labels'.format(filtered) )


# Merging predictions
print( 'Merging predictions' )
# ms time frame
time_frame = Nfft / samplerate
time_frame *= 1000 # ms
model_timing = []
for model_idx in np.ndindex( (channels, channels) ) :
    timing = []
    prediction = filtered_predictions[model_idx]
    start = ChainIndex(prediction.shape)
    while start.is_valid :
        end = start.chain_next()
        while end.is_valid and prediction[start.index] == prediction[end.index] :
            end = end.chain_next()
            
        time_start = np.round(time_frame * start.index).astype(int)
        time_end = np.round(time_frame * end.index).astype(int)
        event = { 'label' : prediction[start.index], 'start' : time_start, 'end' : time_end }
        timing.append( event )
        start = end
    model_timing.append(timing)
    

events = subtitles.extract_timing(SUBS_FILE)   
        


























