#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import scipy.optimize

N  = 4		#number of measurements carried out
L  = 5.5035	#length of chain
dL = 0.001	#error on chain length
n  = 12		#number of atoms in chain
a = 2 * L / (n+1)	#lattice parameter NOTE: Error calculation needed.
vs_single = 3.0132	#speed of sound in single chain, obtained by executing first script
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
k = np.array([(i+1) * np.pi / ((n+1) / 2) / a for i in range(max_modes)])
k_lin = np.linspace(0, np.pi/a, 1000)

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
dk = np.pi / ((n+1) /2) / a
v_s = dw/dk	# NOTE: Error calculation needed.

""" Mass ratio """
ratio = 2 * vs_single / v_s - 1

M = m * ratio

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

plt.legend()

""" Stiffness (hehe) """
D_double = 2*(m + M) / a / a * v_s**2	# NOTE: Error calculation needed.

if sys.argv[1] == 'save':
	plt.savefig(os.path.join(plot_path, 'dispersion_alternating.pdf'))
elif sys.argv[1] == 'show':
	print('\nExercise 1:\nlattice parameter: a = %.5f, end of first Brillouin zone: k_end = %.5f' %(a, np.pi/a))
	print('Exercise 2:\nv_s = %.4f' %v_s)
	print('Exercise 3:\n M/m = %.4f, --> M = %.4f' %(ratio, M))
	print('Exercise 4_ac:\n D_ac = %.4f +/- %.6f (goodness of fit: chi2 = %.3f), D_s = %.4f' %(D1, D1err, chi2_1, D_double))
	print('Exercise 4_opt:\n D_opt = %.4f +/- %.6f (goodness of fit: chi2 = %.3f), D_s = %.4f' %(D2, D2err, chi2_2, D_double))
	plt.show()
