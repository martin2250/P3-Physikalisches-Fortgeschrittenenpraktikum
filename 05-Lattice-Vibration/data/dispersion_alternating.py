#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import scipy.optimize

N  = 4		#number of measurements carried out
n  = 12		#number of atoms in chain

L  = 5.035		#length of chain
L_err = 0.01	#systematic error on chain length

a = 2 * L / n			#lattice parameter
a_err = 2 * L_err / n	#systematic error on lattice parameter

vs_single = 3.0132		#speed of sound in single chain, obtained by executing first script
vs_single_err = 0.00572	#error on sound in single chain, obtained by executing first script

m = 0.504	#small mass
max_modes = 6	#number of possible modes per branch

if len(sys.argv) != 2:
	quit('Usage: ./dispersion_alternating.py <save|show>')

""" path to source and plots """
plot_path = os.path.join(os.path.dirname(__file__), 'plots')
data_path = os.path.join(os.path.dirname(__file__), 'source')

""" measurement series """
data_list = []

for i in range(N):
	filename = 'a1-b-{:0>2d}.lvm'.format(i+1)
	path = os.path.join(data_path, filename)
	data_list.append(np.loadtxt(path, unpack=False, usecols=(1,2)))

""" statistics """
data = 2*np.pi*np.dstack(tuple(data_list))	#convert frequencies to angular frequencies

mean_data_each_glider = np.mean(data, axis=2)							#mean of frequencies (each glider)
mean_data_gliders = np.mean(mean_data_each_glider, axis=1)				#mean of glider 1 and 2

stds_each_glider = np.std(data, axis=2)									#standard deviations (each glider)
mean_errors_each_glider = stds_each_glider / np.sqrt(len(data_list))	#statistical errors on mean values (each glider)

stat_error_propagated = np.sqrt(1 / 2. * np.sum(mean_errors_each_glider**2, axis=1))	#propagated mean error from previous averaging

""" plot """
k = np.array([(i+1) * np.pi / (n / 2) / a for i in range(max_modes)])
k_lin = np.linspace(0, np.pi/a, 1000)
k_end_err = np.pi / a**2 * a_err	#gaussian error propagation

ac_branch = mean_data_gliders[:6]
opt_branch = np.flip(mean_data_gliders[6:], 0)

ac_branch_errors = stat_error_propagated[:6]
opt_branch_errors = np.flip(stat_error_propagated[6:], 0)


plt.errorbar(k, opt_branch, yerr=opt_branch_errors, fmt='o', label='data: optical branch')
plt.errorbar(k, ac_branch, yerr=ac_branch_errors, fmt='o', label='data: acoustic branch')
plt.xlabel('$k$ in $\\frac{1}{m}$')
plt.ylabel('$\\omega (k)$ in $\\frac{1}{s}$')
plt.axvline(x=np.pi/a, color='g')	#mark end of first brillouin zone

"""The Speed of Sound(,the First of Her Name, The Unburnt, Queen of the Andals, the Rhoynar and the First Men, Queen of Meereen,
Khaleesi of the Great Grass Sea, Protector of the Realm, Lady Regnant of the Seven Kingdoms, Breaker of Chains and Mother of Dragons """
dw = ac_branch[0]
dk = np.pi / (n /2) / a
v_s = dw/dk
v_s_err = np.sqrt((1/dk)**2 * ac_branch_errors[0]**2 + (dw * n / np.pi / 2)**2 * a_err**2)	#gaussian error propagation

""" Mass ratio """
ratio = 2 * vs_single / v_s - 1
ratio_err = np.sqrt( (2 / v_s)**2 * vs_single_err**2 + (2 * vs_single / v_s**2)**2 * v_s_err**2 )	#gaussian error propagation

M = m * ratio
M_err = m * ratio_err

""" theoretical curve """
def dispersion_minus(x, D):
	mu = ( 1. / m ) + ( 1. / M )
	return np.sqrt(D * mu - D * np.sqrt(mu**2 - 4 / (m*M) * np.sin(x * a /2)**2))

def dispersion_plus(x, D):
	mu = ( 1. / m ) + ( 1. / M )
	return np.sqrt(D * mu + D * np.sqrt(mu**2 - 4 / (m*M) * np.sin(x * a /2)**2))

""" fit of dispersion relation """
D1, pcov = scipy.optimize.curve_fit(dispersion_minus, k, ac_branch)	#fit curve
D1err = np.sqrt(np.diag(pcov))	#standard deviation on parameter
plt.plot(k_lin, dispersion_minus(k_lin, D1), label='fit: $\\omega_{-}$')

chi2_1 = np.sum( (dispersion_minus(k, D1) - ac_branch)**2 ) / (len(ac_branch) - 1)	#perform reduced chi2 test

D2, pcov = scipy.optimize.curve_fit(dispersion_plus, k, opt_branch)	#fit curve
D2err = np.sqrt(np.diag(pcov))	#standard deviation on parameter
plt.plot(k_lin, dispersion_plus(k_lin, D2), label='fit: $\\omega_{+}$')

chi2_2 = np.sum( (dispersion_plus(k, D2) - opt_branch)**2 ) / (len(opt_branch) - 1)	#perform reduced chi2 test

D_mean = (D1 + D2) / 2
D_mean_err = np.std([D1, D2])/np.sqrt(2)
D_prop_err = np.sqrt(np.sum(0.25*np.square([D1err, D2err])))

plt.legend()

""" Stiffness (hehe) """
D_double = 2*(m + M) / a**2 * v_s**2
D_double_err = np.sqrt( (2*v_s**2 / a**2)**2 * M_err**2
+ (4*(m + M)*v_s / a**2)**2 * v_s_err**2
+ (4*(m + M)*v_s**2 / a**3)**2 * a_err**2 )	#gaussian error propagation

if sys.argv[1] == 'save':
	plt.savefig(os.path.join(plot_path, 'dispersion_alternating_data.pdf'))
elif sys.argv[1] == 'show':
	print('\nExercise 1:\nlattice parameter: a = %.5f +/- %.6f, end of first Brillouin zone: k_end = %.5f +/- %.6f' %(a, a_err, np.pi/a, k_end_err))
	print('Exercise 2:\nv_s = %.4f +/- %.5f' %(v_s, v_s_err))
	print('Exercise 3:\n M/m = %.4f +/- %.5f, --> M = %.4f +/- %.5f' %(ratio, ratio_err, M, M_err))
	print('Exercise 4_ac:\n D_ac = %.4f +/- %.6f (goodness of fit: chi2 = %.3f), D_s = %.4f +/- %.5f' %(D1, D1err, chi2_1, D_double, D_double_err))
	print('Exercise 4_opt:\n D_opt = %.4f +/- %.6f (goodness of fit: chi2 = %.3f), D_s = %.4f +/- %.5f' %(D2, D2err, chi2_2, D_double, D_double_err))
	print('Exercise 4_mean:\n D_mean = %.4f +/- %.6f (std) +/- %.6f (stat)' %(D_mean, D_mean_err, D_prop_err))
	plt.show()
