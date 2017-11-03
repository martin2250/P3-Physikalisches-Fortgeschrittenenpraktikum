#!/usr/bin/python
from __future__ import division, print_function
import numpy as np

angle, run, ch1, ch2, corr, rand = np.loadtxt('source/result.dat', dtype=None, unpack=True)

#fields, constants
d_fix			= 34							#in mm
d				= np.array([32.4, 28.5, 31.2])	#in mm
coin			= np.zeros(shape=(3, 6))		#number of coincidences
av_coin			= np.zeros(3)					#average of coincidences per angle
err_coin		= np.zeros(3)					#errors of avg. coincidences
a				= np.zeros(2)					#correlation function coefficients
#alternative method for evaluating data

for i in range(0,3):
	d_corr			= (d[i]/d_fix)**2			#distance correction
	ch1[i*6:i*6+6] 	= ch1[i*6:i*6+6]*d_corr		#
	ch2[i*6:i*6+6]	= ch2[i*6:i*6+6]*d_corr		#
	rand[i*6:i*6+6]	= rand[i*6:i*6+6]*d_corr	#

	coin[i]			= ( corr[i*6:i*6+6] - corr[-1] ) - ( rand[i*6:i*6+6] - rand[-1] )	#real coincidences with subtracted background and corrected distances

	#error calculations
	av_coin[i]		= np.mean(coin[i])
	err_coin[i]		= np.sqrt(av_coin[i])/np.sqrt(coin[i].size)	#assuming poisson distribution

#coefficients for calculation
A = av_coin[1]/av_coin[0]
B = av_coin[2]/av_coin[0]

#correlation function coefficients
a[0] = 2*(1+B-2*A)
a[1] = 4*A-B-3

#error calculation
delta_A = np.sqrt( ( 1/av_coin[0] * err_coin[1] )**2 + ( -(A/av_coin[0]) * err_coin[0] )**2 )	#gaussian error propagation for datermination coefficients
delta_B = np.sqrt( ( 1/av_coin[0] * err_coin[2] )**2 + ( -(B/av_coin[0]) * err_coin[0] )**2 )	#gaussian error propagation for datermination coefficients

delta_a		= np.zeros(2)
delta_a[0]	= np.sqrt( ( -4*delta_A )**2 + ( 2*delta_B )**2 )	#gaussian error propagation for coefficients
delta_a[1]	= np.sqrt( ( 4*delta_A )**2 + ( -delta_B )**2 )		#gaussian error propagation for coefficients

print('a2 = %.3f +/- %.4f, a4 = %.3f +/- %.4f' %(a[0], delta_a[0], a[1], delta_a[1]))
