#!/usr/bin/python
from __future__ import division, print_function
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

# Martin Pittermann, October 2017
# processes data.npz files and shows the histogram of the correlation/energy spectrum

if len(sys.argv) != 4:
	print('usage: %s data.npz [energy/correlation] [bins]'%sys.argv[0])
	exit(1)

npz = np.load(sys.argv[1])
E = npz['power']
T = npz['time_delta'] #convert to nanoseconds (x8ns)
npz.close()

bins = int(sys.argv[3])

if sys.argv[2] == 'energy':
	D = np.append(E[:,0], E[:,1])

	histr = (800, 10000)
	hist = scipy.stats.histogram(D, bins, histr).count

	X = np.linspace(histr[0], histr[1], bins, endpoint=False)

	if False:
		f = open('energyspectrum.dat', 'w')
		for (x, y) in zip(X, hist):
			f.write('%0.0f\t%d\n'%(x, y))
		f.close()

	plt.plot(X, hist)
	plt.show()

elif sys.argv[2] == 'correlation':
	energythreshold = 6e3
	timethreshold = 50
	D = [d for (d, e1, e2) in zip(T, E[:,0], E[:,1]) if min(e1, e2) > energythreshold and abs(d) < timethreshold]
	print(len(D), 'events with sufficient energy')

	plt.hist(D, bins=50, range=(-200,200))

else:
	print('second argument not recognized')

plt.show()
