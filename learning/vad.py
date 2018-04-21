#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:08:03 2018

@author: ilion
"""

import numpy as np

import matplotlib.pyplot as plt

from voicepack import feature


def make_envelope(signal) :
    '''
    Plots signal and its envelope
    '''
    # Expect signal to be x(t)
    signal = np.asfarray(signal)
    envelope = feature.temporal_envelope(signal, axis=0)
    
    # Plotting
    fig = plt.figure('Temporal Envelope')
    fig.suptitle('Temporal Envelope')
    pic = fig.add_subplot('111')
    pic.plot(signal)
    pic.plot(envelope)
    pic.grid()
    return fig

def make_vad_envelope(signal, samplerate) :
    signal = np.asfarray(signal)
    vad_env = feature.vad_envelope(signal, samplerate, axis=-1)
    fig = plt.figure('VAD Envelope')
    fig.suptitle('VAD Envelope')
    pic = fig.add_subplot('111')
    pic.plot(vad_env)
    pic.grid()
    return fig