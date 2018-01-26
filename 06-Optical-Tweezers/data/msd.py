#!/usr/bin/python
import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy.optimize

if len(sys.argv) < 2:
	print('dumbass')
	exit(1)

pxtomm = (0.7578 - 0.6437)/2**10

data = np.loadtxt(sys.argv[1], delimiter=',', skiprows=1).T

data[2:3] = data[2:3] * pxtomm

n = int(np.max(data[1])) + 1
N = int(np.max(data[0])) + 1
print('found %d trackers in %d frames'%(n, N))

R2 = np.zeros(N)
T = np.arange(N)/13	#13 fps

for ti in range(1, N):
	for i in range(n):
		X = data[2, i:i+ti*n:n]
		Y = data[3, i:i+ti*n:n]

		R2[ti] += np.sum((X - X[0])**2 + (Y - Y[0])**2) / (ti * n)


plt.plot(T, R2)
plt.xlabel('time $t$ (s)')
plt.ylabel('mean square displacement $\\langle r^2\\rangle$ (mm)')

def lin(x, a, b):
	return x*a + b

popt, pcov = scipy.optimize.curve_fit(lin, T, R2)

print(popt)


if len(sys.argv) < 3:
	plt.show()
else:
	plt.savefig(sys.argv[2])
