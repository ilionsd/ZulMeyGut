# -*- coding: utf-8 -*-

from .shape import multi as shape_multi

from collections import namedtuple

def max_multi_index(shape) :
    index = ()
    for k in range(len(shape)) :
        index += (shape[k] - 1,)
    return index

class ChainIndex( namedtuple('ChainIndex', ['shape', 'index', 'multi_index', 'is_valid']) ) :
        
    def next(self) :
        next_index = self.index + 1
        next_multi_index = shape_multi( self.shape, next_index )
        next_is_valid = 0 <= next_index and next_multi_index < self.shape
        return ChainIndex(self.shape, next_index, next_multi_index, next_is_valid)
    
    def prev(self) :
        prev_index = self.index - 1
        prev_multi_index = shape_multi( self.shape, prev_index )
        prev_is_valid = 0 <= prev_index and prev_multi_index < self.shape
        return ChainIndex(self.shape, prev_index, prev_multi_index, prev_is_valid)