# -*- coding: utf-8 -*-

import numpy as np


def moveaxis(ndarray, axis_src, axis_dst) :
    '''
    '''
    ndarray = np.asanyarray(ndarray)
    if axis_src == axis_dst :
        return ndarray.view()
    else :
        step = np.sign(axis_dst - axis_src)
        for axis in range(axis_src, axis_dst, step) :
            ndarray = np.swapaxes(ndarray, axis, axis + step)
        return ndarray


def zero_elimination(ndarray) :
    '''
    '''
    ndarray = np.asfarray(ndarray)
    ndarray[ndarray == 0] = np.finfo(ndarray.dtype).eps
    return ndarray