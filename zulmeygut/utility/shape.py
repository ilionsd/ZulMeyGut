# -*- coding: utf-8 -*-

def multi(shape, plain) :
    '''
    Shaping plain index into multi index
    '''
    if len(shape) == 0 :
        return (plain,) if plain != 0 else ()
    else :
        q, r = divmod(plain, shape[-1])
        return multi(shape[0 : -1], q) + (r,)
    
def plain(shape, multi) :
    '''
    Smoothing multi index to plain index
    '''
    if len(shape) == 0 :
        return multi[-1] if len(multi) > 0 else 0
    else :
        return multi[-1] + shape[-1] * plain(shape[0 : -1], multi[0 : -1])
    
def first(shape) :
    return (0,) * len(shape)

def last(shape) :
    last = ()
    for item in shape :
        last += (item - 1,)
    return last 

def size(shape) :
    return plain(shape, last(shape)) + 1