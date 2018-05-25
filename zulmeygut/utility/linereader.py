#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 18:31:27 2018

@author: ilion
"""
import os
import chardet
import codecs


def encoding(filename):
    size = min(32, os.path.getsize(filename))
    with open(filename, 'rb') as file:
        raw = file.read(size)
    if raw.startswith(codecs.BOM_UTF8):
        return 'utf-8-sig'
    else:
        result = chardet.detect(raw)
        return result['encoding']


def read_all(filename):
    with open(filename, 'r', encoding=encoding(filename)) as file:
        lines = file.read().splitlines()
    return lines
