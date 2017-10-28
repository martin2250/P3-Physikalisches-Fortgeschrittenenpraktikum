#!/usr/bin/python
from __future__ import division, print_function
import sys
import numpy as np
import matplotlib.pyplot as plt

X, Y = np.loadtxt('source/energyspectrum.dat', unpack=True)

plt.plot(X, Y)
plt.xlabel('event energy (a.u.)')
plt.ylabel('capture count')
plt.grid()

if len(sys.argv) == 1:
	plt.show()
else:
	plt.savefig(sys.argv[1])
