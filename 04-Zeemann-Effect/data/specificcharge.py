#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

wvlength = np.empty((0, 2))
B = np.arange(5, 10)/10

for b in B:
	peaks, intensity = np.loadtxt('external/667.8nm_f1_%0.1fT.peaks'%b, unpack=True, skiprows=2)
	wvlength = np.append(wvlength, [peaks], axis=0)

#second order
wvlength *= 1e-10 / 2

La1 = wvlength[:,1]
La2 = wvlength[:,0]

c = 299792458
h = 6.6261-34

K = c*(2*np.pi)*(1/La1 - 1/La2)/(B)

for (b, la1, la2, k) in zip(B, La1, La2, K):
	print(b, la1, la2, k)
