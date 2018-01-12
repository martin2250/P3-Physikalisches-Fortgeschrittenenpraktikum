#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import sys

#todo: replace with mean
stuff,omegas, morestuff = np.loadtxt('source/a1-b-01.lvm', unpack=True)

N = 12
for i in range(N):
	a, b = np.loadtxt('source/a2-n{:02d}.lvm'.format((i + 1)), unpack=True)
	ratio = a / b

	r = np.mean(ratio)

	f = np.sin(np.pi/13 * 5 * (i + 1))/np.sin(np.pi/13 * 6 * (i + 1))


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

	print('{:2d}&\t{:=1.3f}&\t{:=6.1f}&\t{:=6.1f}&\t{:=+1.2f}\\\\'.format(i+1, omegas[i], np.mean(a), np.mean(b), r))
