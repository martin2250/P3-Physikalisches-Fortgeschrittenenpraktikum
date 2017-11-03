#!/usr/bin/python
from __future__ import division, print_function
import numpy as np

angle, run, ch1, ch2, corr, rand = np.loadtxt('source/result.dat', dtype=None, unpack=True)

# method for evaluating data: http://www.physik.kit.edu/Studium/F-Praktika/Downloads/bb_gesamt_oktober_2017.pdf
# see section 7.7.4 (p. 147)

#constants
d_fix			= 34							# in mm
d				= np.array([32.4, 28.5, 31.2])	# in mm

#distance correction
for i in range(0,3):
	d_corr				= (d[i]/d_fix)**2
	ch1[i*6:i*6+6] 		= ch1[i*6:i*6+6]*d_corr
	ch2[i*6:i*6+6]		= ch2[i*6:i*6+6]*d_corr
	rand[i*6:i*6+6]		= rand[i*6:i*6+6]*d_corr
	corr[i*6:i*6+6]		= corr[i*6:i*6+6]*d_corr

#subtract background
ch1_i = ch1[:-1] - ch1[-1]
ch2_i = ch2[:-1] - ch2[-1]
corr_i = corr[:-1] - corr[-1]
rand_i = rand[:-1] - rand[-1]
#reduce event counts by dividing by product of channels
pch = ch1_i*ch2_i
red_corr = corr_i/pch
red_rand = rand_i/pch

#subtract random coincidences from correlations to yield reduced real coincidences
red_coin = red_corr - red_rand

###------- FIRST METHOD -----------

#fields
coin		= np.zeros(shape=(3, 6))
sum_coin	= np.zeros(3)

#slice coincidences for angle analysis
for i in range(0,3):
	coin[i] = red_coin[i*6:i*6+6]

#sum event counts per angle
sum_coin = np.sum(coin, axis=1)

#coefficients for calculation of correlation function coeff.
A = sum_coin[1]/sum_coin[0]
B = sum_coin[2]/sum_coin[0]

#correlation function coeff.
a = np.zeros(2)
a[0] = 4*A - B - 3		#a_2
a[1] = 2*(1 + B - 2*A)	#a_4
An = B - 1				#anisotropy

##ERROR CALCULATION
d_Ni1 = np.sqrt(ch1[:-1] + ch1[-1])
d_Ni2 = np.sqrt(ch1[:-1] + ch1[-1])

d_Nci = np.sqrt(corr[:-1] + corr[-1])
d_Nri = np.sqrt(rand[:-1] + rand[-1])

d_red_corr_i = np.sqrt( ( 1/pch * d_Nci )**2 + ( -red_corr/ch1[:-1] * d_Ni1 )**2 + ( -red_corr/ch2[:-1] * d_Ni2 )**2 )
d_red_rand_i = np.sqrt( ( 1/pch * d_Nri )**2 + ( -red_rand/ch1[:-1] * d_Ni1 )**2 + ( -red_rand/ch2[:-1] * d_Ni2 )**2 )

d_red_coin_i = np.sqrt( d_red_corr_i**2 + d_red_rand_i**2 )

d_red_coin_theta = np.zeros(shape=(3, 6))
for i in range(0,3):
	d_red_coin_theta[i] = d_red_coin_i[i*6:i*6+6]

d_tot = np.zeros(3)
d_tot[0] = np.sqrt( d_red_coin_theta[0][0]**2 + d_red_coin_theta[0][1]**2 + d_red_coin_theta[0][2]**2)

for i in range(0,3):
	for j in range(0,6):
		d_tot[i] = d_tot[i] + d_red_coin_theta[i][j]

d_A = np.sqrt( ( 1/sum_coin[0] * d_tot[1] )**2 + ( -A/sum_coin[0] * d_tot[0])**2 )
d_B = np.sqrt( ( 1/sum_coin[0] * d_tot[2] )**2 + ( -B/sum_coin[0] * d_tot[0])**2 )

delta_a		= np.zeros(2)
delta_a[1]	= np.sqrt( ( -4*d_A )**2 + ( 2*d_B )**2 )	#gaussian error propagation for coefficients
delta_a[0]	= np.sqrt( ( 4*d_A )**2 + ( -d_B )**2 )		#gaussian error propagation for coefficients
delta_An	= d_B										#gaussian error propagation for anisotropy

print('\na2 = %.3f +/- %.4f, a4 = %.3f +/- %.4f, An = %.3f +/- %.4f' %(a[0], delta_a[0], a[1], delta_a[1], An, delta_An))

#relative deviations
theo_a	= np.array([1/8, 1/24])
theo_An	= 0.167

rel_a	= np.abs(theo_a - a)/theo_a * 100
rel_An	= np.abs(theo_An - An)/theo_An * 100

print('\nrelative deviations: a2_rel = %.2f%%, a4_rel = %.2f%%, An_rel = %.2f%%\n' %(rel_a[0], rel_a[1], rel_An))
###------- FIRST METHOD END-----------
