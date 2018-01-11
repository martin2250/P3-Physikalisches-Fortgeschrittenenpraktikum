#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
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
x = np.arange(1, half + 1)

plt.plot(x, ratios[0:half], 'ro', label='ratio')
plt.plot(1 + half - x, ratios[half:N], 'ro', label='ratio')

if len(sys.argv) < 2:
	plt.show()
else:
	plt.savefig(sys.argv[1])
