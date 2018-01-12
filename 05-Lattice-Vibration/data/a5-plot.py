#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import sys

N = 12

ratios = np.zeros(N)
rawratios = np.zeros(N)
correctionfactor = np.zeros(N)

for i in range(N):
	a, b = np.loadtxt('source/a2-n{:02d}.lvm'.format((i + 1)), unpack=True)
	ratio = a / b

	r = np.mean(ratio)
	rawratios[i] = r

	f = np.sin(np.pi/13 * 5 * (i + 1))/np.sin(np.pi/13 * 6 * (i + 1))
	correctionfactor[i] = f

	r /= f

	# if it's stupid and it works it ain't stupid
	if i < 6:
		if r < 0:
			r = -r
		if r > 1.:
			r = 1/r
	else:
		if r > 0:
			r = -r
		r = 1/r

	ratios[i] = r

half = int(N/2)
x = np.pi*np.arange(1, half + 1)/(half)

xacou = x
xopt = x[::-1]
ratioa = ratios[0:half]
ratioo = ratios[half:N]

plt.plot(xacou, ratioa , 'ro', label='ratio')
plt.plot(xopt, ratioo, 'ro', label='ratio')

# theoretical amplitude ratio, ka: wavenumber*lattice constant, ga: mass ratio, pm: plus or minus one (optic or acoustic)
def tratio(ka, ga, pm):
	num = np.cos(ka/2)
	sq = 1 - 4*ga/(1 + ga)**2*np.sin(ka/2)**2
	denom = 1 - (1+ga)/(2*ga)*(1 + pm*np.sqrt(sq))
	return num/denom

def acoustic(ka, ga):
	return tratio(ka, ga, -1)

def optic(ka, ga):
	return tratio(ka, ga, 1)

popta, pconva = scipy.optimize.curve_fit(acoustic, xacou, ratioa,p0=(1.6))
popto, pconvo = scipy.optimize.curve_fit(optic, xopt[:-1], ratioo[:-1], p0=(1.4))
print(popta, popto)

X = np.linspace(x[0], x[-1], 100)
plt.plot(X, acoustic(X, *popta))
plt.plot(X, optic(X, *popto))

plt.ylim(-6, 2)
plt.grid(True)

if len(sys.argv) < 2:
	plt.show()
else:
	plt.savefig(sys.argv[1])
