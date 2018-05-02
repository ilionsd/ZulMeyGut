# -*- coding: utf-8 -*-

import re as regex
from collections import namedtuple

from ..utility import shape


class Time( namedtuple('Time', ['hh', 'mm', 'ss', 'cc', 'raw']) ) :
                            
    @property
    def hours(self) :
        return self.hh
    @property
    def minutes(self) :
        return self.mm
    @property
    def seconds(self) :
        return self.ss
    @property
    def centiseconds(self) :
        return self.cc
    
    
class TimeFormat :
    FORMATS = {
        'SSA' : 
            { 'match'  : '(?P<hh>\d):(?P<mm>[0-5]\d):(?P<ss>[0-5]\d)[.:](?P<cc>\d\d)',
              'format' : '{:d}:{:02d}:{:02d}.{:02d}' }
        }
            
    def __init__(self, timeformat) :
        '''
        '''
        if not timeformat in TimeFormat.FORMATS :
            raise ValueError( str(TimeFormat.FORMATS.keys()) + ' allowed. Given ' + timeformat )
        self.__timeformat = timeformat
        self.__reference = regex.compile( TimeFormat.FORMATS[timeformat]['match'] )
        self.__view = TimeFormat.FORMATS[timeformat]['format']
        
    @property
    def timeformat(self) :
        return self.__timeformat
            
    def from_raw(self, arg) :
        raw = int(arg)
        hh, mm, ss, cc = shape.multi( shape=(60, 60, 100), plain=raw )
        return Time(hh, mm, ss, cc, raw)
    
    def from_str(self, arg) :
        string = str(arg)
        matching = self.__reference.match(string)
        if matching is None :
            raise ValueError( 'Time representation does not match time the format ' + str(self.__timeformat) )
        tup = matching.group('hh', 'mm', 'ss', 'cc')
        tup = map(int, tup)
        return self.from_tup(tup)
        
    def from_tup(self, arg) :
        tup = tuple(arg)
        hh, mm, ss, cc = tup
        raw = shape.plain( shape=(60, 60, 100), multi=tup )
        return Time(hh, mm, ss, cc, raw)
    
    def to_str(self, time) :
        hh, mm, ss, cc, _ = time
        return self.__view.format(hh, mm, ss, cc)
    
    
                
        
    
    
    
    
    
    
    
    