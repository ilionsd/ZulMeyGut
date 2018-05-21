# -*- coding: utf-8 -*-

import os
import sys
import argparse

CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR, '../../')

# The Way of the Voice
sys.path.append( PROJECT_DIR )

from zulmeygut.subspack import time

def arguments(argv, description='') :
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--start', type=time.parse_ssa)
    parser.add_argument('--end'  , type=time.parse_ssa)
    parser.add_argument('audio'    , type=str)
    parser.add_argument('subtitles', type=str)

    args = parser.parse_args( argv )

    return args

def dataset(datafile) :
    head, _ = os.path.split(datafile)
    return os.path.basename(head)
    