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


def butterworth_bandpass(signal, samplerate, band, order, axis=-1, zi=None) :
    signal = np.asfarray(signal)
    band = np.asfarray(band)
    nyquist_freq = samplerate / 2.
    sos = dsp.butter(N=order, Wn=band / nyquist_freq, btype='band', output='sos')
    if zi is None :
        zi = dsp.sosfilt_zi(sos)[..., np.newaxis]
    signal = np.swapaxes(signal, axis, 0)
    filtered, zf = dsp.sosfilt(sos, signal, axis=0, zi=zi * np.take(signal, [0], axis=0))
    return np.swapaxes(filtered, axis, 0), zf


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


def mirroring_crop(spectrogram, axis=-1) :
    spectrogram = np.asfarray(spectrogram)
    tmp = np.swapaxes(spectrogram, axis, -1)
    Nfft = spectrogram.shape[-1]
    half = Nfft // 2
    tmp = tmp[... , 0 : half]
    return np.swapaxes(tmp, axis, -1), half