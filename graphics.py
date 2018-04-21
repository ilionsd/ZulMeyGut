# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

import numpy as np 

def draw(data, title, cmap, norm) :
    fig = plt.figure(title)
    fig.suptitle(title)
    pic = fig.add_subplot('111')
    pcm = pic.pcolormesh(data.T, cmap=cmap, norm=norm)
    fig.colorbar(pcm)
    return fig
    
def percent_levels(data, percentile) :
    sorted_desc = np.sort(data)
    _, vals = np.percentile(np.cumsum(sorted_desc), percentile)
    return vals
    
def percentplot(data, percentile=[10, 20, 30, 40, 50, 60, 70, 80, 90], title='', colormap='magma') :
    cmap = plt.get_cmap(colormap)
    lvls = np.median( np.apply_along_axis(percent_levels, axis=1, arr=data, percentile=percentile), axis=0)
    norm = BoundaryNorm(lvls, ncolors=cmap.N, clip=True)
    return draw(data, title, cmap, norm)
    
def linplot(data, title='', colormap='magma') :
    cmap = plt.get_cmap(colormap)
    lvls = MaxNLocator(nbins=15).tick_values(data.min(), data.max())
    norm = BoundaryNorm(lvls, ncolors=cmap.N, clip=True)
    return draw(data, title, cmap, norm)