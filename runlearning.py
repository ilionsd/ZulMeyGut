# -*- coding: utf-8 -*-
import os
import sys
import subprocess


directory = 'data/Hyperdimension Neptunia'
default_audio = '[Commie] Hyperdimension Neptunia The Animation - 01 [BD 1080p FLAC] [AEA707BB]_Audio02.flac'
default_subs  = '[Commie] Hyperdimension Neptunia The Animation - 01 [BD 1080p FLAC] [AEA707BB]_Subtitles03.ass'

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

start = test_data[test_case]['start']
stop = test_data[test_case]['end']


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))


if __name__ == '__main__' :
    task = [sys.executable,
            './learning/envelope.py', 
            '--start', '0:00:00.00', 
            '--end'  , '0:01:55.00',
            directory + '/' + default_audio,
            directory + '/' + default_subs]
    #result = subprocess.run(task, stdout=subprocess.PIPE, shell=True)
    #print( result )
    
#sys.exit()
