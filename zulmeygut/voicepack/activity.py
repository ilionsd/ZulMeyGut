# -*- coding: utf-8 -*-

import numpy as np
from scipy import signal as dsp

from . import processing
from . import feature


def envelope_stat(signal, samplerate, axes=(0, -1), zi=(None, None)):
    '''
    Sub-band temporal envelope analysis
    '''
    band2 = ( 500, 1000)
    band5 = (3000, 4000)
    butterworth_order = 6
    if axes[0] == axes[1]:
        raise ValueError('Axes {} must be different'.format(axes))

    axis_time, axis_Nfft = axes
    zf2, zf5 = zi

    signal2 = np.empty(signal.shape, signal.dtype)
    signal5 = np.empty(signal.shape, signal.dtype)
    
    hamming_window = dsp.hamming(signal.shape[axis_Nfft])[:, np.newaxis]
    index = [slice(None)] * signal.ndim
    for k, in np.ndindex(signal.shape[axis_time]):
        index[axis_time] = k
        frame = signal[index] * hamming_window
        signal2[index], zf2 = processing.butterworth_bandpass(frame, samplerate, band2, zi=zf2, 
               order=butterworth_order, axis=axis_Nfft)
        signal5[index], zf5 = processing.butterworth_bandpass(frame, samplerate, band5, zi=zf5,
               order=butterworth_order, axis=axis_Nfft)

    envelope2 = feature.envelope(signal2, axis=axis_Nfft)
    envelope5 = feature.envelope(signal5, axis=axis_Nfft)
    q3_2 = np.percentile(envelope2, 75, axis=axis_Nfft)
    q1_2 = np.percentile(envelope2, 25, axis=axis_Nfft)
    iqr2 = q3_2 - q1_2
    mu2 = np.mean(envelope2, axis=axis_Nfft)
    mu5 = np.mean(envelope5, axis=axis_Nfft)
    stat = iqr2 - (mu2 - mu5)
    stat *= 2**15
    return np.piecewise(stat, [stat > 1.], [np.log10, 0]), (zf2, zf5)


def variance_stat(spectre, Ntropy, samplerate, axes=(0, -1)) :
    '''
    Sub-band long-term signal variability analysis
    '''
    spectre = np.asfarray(spectre)
    Nfft = spectre.shape[ axes[-1] ]
    
    step = samplerate // (Nfft - 1)
    band23 = (500, 2000)
    f_begin = np.ceil (band23[0] / step).astype(np.int)
    f_end   = np.floor(band23[1] / step).astype(np.int)
    
    spectre = np.swapaxes(spectre, axes[1], 0)
    spectre_band = np.swapaxes( spectre[f_begin : f_end + 1, ...], axes[1], 0 ) 
    entropy23 = feature.entropy(spectre_band, Ntropy, axis=axes[0])
    
    stat = np.var(entropy23, axis=axes[1], ddof=1)
    return np.log10(stat)

















