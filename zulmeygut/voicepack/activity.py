# -*- coding: utf-8 -*-

import numpy as np

from . import processing
from . import feature


def envelope_stat(signal, samplerate, axes=(0, -1)) :
    '''
    Sub-band temporal envelope analysis
    '''
    band2 = ( 500, 1000)
    band5 = (3000, 4000)
    butterworth_order = 6
    if axes[0] == axes[1] :
        raise ValueError('Axes {} must be different'.format(axes))
    
    if axes[0] < axes[1] :
        axisN = axes[1] - 1
    else :
        axisN = axes[1]
    signal = np.moveaxis(signal, axes[0], 0)
            
    signal2 = np.empty( signal.shape, signal.dtype )
    signal5 = np.empty( signal.shape, signal.dtype )
    zf2, zf5 = None, None
    for index, in np.ndindex( signal.shape[0] ) :
        frame = np.take(signal, index, axis=0)
        signal2[index, ...], zf2 = processing.butterworth_bandpass(frame, samplerate, band2, zi=zf2,
               order=butterworth_order, axis=axisN)
        signal5[index, ...], zf5 = processing.butterworth_bandpass(frame, samplerate, band5, zi=zf5,
               order=butterworth_order, axis=axisN)
    signal2 = np.moveaxis(signal2, 0, axes[0])
    signal5 = np.moveaxis(signal5, 0, axes[0])
    
    envelope2 = feature.envelope(signal2, axis=axes[1])
    envelope5 = feature.envelope(signal5, axis=axes[1])
    q3_2 = np.percentile(envelope2, 75, axis=axes[1])
    q1_2 = np.percentile(envelope2, 25, axis=axes[1])
    iqr2 = q3_2 - q1_2
    mu2 = np.mean(envelope2, axis=axes[1])
    mu5 = np.mean(envelope5, axis=axes[1])
    stat = iqr2 - (mu2 - mu5)
    stat *= 2**15
    return np.piecewise(stat, [stat > 0.], [np.log10, 0])


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

















