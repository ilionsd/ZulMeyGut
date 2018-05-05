# -*- coding: utf-8 -*-

import numpy as np

from scipy import fftpack
from scipy import signal as dsp

from ..utility.strides import rolling_window
from ..utility.common import zero_elimination
from ..utility.common import moveaxis


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
    
    def polygon(x, y, mesh, default=0, dtype=np.float64) :
        '''
        (x - x1) / (x2 - x1) = (y - y1) / (y2 - y1) -->
        --> y = [(y2 - y1) / (x2 - x1)] * x - [(y2 - y1) / (y2 - y1)] * x1 + y1
        '''
        def line(x, y, mesh, lb=np.less, rb=np.less_equal) :
            cn = np.logical_and( lb(x[0], mesh), rb(mesh, x[1]) )
            fn = lambda t: ((y[1] - y[0]) * (t - x[0]) / (x[1] - x[0])) + y[0]
            return cn, fn
            
        it = np.nditer([ rolling_window(x, window=2), rolling_window(y, window=2) ],
                        ['external_loop'], [['readonly'], ['readonly']])
        
        cn = np.array([])
        fn = np.array([])
        first = True
        for xi, yi in it :
            ci, fi = line(xi, yi, mesh, lb=np.less_equal if first else np.less, rb=np.less_equal)
            cn = np.append(cn, ci)
            fn = np.append(fn, fi)
            first = False
            
        cn = cn.reshape((-1, mesh.size))
        fn = np.append(fn, default)
        return np.piecewise(mesh.astype(dtype), cn, fn)
    
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



def envelope(signal, axis=0) :
    '''
    Absolute value of analytic signal
    '''
    return np.absolute( dsp.hilbert(signal, axis=axis) )

    
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
    












