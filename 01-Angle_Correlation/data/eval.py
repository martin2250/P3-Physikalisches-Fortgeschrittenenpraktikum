#!/usr/bin/python
from __future__ import division, print_function
import numpy as np

angle, run, ch1, ch2, corr, rand = np.loadtxt('source/result.dat', dtype=None, unpack=True)

#fields, constants
d_fix			= 34							# in mm
d				= np.array([32.4, 28.5, 31.2])	# in mm
dba				= (d[0]/d_fix)**2				# background meas. was done at 90 degrees
coin			= np.zeros(shape=(3, 6))
av_coin			= np.zeros(3)
err_coin		= np.zeros(3)

for i in range(0,3):
	d_corr		= (d[i]/d_fix)**2																	# distance correction
	coin[i]		= ((corr[i*6:i*6+6]*d_corr - corr[-1]*dba)-(rand[i*6:i*6+6]*d_corr - rand[-1])*dba)	# real coincidences with subtracted background and corrected distance
	av_coin[i] 	= np.mean(coin[i])
	err_coin[i]	= np.sqrt(av_coin[i])																# assuming poisson distribution on event count
	err_coin[i] = err_coin[i]/np.sqrt(coin[i].size) 												# see: https://pawn.physik.uni-wuerzburg.de/~reusch/fehler/wisem0102/vorlesung7.pdf
	print(av_coin[i], '+/-', err_coin[i])
