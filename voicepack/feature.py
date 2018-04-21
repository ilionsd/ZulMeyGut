# -*- coding: utf-8 -*-

import numpy as np

from scipy import fftpack
from scipy import signal as dsp

from voicepack.utility import rolling_window
from voicepack.utility import polygon
from voicepack.utility import zero_elimination
from voicepack.utility import moveaxis


def mfe(powers, size, lower, upper, samplerate, axis=-1) : 
    '''
    Mel-Frequency Energy features
    '''
    def freq_to_mel(ndarray) :
        return 1125. * np.log(1. + ndarray / 700.)

    def mel_to_freq(ndarray) :
        return 700. * (np.exp(ndarray / 1125.) - 1.)
    
    def meldifference(start, stop) :
        return freq_to_mel(stop) - freq_to_mel(start)

    def melspace(start, stop, n) :
        mel_start = freq_to_mel(start)
        mel_stop  = freq_to_mel(stop )
        return mel_to_freq( np.linspace(mel_start, mel_stop, n) )

    def find_index(freq, samplerate, Nfft=512) :
        return np.round(Nfft * freq / samplerate).astype(type(Nfft))
    
    powers = np.asfarray(powers)
    energy = np.sum(powers, axis=axis)
    powers = np.swapaxes(powers, axis, -1)
    Nfft = powers.shape[-1]
    
    freq, step = np.linspace(0, samplerate, Nfft, retstep=True)
    point_limit = 1 + meldifference(upper, lower) // meldifference(lower + step, lower)
    if point_limit < size + 2 :
        size = point_limit - 2
    inds = find_index( melspace(lower, upper, size + 2), samplerate, Nfft )
    rolling_inds = rolling_window( inds, window=3 )
    
    mfe_shape = powers.shape[:-1] + (size,)
    tmp = np.empty(mfe_shape)
    
    for k in np.ndindex(size) :
        vertices = rolling_inds[k]
        triangle = polygon( x=freq[vertices], y=np.array([0, 1, 0]), mesh=freq, default=0 )
        tmp[... , k] = np.multiply(powers, triangle).sum(axis=-1, keepdims=True)
        
    return np.swapaxes(tmp, axis, -1), energy
    
def mfcc(powers, size, lower, upper, samplerate, dc=True, axis=-1) :
    '''
    Mel-Frequency Cepstral Coefficients
    '''
    mfe_feature, energy = mfe(powers, size, lower, upper, samplerate, axis=axis)
    mfe_feature = zero_elimination( mfe_feature )
    lmfe_feature = np.log( mfe_feature )
    mfcc_feature = fftpack.dct(lmfe_feature, axis=axis)
    if not dc :
        energy = zero_elimination(energy)
        mfcc_feature = moveaxis(mfcc_feature, axis, 0)
        mfcc_feature[0, ...] = np.log(energy)
        mfcc_feature = moveaxis(mfcc_feature, 0, axis)
    return mfcc_feature



def temporal_envelope(signal, axis=-1) :
    '''
    Absolute value of analytic signal
    '''
    return np.absolute( dsp.hilbert(signal, axis=axis) )

def vad_envelope(signal, samplerate, axis=-1) :
    '''
    Sub-Band temporal envelope feature
    '''
    def butterworth_bandpass(signal, samplerate, band, order, axis=-1) :
        signal = np.asfarray(signal)
        band = np.asfarray(band)
        nyquist_freq = samplerate / 2.
        b, a = dsp.butter(N=order, Wn=band / nyquist_freq, btype='band')
        return dsp.lfilter(b, a, signal, axis=axis)

    band2 = ( 500, 1000)
    band5 = (3000, 4000)
    butterworth_order = 6
    signal2 = butterworth_bandpass(signal, samplerate, band2, order=butterworth_order, axis=axis)
    signal5 = butterworth_bandpass(signal, samplerate, band5, order=butterworth_order, axis=axis)
    envelope2 = temporal_envelope(signal2, axis=axis)
    envelope5 = temporal_envelope(signal5, axis=axis)
    q3_2 = np.percentile(envelope2, 75, axis=axis)
    q1_2 = np.percentile(envelope2, 25, axis=axis)
    mu2 = np.mean(envelope2, axis=axis)
    mu5 = np.mean(envelope5, axis=axis)
    x = (q3_2 - q1_2) - (mu2 - mu5)
    return np.piecewise(x, [x > 1.], [np.log10, 0.])    
    
    
def entropy(spectrogram, Ntropy, axis=0) :
    '''
    Long-term signal variability measure
    '''
    rolling_spectre = rolling_window(spectrogram, window=Ntropy * 2 + 1, axes=axis)
    sum_spectre = np.sum(rolling_spectre, axis=-1, keepdims=True)
    normalized_rolling_spectre = rolling_spectre / sum_spectre
    e = -np.sum( normalized_rolling_spectre * np.log(normalized_rolling_spectre), axis=-1 )
    padding = ((0, 0),) * e.ndim
    padding = padding[:axis] + ((Ntropy, Ntropy),) + padding[axis + 1:]
    e = np.pad(e, padding, 'edge')
    return e

def vad_variance(spectrogram, Ntropy, samplerate, axis=(0, 1)) :
    '''
    '''
    spectrogram = np.asfarray(spectrogram)
    Nfft = spectrogram.shape[ axis[-1] ]
    
    step = samplerate // (Nfft - 1)
    # 2nd band first point
    f_begin = np.ceil ( 500 / step).astype(np.int)
    # 3rd band last point 
    f_end   = np.floor(2000 / step).astype(np.int)
    
    spectrogram = np.swapaxes(spectrogram, axis[1], 0)
    spectre_band = np.swapaxes( spectrogram[f_begin : f_end + 1, ...], axis[1], 0) 
    entropy23 = entropy(spectre_band, Ntropy, axis=axis[0])
    
    entropy_var = np.var(entropy23, axis=axis[1])
    return entropy_var
    












