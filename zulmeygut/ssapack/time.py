# -*- coding: utf-8 -*-

import re as regex
from collections import namedtuple

from zulmeygut.utility.static_variables import static_variables
from zulmeygut.utility import shape


TimeTuple = namedtuple('TimeTuple', ['hh', 'mm', 'ss', 'cc'])


def raw_to_tup(raw):
    raw = int(raw)
    hh, mm, ss, cc = shape.multi(shape=(60, 60, 100), plain=raw)
    return hh, mm, ss, cc


def tup_to_raw(tup):
    hh, mm, ss, cc = tuple(tup)
    raw = shape.plain(shape=(60, 60, 100), multi=(hh, mm, ss, cc))
    return raw


class Time:
    '''
    Subtitles event time representation
    '''
    def __init__(self, arg=None, hh=None, mm=None, ss=None, cc=None):
        if arg is not None:
            # 1st priority: ignore hh, mm, ss, cc
            try:
                # If not iterable
                arg = iter(arg)
            except TypeError:
                # Consider `arg` raw-time value
                raw = int(arg)
                hh, mm, ss, cc = raw_to_tup(raw)
            else:
                # Consider `arg` tup-time value
                tup = tuple(arg)
                hh, mm, ss, cc = tup
                raw = tup_to_raw(tup)
        elif hh is not None and mm is not None and ss is not None and cc is not None:
            # 2nd priority
            hh, mm, ss, cc = int(hh), int(mm), int(ss), int(cc)
            raw = tup_to_raw((hh, mm, ss, cc))
        else:
            hh, mm, ss, cc, raw = 0, 0, 0, 0, 0
        self.__hh, self.__mm, self.__ss, self.__cc, self.__raw = hh, mm, ss, cc, raw

    def __int__(self):
        return self.raw

    def __index__(self):
        return self.raw

    def __add__(self, other):
        return Time(self.raw + int(other))

    def __sub__(self, other):
        return Time(self.raw - int(other))

    def __radd__(self, other):
        return Time(int(other) + self.raw)

    def __rsub__(self, other):
        return Time(int(other) - self.raw)

    def __eq__(self, other):
        return self.raw == int(other)

    def __ne__(self, other):
        return self.raw != int(other)

    def __lt__(self, other):
        return self.raw < int(other)

    def __le__(self, other):
        return self.raw <= int(other)

    def __gt__(self, other):
        return self.raw > int(other)

    def __ge__(self, other):
        return self.raw >= int(other)

    def __repr__(self):
        return '{:d}:{:02d}:{:02d}.{:02d} ({})'.format(self.__hh, self.__mm, self.__ss, self.__cc, self.__raw)

    def tup(self):
        return TimeTuple(self.__hh, self.__mm, self.__ss, self.__cc)

    @property
    def hh(self):
        return self.__hh

    @property
    def mm(self):
        return self.__mm

    @property
    def ss(self):
        return self.__ss

    @property
    def cc(self):
        return self.__cc

    @property
    def raw(self):
        return self.__raw

    @property
    def hours(self):
        return self.hh

    @property
    def minutes(self):
        return self.mm

    @property
    def seconds(self):
        return self.ss

    @property
    def centiseconds(self):
        return self.cc


@static_variables(pattern=regex.compile('(?P<hh>\d):(?P<mm>[0-5]\d):(?P<ss>[0-5]\d)[.:](?P<cc>\d\d)'))
def parse_ssa(arg):
    arg = str(arg)
    matching = parse_ssa.pattern.match(arg)
    if matching is None:
        raise ValueError('Time representation {} does not match SSA time the format.'.format(arg))
    tup = matching.group('hh', 'mm', 'ss', 'cc')
    tup = map(int, tup)
    return Time(tup)


@static_variables(pattern='{:d}:{:02d}:{:02d}.{:02d}')
def format_ssa(time):
    hh, mm, ss, cc = time.tup()
    return format_ssa.pattern.format(hh, mm, ss, cc)


def astime(arg):
    return Time(arg)


def incenties(event_time):
    return event_time.raw


def inseconds(event_time):
    return event_time.raw / 100


def inminutes(event_time):
    return event_time.raw / (60 * 100)


def inhours(event_time):
    return event_time.raw / (60 * 60 * 100)
