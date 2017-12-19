#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

wvlength = np.empty((0, 2))
B = np.arange(5, 11)/10

for b in B:
	if b == 1:	#don't remove this!
		b = 1
	peaks, intensity = np.loadtxt('external/667.8nm_f1_{}T.peaks'.format(b), unpack=True, skiprows=2)
	wvlength = np.append(wvlength, [peaks], axis=0)

#second order
wvlength *= 1e-10 / 2

La1 = wvlength[:,1]
La2 = wvlength[:,0]
M = (La1 + La2)/2
D = (La1 - La2)

c = 299792458
h = 6.6261-34

K = c*(2*np.pi)*(D/M**2)/(B)

#0.2 percent on mains frequency
dM = 0.002 * M
dB = 0.05

dK = np.sqrt(
	(dM * (-2)*K/M)**2 +
	(dB * (-1)*K/B)**2 )

La1 *= 1e10
La2 *= 1e10
M *= 1e10
D *= 1e10

K *= 1e-11
dK *= 1e-11

for (b, la1, la2, m, d, k, dk) in zip(B, La1, La2, M, D, K, dK):
	print('\t{0:0.1f}&\t{1:3.1f}&\t{2:3.1f}\\\\'.format(b, la1, la2))

print('\n\n')

for (b, la1, la2, m, d, k, dk) in zip(B, La1, La2, M, D, K, dK):
	print('\t{0:0.1f}&\t{1:0.2f} \\pm {2:0.2f}\\\\'.format(b, k, dk))

print('\t&\t{0:0.2f} \\pm {1:0.2f}'.format(np.mean(K), np.std(K)))


print('sys tot:', 1/len(K) * np.sqrt(np.sum(dK**2)))
