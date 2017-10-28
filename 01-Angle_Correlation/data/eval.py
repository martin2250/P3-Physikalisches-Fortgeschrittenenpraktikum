#!/usr/bin/python
from __future__ import division, print_function
import numpy as np

D = np.loadtxt('source/result.dat', dtype=None, unpack=True)

d90 = D[0:6]
d135 = D[6:12]
d180 = D[12:18]
bg = D[18:18]
