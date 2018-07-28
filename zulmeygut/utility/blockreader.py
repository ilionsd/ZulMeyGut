# -*- coding: utf-8 -*-

import soundfile as sf
import numpy as np


def align_floor(blocksize, sample):
    return blocksize * np.floor(sample / blocksize).astype(type(sample))


def align_ceil(blocksize, sample):
    return blocksize * np.ceil(sample / blocksize).astype(type(sample))


def info(filename):
    with sf.SoundFile(filename, 'r') as file:
        channels = file.channels
        samplerate = file.samplerate
        samples = file.seek(0, sf.SEEK_END)
    return channels, samples, samplerate


class BlockReader:
    '''
    '''
    def __init__(self, filename, start, stop, blocksize=1, dtype='float64', 
                 zeropadding=True, retindex=True):
        self.filename = filename
        self.start = start
        self.stop = stop
        self.blocksize = blocksize
        self.dtype = dtype
        self.zeropadding = zeropadding
        self.retindex = retindex
        self.__index = 0

    @property
    def index(self):
        return self.__index

    @property
    def size(self):
        return np.ceil((self.stop - self.start) / self.blocksize).astype(type(self.blocksize));

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        block_start = self.start + self.blocksize * self.__index
        block_stop = block_start + self.blocksize
        if block_start >= self.stop:
            raise StopIteration()
        if block_stop <= self.stop:
            data, _ = sf.read(self.filename, start=block_start, stop=block_stop, dtype=self.dtype)
        else:
            data, _ = sf.read(self.filename, start=block_start, stop=self.stop , dtype=self.dtype)
            if self.zeropadding :
                data = np.pad(data, ((0, block_stop - self.stop), (0, 0)), 'constant')
        index = self.index
        self.__index += 1
        if self.retindex:
            return data, index
        else:
            return data

    def reset(self):
        self.__index = 0
