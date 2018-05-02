# -*- coding: utf-8 -*-
import os
import sys


CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')


# The Way of the Voice
sys.path.append( PROJECT_DIR )

from utility.shape import multi, plain
from subspack.event import TimeFormat


shape = (2, 3)
plain_index = 19
multi_index = (3, 0, 1)
print( multi(shape, plain_index) )
print( plain(shape, multi_index) )


time_str = '0:11:22.33'

formatter = TimeFormat('SSA')
from_str = formatter.from_str(time_str)

print( from_str )

