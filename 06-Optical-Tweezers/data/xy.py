#!/usr/bin/python
import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy.optimize

if len(sys.argv) < 3:
	print('dumbass')
	exit(1)

pxtoum = 1e3*(0.7578 - 0.6437)/2**10
data = np.loadtxt(sys.argv[1], delimiter=',').T

N = int(np.max(data[0])) + 1
n = int(data.shape[1] / N)
print('found %d trackers in %d frames'%(n, N))

data = data * pxtoum
X = data[1].reshape((n, N))
Y = data[2].reshape((n, N))

#try this:
if False:
	X = X[1]
	Y = Y[1]

if False:
	#use means
	X = X - np.outer(np.mean(X, axis=1), np.ones(N))
	Y = Y - np.outer(np.mean(Y, axis=1), np.ones(N))
else:
	X = X - np.outer(X[:,10], np.ones(N))
	Y = Y - np.outer(Y[:,10], np.ones(N))


if sys.argv[2] == 'distrib':
	size = 0.5
	for i in range(n):
		plt.plot(X, Y, '+', color='red', markersize=1)
		plt.xlim(-size, size)
		plt.ylim(-size, size)

	plt.xlabel('position X ($\mu m$)')
	plt.ylabel('position Y ($\mu m$)')

elif sys.argv[2] == 'hist2d':
	size = 0.2
	plt.hist2d(X.flatten(), Y.flatten(), bins=40, range=((-size, size),(-size, size)))

	plt.xlabel('position X ($\mu m$)')
	plt.ylabel('position Y ($\mu m$)')

elif sys.argv[2] == 'msd':
	R2 = np.zeros(N - 1)
	T = np.arange(len(R2))/13	#13 fps

	for t in range(10, N):
		R2[t-1] = np.sum(X[:,:t].flatten()**2 + Y[:,:t].flatten()**2) / (n*t)

	def lin(x, a, b):
		return x*a + b
	popt, pcov = scipy.optimize.curve_fit(lin, T, R2)
	print('m = %0.3e um^2/s'%popt[0])

	plt.plot(T, R2)
	plt.plot(T, lin(T, *popt),label='linear fit\n$m \\cdot t + c$')
	plt.xlabel('time $t$ (s)')
	plt.ylabel('mean square displacement $\\langle r^2\\rangle$ ($\mu m^2$)')
	plt.legend()

elif sys.argv[2] == 'gaussian':
	X = X.flatten()
	Y = Y.flatten()
	R2 = X**2 + Y**2

	def gauss(r2, sigma):
		return 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-0.5*(r2/(sigma**2)))

	def neglikelihood(sigma, offset):
		return offset-np.sum(np.log(gauss(R2,sigma)))

	sigma_0 = scipy.optimize.minimize(neglikelihood, x0=(1), args=(0), bounds=[(0.01, 10)]).x

	offset = -neglikelihood(sigma_0, 0)

	left = scipy.optimize.root(neglikelihood, x0=(sigma_0 / 2), args=(offset - 0.5)).x
	right = scipy.optimize.root(neglikelihood, x0=(3*sigma_0 / 2), args=(offset - 0.5)).x

	print('sigma_0 = %0.4f [%0.4f, %0.4f]  (68%% confidence)'%(sigma_0, left, right))

	X = np.linspace(left, right, 100)
	Y = [neglikelihood(x, offset) for x in X]

	plt.plot(X, Y)
	plt.show()



if len(sys.argv) < 4:
	plt.show()
else:
	plt.savefig(sys.argv[3])
