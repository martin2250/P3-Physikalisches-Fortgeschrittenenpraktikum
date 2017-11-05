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
d_red_coin = np.sqrt(1/pch**2 * ( corr_i + rand_i + ((corr_i - rand_i)**2/ch1[:-1]**2)*ch1[:-1] + ((corr_i - rand_i)**2/ch2[:-1]**2)*ch2[:-1] ))	#assumed background to be negligable

###------- FIRST METHOD --------------------------------------------------------

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
#slice delta red. coin per angle
d_red_coin_theta = np.zeros(shape=(3, 6))
for i in range(0,3):
	d_red_coin_theta[i] = d_red_coin[i*6:i*6+6]

#errors for means per angle
d_tot = np.zeros(3)

for i in range(0,3):
	for j in range(0,6):
		d_tot[i] = d_tot[i] + d_red_coin_theta[i][j]**2

d_tot = np.sqrt(d_tot)

#error for calculation coefficients
d_A = np.sqrt( ( 1/sum_coin[0] * d_tot[1] )**2 + ( -A/sum_coin[0] * d_tot[0])**2 )
d_B = np.sqrt( ( 1/sum_coin[0] * d_tot[2] )**2 + ( -B/sum_coin[0] * d_tot[0])**2 )

delta_a		= np.zeros(2)
delta_a[1]	= np.sqrt( ( -4*d_A )**2 + ( 2*d_B )**2 )	#gaussian error propagation for coefficients
delta_a[0]	= np.sqrt( ( 4*d_A )**2 + ( -d_B )**2 )		#gaussian error propagation for coefficients
delta_An	= d_B										#gaussian error propagation for anisotropy

print('------------------FIRST METHOD --------------------------\na2 = %.3f +/- %.4f, a4 = %.3f +/- %.4f, An = %.3f +/- %.4f' %(a[0], delta_a[0], a[1], delta_a[1], An, delta_An))

#relative deviations
theo_a	= np.array([1/8, 1/24])
theo_An	= 0.167

rel_a	= np.abs(theo_a - a)/theo_a * 100
rel_An	= np.abs(theo_An - An)/theo_An * 100

print('\nrelative deviations: a2_rel = %.2f%%, a4_rel = %.2f%%, An_rel = %.2f%%\n' %(rel_a[0], rel_a[1], rel_An))
###------- FIRST METHOD END-----------------------------------------------------

###--------SECOND METHOD -------------------------------------------------------
coin	= np.zeros(shape=(6, 3))

#slice red. coincidences per measurement series
for i in range(0,6):
	for j in range(0,3):
		coin[i][j] = red_coin[i+6*j]

#coefficients for calculation of correlation function coeff.
A	= np.zeros(6)
B	= np.zeros(6)
An	= np.zeros(6)

for i in range(0, 6):
	A[i] = coin[i][1]/coin[i][0]
	B[i] = coin[i][2]/coin[i][0]

#correlation function coeff.
a2 = 4*A - B - 3
a4 = 2*(1 + B - 2*A)
An = B-1

#mean over those
a2_val = np.mean(a2)
a4_val = np.mean(a4)
An_val = np.mean(An)

##ERROR CALCULATION
#slice delta red. coincidences per measurement series
d_coin = np.zeros(shape=(6,3))
for i in range(0,6):
	for j in range(0,3):
		d_coin[i][j] = d_red_coin[i+6*j]

#errors for calculation coefficients
d_A		= np.zeros(6)
d_B		= np.zeros(6)
d_An	= np.zeros(6)

for i in range(0,6):
	d_A[i] = np.sqrt( ( 1/coin[i][0] * d_coin[i][1] )**2 + ( -A[i]/coin[i][0] * d_coin[i][0] )**2 )	#gaussian error propagation for coefficients
	d_B[i] = np.sqrt( ( 1/coin[i][0] * d_coin[i][2] )**2 + ( -B[i]/coin[i][0] * d_coin[i][0] )**2 )	#gaussian error propagation for coefficients

#errors for correlation coefficients
d_a = np.zeros(shape=(2, 6))
d_An = d_B	#gaussian error propagation for anisotropy
d_a[1]	= np.sqrt( ( -4*d_A )**2 + ( 2*d_B )**2 )	#gaussian error propagation for coefficients
d_a[0]	= np.sqrt( ( 4*d_A )**2 + ( -d_B )**2 )		#gaussian error propagation for coefficients

#errors for means of correlation coefficients
d_means = np.zeros(3)

d_means[0] = np.std(a2)/np.sqrt(6)
d_means[1] = np.std(a4)/np.sqrt(6)
d_means[2] = np.std(An)/np.sqrt(6)

#errors from mean propagation
d_prop = np.zeros(3)

for i in range(0,2):
	for j in range(0,6):
		d_prop[i] = d_prop[i] + d_a[i][j]**2

for j in range(0,6):
	d_prop[2] = d_prop[2] + d_An[j]**2

d_prop = np.sqrt((1/6)*d_tot)

print('------------------SECOND METHOD -----------------------\na2 = %.3f +/- %.7f(sys.) +/- %.4f(stat.), a4 = %.3f +/- %.7f(sys.) +/- %.4f(stat.), An = %.3f +/- %.7f(sys.) +/- %.4f(stat.)' %(a2_val, d_prop[0], d_means[0], a4_val, d_prop[1], d_means[1], An_val, d_prop[2], d_means[2]))

rel_a2	= np.abs(theo_a[0] - a2_val)/theo_a[0] * 100
rel_a4	= np.abs(theo_a[1] - a4_val)/theo_a[1] * 100
rel_An	= np.abs(theo_An - An_val)/theo_An * 100

print('\nrelative deviations: a2_rel = %.2f%%, a4_rel = %.2f%%, An_rel = %.2f%%\n' %(rel_a2, rel_a4, rel_An))
###--------SECOND METHOD END ---------------------------------------------------
