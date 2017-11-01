#!/usr/bin/python
from __future__ import division, print_function
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks_cwt

X, Y = np.loadtxt('source/energyspectrum.dat', unpack=True)

def annotateallthethings(x, y):
	y_trimmed1 = y[230:285]
	y_trimmed2 = y[289:366]
	i = (np.argmax(y_trimmed1), np.argmax(y_trimmed2))
	plt.annotate('1173 keV photopeak', xy=(x[i[0]+230]+10, y[i[0]+230]+10), xytext=(x[i[0]+230]+150, y[i[0]+230]+300), arrowprops=dict(facecolor='black', shrink=0.005))
	plt.annotate('1332 keV photopeak', xy=(x[i[1]+289]+10, y[i[1]+289]+10), xytext=(x[i[1]+289]+150, y[i[1]+289]+150), arrowprops=dict(facecolor='black', shrink=0.005))

	plt.text(3730, 1680, 'energy threshold', color='xkcd:teal')

plt.plot(X, Y)
plt.xlabel('event energy (a.u.)')
plt.ylabel('capture count')
plt.axvline(x=3700, color='xkcd:teal')	#yes, there is an xkcd color palette. see https://matplotlib.org/api/colors_api.html
plt.text(3730, 1680, 'energy threshold', color='xkcd:teal')
annotateallthethings(X, Y)
plt.grid()

if len(sys.argv) == 1:
	plt.show()
else:
	plt.savefig(sys.argv[1])
