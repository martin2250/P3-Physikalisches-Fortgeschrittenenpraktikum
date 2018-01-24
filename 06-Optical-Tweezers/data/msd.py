#!/usr/bin/python
import numpy as np
import sys
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
	print('dumbass')
	exit(1)

pxtomm = (0.7578 - 0.6437)/2**10

data = np.loadtxt(sys.argv[1], delimiter=',', skiprows=1).T

data[2:3] = data[2:3] * pxtomm

n = int(np.max(data[1])) + 1
N = int(np.max(data[0])) + 1
print('found %d trackers in %d frames'%(n, N))

R2 = np.zeros(n)

for i in range(n):
	X = data[2, i:i+N*n:n]
	Y = data[3, i:i+N*n:n]

	if False:
		plt.plot(X, Y)
		plt.show()

	x0 = np.mean(X)
	y0 = np.mean(Y)

	R2[i] = np.sum((X - x0)**2 + (Y - y0)**2) / N

print("mean displacement (mm^2):", R2)
print("mean mean displacement (mm^2):", np.mean(R2))
