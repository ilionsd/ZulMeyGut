# -*- coding: utf-8 -*-

import numpy as np

from scipy import fftpack
from scipy import signal as dsp


def preemphasis(signal, alpha=.95, prev=0., axis=0, inplace=False) :
    '''
    '''
    signal = np.asfarray(signal)
    signal = np.swapaxes(signal, axis, 0)
    if not inplace :
        emphased = np.append(signal[0, ...] - prev, signal[1:, ...] - alpha * signal[:-1, ...])
        return np.swapaxes(emphased, axis, 0)
    else :
        for idx in np.ndindex(signal.shape[0]) :
            signal[idx, ...], prev = signal[idx, ...] - alpha * prev, signal[idx, ...]
        return np.swapaxes(signal, axis, 0)


def spectrogram(signal, axis=-1, inplace=False) :
    '''
    '''
    def square_modulus(ndarray, dtype) :
        return np.real(ndarray)**2 + np.imag(ndarray)**2;
    
    signal = np.asfarray(signal)
    signal = np.swapaxes(signal, axis, -1)
    Nfft = signal.shape[-1]
    dtype = signal.dtype
    fourier = fftpack.fft( signal * dsp.hamming(Nfft), axis=-1, overwrite_x=inplace )
    powers = square_modulus(fourier, dtype=dtype)
    return np.swapaxes(powers, axis, -1)