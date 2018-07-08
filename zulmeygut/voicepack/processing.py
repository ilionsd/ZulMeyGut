# -*- coding: utf-8 -*-

import numpy as np

from scipy import fftpack
from scipy import signal as dsp


def preemphasis(signal, alpha=.95, prev=0., axis=0, inplace=False):
    '''
    '''
    signal = np.asfarray(signal)
    signal = np.swapaxes(signal, axis, 0)
    if not inplace:
        emphased = np.append(signal[0, ...] - prev, signal[1:, ...] - alpha * signal[:-1, ...])
        return np.swapaxes(emphased, axis, 0)
    else :
        for idx in np.ndindex(signal.shape[0]):
            signal[idx, ...], prev = signal[idx, ...] - alpha * prev, signal[idx, ...]
        return np.swapaxes(signal, axis, 0)


def butterworth_bandpass(signal, samplerate, band, order, axis=-1, zi=None):
    signal = np.asfarray(signal)
    band = np.asfarray(band)
    nyquist_freq = samplerate / 2.
    sos = dsp.butter(N=order, Wn=band / nyquist_freq, btype='band', output='sos')
    if zi is None:
        zi = dsp.sosfilt_zi(sos)[..., np.newaxis]
    filtered, zf = dsp.sosfilt(sos, signal, axis=axis, zi=zi * np.take(signal, [0], axis=axis))
    return filtered, zf


def spectrum(signal, axis=-1, ret=True, inplace=False):
    '''
    Absolute value of DFT of signal divided into frames over given axis
    '''
    def square_modulus(ndarray, dtype):
        return np.real(ndarray)**2 + np.imag(ndarray)**2

    def combined_fft(signal, axis, ret, inplace):
        if len(ret) == 0:
            return ()
        else:
            fourier = fftpack.fft(signal, axis=-1, overwrite_x=inplace)
            powers = square_modulus(fourier, dtype=dtype)
            if not inplace and ret[0]:
                return (powers,) + combined_fft(powers, axis=axis, ret=ret[1:], inplace=inplace)
            else:
                return combined_fft(powers, axis=axis, ret=ret[1:], inplace=inplace)

    signal = np.asfarray(signal)
    ret = tuple(ret)
    signal = np.swapaxes(signal, axis, -1)
    Nfft = signal.shape[-1]
    dtype = signal.dtype
    powers_tuple = combined_fft(signal * dsp.hamming(Nfft), axis=-1, ret=ret, inplace=inplace)
    powers_tuple = tuple(np.swapaxes(powers, axis, -1) for powers in powers_tuple)
    if len(powers_tuple) == 0:
        return None
    elif len(powers_tuple) == 1:
        return powers_tuple[0]
    else:
        return powers_tuple


def mirroring_crop(spectrogram, axis=-1):
    spectrogram = np.asfarray(spectrogram)
    tmp = np.swapaxes(spectrogram, axis, -1)
    Nfft = spectrogram.shape[-1]
    half = Nfft // 2
    tmp = tmp[..., 0: half]
    return np.swapaxes(tmp, axis, -1), half
