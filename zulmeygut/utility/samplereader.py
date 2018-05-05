# -*- coding: utf-8 -*-

import numpy as np
import soundfile as sf

class SampleReader :
    def __init__(self, filename, blocksize = 512, dtype='float64') :
        self.filename = filename
        self.file = None
        self.blocksize = blocksize
        self.dtype = dtype
        
    def __enter__(self) :
        self.file = sf.SoundFile(self.filename, mode='r')
        return self
    
    def __exit__(self, type, value, traceback) :
        self.file.close()
        
    @property
    def samplerate(self) :
        return self.file.samplerate
    @property
    def channels(self) :
        return self.file.channels
    
    def to_sample(self, time) :
        if time is None :
            return None
        return time * self.file.samplerate
    
    def align_floor(self, sample) :
        if sample is None :
            return None
        return self.blocksize * np.floor(sample / self.blocksize).astype( type(self.blocksize) )
    
    def align_ceil(self, sample) :
        if sample is None :
            return None
        return self.blocksize * np.ceil(sample / self.blocksize).astype( type(self.blocksize) )
    
    def sample_number(self) :
        return self.file.seek(0, sf.SEEK_END)
    
    def block_number(self) :
        return np.floor(self.sample_number() / self.blocksize).astype( type(self.blocksize) )
    
    def read(self, start=0, stop=None, inseconds=True) :
        if inseconds :
            start, stop = self.to_sample( start ), self.to_sample( stop )
        sample_0, sample_n = self.align_floor( start ), self.align_floor( stop ) 
        data, _ = sf.read(self.file.name, start=sample_0, stop=sample_n, dtype=self.dtype, fill_value=0)
        return data
    
    def read_all(self) :
        frames = self.sample_number()
        aligned_frames = self.align_ceil(frames)
        data, _ = sf.read(self.file.name, start=0, frames=aligned_frames, dtype=self.dtype, fill_value=0)
        return data
    
    def block(self, index) :
        sample_0 = self.blocksize * index
        data, _ = sf.read(self.file.name, start=sample_0, frames=self.blocksize, dtype=self.dtype, fill_value=0)
        return data



        
    
        
    
        
    
        
        