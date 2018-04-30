# -*- coding: utf-8 -*-

import numpy as np
from scipy import signal as dsp

from subspack import event

import sys
import shlex
import argparse
        

print( 'Hey, Im running! ' + __name__ )

def main(argv) :
    start = '0:00:00.00'
    end   = '0:01:55.00'
    directory = 'data/Hyperdimension Neptunia'
    audio      = '[Commie] Hyperdimension Neptunia The Animation - 01 [BD 1080p FLAC] [AEA707BB]_Audio02.flac'
    subs  = '[Commie] Hyperdimension Neptunia The Animation - 01 [BD 1080p FLAC] [AEA707BB]_Subtitles03.ass'
    argstr = '--start {0} --end {1} "{2}" "{3}"'.format(
            start, 
            end, 
            directory + '/' + audio, 
            directory + '/' + subs)
    
    formatter = event.TimeFormat('SSA')
    
    parser = argparse.ArgumentParser(description='Learning signal envelope')
    parser.add_argument('--start', type=formatter.from_str)
    parser.add_argument('--end'  , type=formatter.from_str)
    parser.add_argument('audio'    , type=str)
    parser.add_argument('subtitles', type=str)
    
    arglist = shlex.split(argstr)
    print( arglist )
    args = parser.parse_args( arglist )

    print(args)
    
    args = parser.parse_args( sys.argv )




if __name__ == '__main__' :
    main(sys.argv)
    
    

 