#!/usr/bin/python
from __future__ import division, print_function
import numpy as np

angle, run, ch1, ch2, corr, rand = np.loadtxt('source/result.dat', dtype=None, unpack=True)

#fields, constants
d_fix			= 34							# in mm
d				= np.array([32.4, 28.5, 31.2])	# in mm
coin			= np.zeros(shape=(3, 6))
av_coin			= np.zeros(3)
err_coin		= np.zeros(3)

# method for evaluating data: http://www.physik.kit.edu/Studium/F-Praktika/Downloads/bb_gesamt_oktober_2017.pdf
# see section 7.7.4 (p. 147)

#distance correction
for i in range(0,3):
	d_corr				= (d[i]/d_fix)**2
	ch1[i*6:i*6+6] 		= ch1[i*6:i*6+6]*d_corr
	ch2[i*6:i*6+6]		= ch2[i*6:i*6+6]*d_corr
	rand[i*6:i*6+6]		= rand[i*6:i*6+6]*d_corr

# real coincidences with subtracted background
for i in range(0,3):
	prodch		= ch1[i*6:i*6+6]*ch2[i*6:i*6+6]
	prodchba	= ch1[-1]*ch2[-1]
	coin[i]		= ( corr[i*6:i*6+6]/prodch - corr[-1]/prodchba ) - ( rand[i*6:i*6+6]/prodch - rand[-1]/prodchba )
	#print(coin[i])
