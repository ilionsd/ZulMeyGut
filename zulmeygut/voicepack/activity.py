# -*- coding: utf-8 -*-

import numpy as np

from . import processing
from . import feature


def envelope_stat(signal, samplerate, axis=-1) :
    '''
    '''
    band2 = ( 500, 1000)
    band5 = (3000, 4000)
    butterworth_order = 6
    signal2 = processing.butterworth_bandpass(signal, samplerate, band2, order=butterworth_order, axis=axis)
    signal5 = processing.butterworth_bandpass(signal, samplerate, band5, order=butterworth_order, axis=axis)
    envelope2 = feature.envelope(signal2, axis=axis)
    envelope5 = feature.envelope(signal5, axis=axis)
    q3_2 = np.percentile(envelope2, 75, axis=axis)
    q1_2 = np.percentile(envelope2, 25, axis=axis)
    iqr2 = q3_2 - q1_2
    mu2 = np.mean(envelope2, axis=axis)
    mu5 = np.mean(envelope5, axis=axis)
    stat = iqr2 - (mu2 - mu5)
    return np.piecewise(stat, [stat > 1.], [np.log10, 0.])


def variance_stat(spectre, Ntropy, samplerate, axis=(0, 1)) :
    '''
    '''
    spectre = np.asfarray(spectre)
    Nfft = spectre.shape[ axis[-1] ]
    
    step = samplerate // (Nfft - 1)
    band23 = (500, 2000)
    f_begin = np.ceil (band23[0] / step).astype(np.int)
    f_end   = np.floor(band23[1] / step).astype(np.int)
    
    spectre = np.swapaxes(spectre, axis[1], 0)
    spectre_band = np.swapaxes( spectre[f_begin : f_end + 1, ...], axis[1], 0 ) 
    entropy23 = feature.entropy(spectre_band, Ntropy, axis=axis[0])
    
    stat = np.var(entropy23, axis=axis[1])
    return stat