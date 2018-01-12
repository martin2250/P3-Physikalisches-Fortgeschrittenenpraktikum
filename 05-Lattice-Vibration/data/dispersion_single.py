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
a  = L/(n+1) 	#lattice parameter NOTE: Error calculation needed.
m = 0.504	#mass of atoms

if len(sys.argv) != 2:
	quit('Usage: ./dispersion_single.py <save|show>')

""" path to source and plots """
plot_path = os.path.join(os.path.dirname(__file__), 'plots')
data_path = os.path.join(os.path.dirname(__file__), 'source')

""" measurement series """
data_list = []

for i in range(N):
	filename = 'a1-a-{:0>2d}.lvm'.format(i+1)
	path = os.path.join(data_path, filename)
	data_list.append(np.loadtxt(path, unpack=False, usecols=(1,2)))

""" statistics """
data = 2*np.pi*np.dstack(tuple(data_list))	#convert frequencies to angular frequencies

mean_data_each_glider = np.mean(data, axis=2)							#mean of frequencies (each glider)
mean_data_gliders = np.mean(mean_data_each_glider, axis=1)				#mean of glider 1 and 2

stds_each_glider = np.std(data, axis=2)									#standard deviations (each glider)
mean_errors_each_glider = stds_each_glider / np.sqrt(len(data_list))	#statistical errors on mean values (each glider)

stat_error_propagated = np.sqrt(1 / 2. * np.sum(mean_errors_each_glider**2, axis=1))	#propagated mean error from previous averaging

""" theoretical curve """
def dispersion(k, D):
	return np.sqrt(4 * D / m) * np.abs(np.sin(k * a / 2))

""" plot """
k = np.array([(i+1) * np.pi / (n+1) / a for i in range(n)])
k_lin = np.linspace(0, np.pi/a, 1000)

plt.errorbar(k, mean_data_gliders, yerr=stat_error_propagated, fmt='o', label='data')
plt.xlabel('$k$ in $\\frac{1}{m}$')
plt.ylabel('$\\omega (k)$ in $\\frac{1}{s}$')
plt.axvline(x=np.pi/a, color='g')	#mark end of first brillouin zone

""" fit of dispersion relation """
D, pcov = scipy.optimize.curve_fit(dispersion, k, mean_data_gliders)	#fit curve
Derr = np.sqrt(np.diag(pcov))	#standard deviation on parameter
plt.plot(k_lin, dispersion(k_lin, D), label='$\\omega(k) =\\sqrt{\\frac{4D}{m}}\\left|\\sin\\left(\\frac{ka}{2}\\right)\\right|$')

chi2 = np.sum( (dispersion(k, D) - mean_data_gliders)**2 ) / (len(mean_data_gliders) - 1)	#perform reduced chi2 test

plt.legend()

"""The Speed of Sound(,the First of Her Name, The Unburnt, Queen of the Andals, the Rhoynar and the First Men, Queen of Meereen,
Khaleesi of the Great Grass Sea, Protector of the Realm, Lady Regnant of the Seven Kingdoms, Breaker of Chains and Mother of Dragons """
dw = mean_data_gliders[1]-mean_data_gliders[0]
dk = np.pi / (n+1) / a
v_s = dw/dk	# NOTE: Error calculation needed.

""" Stiffness (hehe) """
D2 =m / a / a * v_s**2	# NOTE: Error calculation needed.

if sys.argv[1] == 'save':
	plt.savefig(os.path.join(plot_path, 'dispersion_single.pdf'))
elif sys.argv[1] == 'show':
	print('\nExercise 1:\nlattice parameter: a = %.5f, end of first Brillouin zone: k_end = %.5f' %(a, np.pi/a))
	print('Exercise 2:\nv_s = %.4f' %v_s)
	print('Exercise 4:\n D_1 = %.4f +/- %.6f (goodness of fit: chi2 = %.3f), D_2 = %.4f' %(D, Derr, chi2, D2))
	plt.show()
