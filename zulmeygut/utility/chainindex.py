# -*- coding: utf-8 -*-
from .shape import multi as shape_multi
from .shape import size as shape_size

class ChainIndex :
    
    def __init__(self, shape, index=0) :
        self.__shape = tuple(shape)
        self.__index = int(index)
        self.__size = shape_size(self.__shape)
        self.__multi_index = shape_multi(self.__shape, self.__index)
        self.__is_valid = 0 <= index and index < self.__size
        
    @property
    def shape(self) :
        return self.__shape
    @property
    def index(self) :
        return self.__index
    @property
    def size(self) :
        return self.__size
    @property
    def multi_index(self) :
        return self.__multi_index
    @property
    def is_valid(self) :
        return self.__is_valid
        
    def chain_next(self) :
        return ChainIndex(self.__shape, self.__index + 1)
    
    def chain_prev(self) :
        return ChainIndex(self.__shape, self.__index - 1)
    
    def __str__(self) :
        return '{0} of {1}'.format(self.__multi_index, self.__shape)
    