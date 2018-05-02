# -*- coding: utf-8 -*-
import os
import sys


CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')


# The Way of the Voice
sys.path.append( PROJECT_DIR )

import shlex
import argparse

import numpy as np
from scipy import signal as dsp

from zulmeygut.subspack import event
        

def main(argv) :
    start = '0:00:00.00'
    end   = '0:01:55.00'
    audio = 'someaudio'
    subs  = 'somesubs'
    argstr = '--start {0} --end {1} "{2}" "{3}"'.format(
            start, 
            end, 
            audio, 
            subs)
    
    formatter = event.TimeFormat('SSA')
    
    parser = argparse.ArgumentParser(description='Learning signal envelope')
    parser.add_argument('--start', type=formatter.from_str)
    parser.add_argument('--end'  , type=formatter.from_str)
    parser.add_argument('audio'    , type=str)
    parser.add_argument('subtitles', type=str)
    
    print( 'Passed arguments:' )
    print( argv )
    args = parser.parse_args( argv )
    print(args)
    
    print( 'Predefined arguments' ) 
    argv = shlex.split(argstr)
    print(argv)
    args = parser.parse_args(argv)
    print(args)
    

if __name__ == '__main__' :
    main(sys.argv[1:])
    
    

 