# -*- coding: utf-8 -*-

import pysubs2

def extract_timing(file) :
    subs = pysubs2.load(file, encoding='utf-8')
    timing = []
    for event in subs.events :
        timing.append( {'start' : event.start, 'end' : event.end} )
    return timing
    
    