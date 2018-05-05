# -*- coding: utf-8 -*-

import re as regex

from ..utility import shape


class Time :
    
    def __init__(self, hh, mm, ss, cc, raw) :
        self.__hh = hh
        self.__mm = mm
        self.__ss = ss
        self.__cc = cc
        self.__raw = raw
        
    def __add__(self, other) :
        if not other is Time :
            raise NotImplemented('Defined only for time')
        return raw_to_time(self.raw + other.raw)
    
    def __sub__(self, other) :
        if not other is Time :
            raise NotImplemented('Defined only for time')
        return raw_to_time(self.raw - other.raw)
        
    @property
    def hh(self) :
        return self.__hh
    @property
    def mm(self) :
        return self.__mm
    @property
    def ss(self) :
        return self.__ss
    @property
    def cc(self) :
        return self.__cc
    @property
    def raw(self) :
        return self.__raw
                            
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
    

def raw_to_time(arg) :
    raw = int(arg)
    hh, mm, ss, cc = shape.multi( shape=(60, 60, 100), plain=raw )
    return Time(hh, mm, ss, cc, raw)


def tup_to_time(arg) :
    tup = tuple(arg)
    hh, mm, ss, cc = tup
    raw = shape.plain( shape=(60, 60, 100), multi=tup )
    return Time(hh, mm, ss, cc, raw)

def astime(arg) :
    if arg is Time :
        return arg
    elif arg is int :
        return raw_to_time(arg)
    elif arg is tuple :
        return tup_to_time(arg)
    else :
        raise ValueError( 'Unsupported type' )


class TimeParser :
    SPEC = {
            'SSA' : '(?P<hh>\d):(?P<mm>[0-5]\d):(?P<ss>[0-5]\d)[.:](?P<cc>\d\d)',
            }
    
    def __init__(self, timeformat) :
        '''
        '''
        if not timeformat in TimeParser.SPEC :
            raise ValueError( str(TimeParser.SPEC.keys()) + ' allowed. Given ' + timeformat )
        self.__timeformat = timeformat
        self.__reference = regex.compile( TimeParser.SPEC[timeformat] )
        
    @property
    def timeformat(self) :
        return self.__timeformat
    
    def parse(self, arg) :
        string = str(arg)
        matching = self.__reference.match(string)
        if matching is None :
            raise ValueError( 'Time representation does not match time the format ' + str(self.__timeformat) )
        tup = matching.group('hh', 'mm', 'ss', 'cc')
        tup = map(int, tup)
        return tup_to_time(tup)


class TimeFormatter :
    SPEC = {
        'SSA' : '{:d}:{:02d}:{:02d}.{:02d}',
        }
            
    def __init__(self, timeformat) :
        '''
        '''
        if not timeformat in TimeFormatter.SPEC :
            raise ValueError( str(TimeFormatter.SPEC.keys()) + ' allowed. Given ' + timeformat )
        self.__timeformat = timeformat
        self.__view = TimeFormatter.SPEC[timeformat]
        
    @property
    def timeformat(self) :
        return self.__timeformat
    
    def format(self, time) :
        hh, mm, ss, cc, _ = time
        return self.__view.format(hh, mm, ss, cc)
    
def incenties(event_time) :
    return event_time.raw

def inseconds(event_time) :
    return event_time.raw / 100

def inminutes(event_time) :
    return event_time.raw / (60 * 100)

def inhours(event_time) :
    return event_time.raw / (60 * 60 * 100)

    
    
                
        
    
    
    
    
    
    
    
    