# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt




def linplot(data, title='') :
    data = np.asfarray(data)
    fig = plt.figure(title)
    fig.suptitle(title)
    pic = fig.add_subplot('111')
    it = np.nditer(data, ['external_loop'], ['readonly'])
    for item in it :
        item = np.ravel(item)
        pic.plot(item)
    return fig