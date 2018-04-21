# -*- coding: utf-8 -*-

from voicepack.samplereader import SampleReader
from voicepack import processing

from learning import vad


directory = 'data/Hyperdimension Neptunia'
audio = '[Commie] Hyperdimension Neptunia The Animation - 01 [BD 1080p FLAC] [AEA707BB]_Audio02.flac'
subs  = '[Commie] Hyperdimension Neptunia The Animation - 01 [BD 1080p FLAC] [AEA707BB]_Subtitles03.ass'

test_data = {
        'swear_speech' : 
            { 'start' :   0, 'end' : 115, 'speakers' : 1 },
        'banquet_dialogue' : 
            { 'start' : 115, 'end' : 167, 'speakers' : 4 },
        'lazynep_scolded' : 
            { 'start' : 173, 'end' : 217, 'speakers' : 3 },
        'antigoddess_pamphlets' : 
            { 'start' : 307, 'end' : 331, 'speakers' : 3 },
        'share_energy_talk' :
            { 'start' : 332, 'end' : 450, 'speakers' : 5 }
        }
test_case = 'swear_speech'

Nfft = 1024
start = test_data[test_case]['start']
stop = test_data[test_case]['end']

with SampleReader(directory + '/' + audio, blocksize=Nfft) as reader :
    samplerate = reader.file.samplerate
    channels = reader.file.channels
    
    signal = reader.read(start=start, stop=stop, inseconds=True)

channel = 0
signal = signal[:, 0]
emphased_signal = processing.preemphasis(signal, alpha=0.95)

vad.make_envelope(signal)

signal = signal.reshape((-1, Nfft))
vad.make_vad_envelope(signal, samplerate)

vad.make_envelope(emphased_signal)

emphased_signal = emphased_signal.reshape((-1, Nfft))
vad.make_vad_envelope(emphased_signal, samplerate)

