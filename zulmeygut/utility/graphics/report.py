# -*- coding: utf-8 -*-
import os
import uuid

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator


class Report :
    def __init__(self, path, dataset, start, end) :
        if not os.path.isdir(path) :
            raise ValueError( '`path` can only be directory ' )
        self.dest = os.path.join(path, '{}: [{} - {}]'.format(dataset, start, end) )
        if not os.path.exists(self.dest) :
            os.mkdir(self.dest)
            
        
    def linplot(self, data, title='', savefig=True) :
        '''
        '''
        data = np.asfarray(data)
        title = str(title)
        title = title if title else str( uuid.uuid4() )
        fig = plt.figure(title)
        fig.suptitle(title)
        pic = fig.add_subplot('111')
        if data.ndim == 1 :
            pic.plot(data, label=title)
            pic.legend()
        else :
            index = np.ndindex(data.shape[0])
            labels = np.asarray([label.strip() for label in title.split('|')])
            for k in index:
                entry = np.ravel(data[k, ...])
                pic.plot(entry, label=labels[k])
            pic.legend()
        if savefig :
            filename = self.dest + '/' + title
            fig.savefig(filename, format='png')
        return fig
    
    def draw(self, data, title, cmap, norm, savefig=True) :
        fig = plt.figure(title)
        fig.suptitle(title)
        pic = fig.add_subplot('111')
        pcm = pic.pcolormesh(data.T, cmap=cmap, norm=norm)
        fig.colorbar(pcm)
        
        if savefig :
            filename = self.dest + '/' + title
            fig.savefig(filename, format='png')
        return fig
    
    def linmesh(self, data, title='', colormap='magma', savefig=True) :
        cmap = plt.get_cmap(colormap)
        lvls = MaxNLocator(nbins=15).tick_values(data.min(), data.max())
        norm = BoundaryNorm(lvls, ncolors=cmap.N, clip=True)
        return self.draw(data, title, cmap, norm, savefig)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    