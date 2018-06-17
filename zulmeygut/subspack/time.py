#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:38:13 2018

@author: ilion
"""

import re as regex
from collections import namedtuple

from zulmeygut.utility.static_variables import static_variables
from zulmeygut.utility import shape


class Time(namedtuple('Time', ['hh', 'mm', 'ss', 'cc'])):
    def __repr__(self):
        return '{:d}:{:02d}:{:02d}.{:02d}'.format(self.hh, self.mm, self.ss, self.cc)


@static_variables(pattern=regex.compile('(?P<hh>\d):(?P<mm>[0-5]\d):(?P<ss>[0-5]\d)[.:](?P<cc>\d\d)'))
def parse_ssa(arg):
    arg = str(arg)
    matching = parse_ssa.pattern.match(arg)
    if matching is None:
        raise ValueError('Time representation {} does not match SSA time the format.'.format(arg))
    tup = matching.group('hh', 'mm', 'ss', 'cc')
    tup = map(int, tup)
    return Time(*tup)


@static_variables(pattern='{:d}:{:02d}:{:02d}.{:02d}')
def format_ssa(time):
    hh, mm, ss, cc = time.tup()
    return format_ssa.pattern.format(hh, mm, ss, cc)


def raw_to_tup(raw):
    raw = int(raw)
    hh, mm, ss, cc = shape.multi(shape=(60, 60, 100), plain=raw)
    return hh, mm, ss, cc


def tup_to_raw(tup):
    hh, mm, ss, cc = tuple(tup)
    raw = shape.plain(shape=(60, 60, 100), multi=(hh, mm, ss, cc))
    return raw
