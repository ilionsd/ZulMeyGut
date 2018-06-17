#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:43:29 2018

@author: ilion
"""
import pandas as pd

from . import time


def load_formatted(lines, section='', retiter=False):
    try:
        lines = iter(lines)
    except TypeError:
        pass
    line = ''
    while line != section:
        try:
            line = next(lines).strip()
        except StopIteration:
            raise ValueError('Style section not found')
    line = ''
    while not line.startswith('Format:'):
        try:
            line = next(lines).strip()
        except StopIteration:
            raise ValueError('Format of style section not found')
    fields = line[len('Format:'):].split(',')
    fields = [field.strip() for field in fields]
    nextsection, eof = False, False
    data = {field: [] for field in fields}
    data['prefix'] = []
    length = 0
    while not nextsection and not eof:
        try:
            line = next(lines).strip()
        except StopIteration:
            eof=True
        else:
            if line and not line.startswith(';'):
                if line.startswith('['):
                    nextsection = True
                else:
                    prefix, _, line = line.partition(':')
                    values = line.split(',', maxsplit=len(fields) - 1)
                    values = [value.strip() for value in values]
                    data['prefix'].append(prefix)
                    for field, value in zip(fields, values):
                        data[field].append(value)
                    length += 1
    if retiter:
        return fields, data, length, lines
    else:
        return fields, data, length


def load_dataframe(lines, section=''):
    fields, events, length = load_formatted(lines, section='[Events]')
    events['Start'] = [time.tup_to_raw(time.parse_ssa(t)) for t in events['Start']]
    events['End'] = [time.tup_to_raw(time.parse_ssa(t)) for t in events['End']]
    return pd.DataFrame(events)





























