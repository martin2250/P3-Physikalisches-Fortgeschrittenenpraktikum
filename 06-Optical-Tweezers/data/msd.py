#!/usr/bin/python
import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy.optimize

if len(sys.argv) < 2:
	print('dumbass')
	exit(1)

pxtoum = (0.7578e3 - 0.6437)/2**10

if 'blender' in sys.argv[1]:
	data = np.loadtxt(sys.argv[1], delimiter=',', skiprows=1).T

	N = int(np.max(data[0])) + 1
	n = int(data.shape[1] / N) + 1
	print('found %d trackers in %d frames'%(n, N))

	startN = 80

	data = data * pxtoum
	R2 = np.zeros(N - 1 - startN)
	T = np.arange(N - 1 - startN)/13	#13 fps

	for ti in range(startN + 1, N):
		for i in range(n):
			X = data[1, i*N + startN:i*N+ti]
			Y = data[2, i*N + startN:i*N+ti]

		#	if ti==N-1:
			#	print(X - X[0])

			R2[ti - startN - 1] += np.sum((X - np.mean(X))**2 + (Y - np.mean(Y))**2) / (ti * n)
else:
	data = np.loadtxt(sys.argv[1], delimiter=',', skiprows=1).T
	data[2:3] = data[2:3] * pxtoum

	n = int(np.max(data[1])) + 1
	N = int(np.max(data[0])) + 1
	print('found %d trackers in %d frames'%(n, N))

	R2 = np.zeros(N)
	T = np.arange(N)/13	#13 fps

	for ti in range(1, N):
		for i in [0, 1, 2]:#range(n):
			X = data[2, i:i+ti*n:n]
			Y = data[3, i:i+ti*n:n]

			R2[ti] += np.sum((X - X[0])**2 + (Y - Y[0])**2) / (ti * n)


plt.plot(T, R2, label='data')

def lin(x, a, b):
	return x*a + b
popt, pcov = scipy.optimize.curve_fit(lin, T, R2)
print('m = %0.3e um^2/s'%popt[0])

plt.plot(T, lin(T, *popt),label='linear fit\n$m \\cdot t + c$')
# plt.text(18, 0.13, '$m = %0.3e$'%popt[0])

if False:
	ax2 = plt.gca().twinx()
	ax2.plot(T[:-1], R2[1:] - R2[:-1], '+', label='instantaneous displacement')

plt.xlabel('time $t$ (s)')
plt.ylabel('mean square displacement $\\langle r^2\\rangle$ ($\mu m^2$)')
plt.legend()

if len(sys.argv) < 3:
	plt.show()
else:
	plt.savefig(sys.argv[2])
