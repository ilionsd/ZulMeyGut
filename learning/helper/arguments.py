# -*- coding: utf-8 -*-

import os
import sys
import argparse

CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR, '../../')

# The Way of the Voice
sys.path.append( PROJECT_DIR )

from zulmeygut.subspack import event

def arguments(argv, description='') :
    time_parser = event.TimeParser('SSA')
    
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--start', type=time_parser.parse)
    parser.add_argument('--end'  , type=time_parser.parse)
    parser.add_argument('audio'    , type=str)
    parser.add_argument('subtitles', type=str)
    
    args = parser.parse_args( argv )
    
    audio, subtitles = args.audio, args.subtitles
    start, end = args.start, args.end
    
    return (audio, subtitles, start, end)
    