#!/usr/bin/python
from __future__ import division, print_function
import numpy as np

angle, run, ch1, ch2, corr, rand = np.loadtxt('source/result.dat', dtype=None, unpack=True)

coin			= np.zeros(shape=(3, 6))
av_coin			= np.zeros(3)
err_coin		= np.zeros(3)

for i in range(0,3):
	coin[i]		= (corr[i*6:i*6+6]-corr[-1])-(rand[i*6:i*6+6]-rand[-1])	# real coincidences with subtracted background
	av_coin[i] 	= np.mean(coin[i])
	err_coin[i]	= np.sqrt(av_coin[i])									# assuming poisson distribution on event count
	err_coin[i] = err_coin[i]/np.sqrt(coin[i].size) 					# see: https://pawn.physik.uni-wuerzburg.de/~reusch/fehler/wisem0102/vorlesung7.pdf
	#print(av_coin[i], '+/-', err_coin[i])
