#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import sys

N = 12

A = np.zeros(N)
B = np.zeros(N)
dA = np.zeros(N)
dB = np.zeros(N)
R = np.zeros(N)
dR = np.zeros(N)

stuff,freqs, morestuff = np.loadtxt('source/a1-b-01.lvm', unpack=True)

for i in range(N):
	a, b = np.loadtxt('source/a2-n{:02d}.lvm'.format((i + 1)), unpack=True)

	a = a[1:] #discard first value
	b = b[1:]

	A[i] = np.mean(a)
	B[i] = np.mean(b)

	dA[i] = np.std(a) / np.sqrt(len(A))
	dB[i] = np.std(b) / np.sqrt(len(A))

	ratio = b/a

	r = np.mean(ratio)

	f = np.sin(np.pi/13 * 5 * (i + 1))/np.sin(np.pi/13 * 6 * (i + 1))

	r *= f

	# if it's stupid and it works it ain't stupid
	if i < 6:
		if r < 0:
			r = -r
	else:
		if r > 0:
			r = -r

	R[i] = r
	dR[i] = np.abs(np.std(b/a)*f) / np.sqrt(len(R))

half = int(N/2)
x = np.pi*np.arange(1, half + 1)/(half)

xacou = x
xopt = x[::-1]

Ra = R[0:half]
Ro = R[half:N]

plt.errorbar(xacou, Ra, yerr=dR[:half], label='todo', fmt='ro')
plt.errorbar(xopt, Ro, yerr=dR[half:N], fmt='ro')

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

popta, pconva = scipy.optimize.curve_fit(acoustic, xacou[:-1], Ra[:-1],p0=(1.6))
popto, pconvo = scipy.optimize.curve_fit(optic, xopt[1:], Ro[1:], p0=(1.4), bounds=(1, 2))
print(popta, popto)

X = np.linspace(x[0], x[-1], 100)[:-1]	#discard singularity
plt.plot(X, acoustic(X, *popta))
plt.plot(X, optic(X, *popto))

plt.ylim(-6, 2)
plt.xlim(np.pi/6 - 0.1, np.pi + 0.1)

ticks = np.arange(1, half + 1)*np.pi/half
plt.xticks(ticks, ['$%d\\pi/6$'%h for h in np.arange(1, half + 1)])

plt.legend()
plt.grid(True)

if len(sys.argv) < 2:
	plt.show()
elif sys.argv[1] == "table":
	for i in range(N):
		print('{:2d}&\t{:=1.3f}&\t{:=6.1f} \\pm {:=4.1f}&\t{:=6.1f} \\pm {:=4.1f}&\t{:=+1.2f} \\pm {:=1.2f}\\\\'.format(i+1, freqs[i], A[i], dA[i], B[i], dB[i], R[i], dR[i]))
else:
	plt.savefig(sys.argv[1])
