#!/usr/bin/python
from __future__ import division, print_function
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

# Martin Pittermann, October 2017
# analyze data.npz files
# extracts:
# - total number of events channel 1
# - total number of events channel 2
# - number of correlated events
# - number of correlated events with time offset (random coincidences)

energythreshold = 3700	#this is so wrong
correlationthreshold = 100
randomoffset = 300

if len(sys.argv) == 1:
	print('usage: %s [data1.npz] [data2.npz] ...'%sys.argv[0])
	print('writes output to result.dat')
	exit(1)

output = open('result.dat', 'w')

output.write('# e-thresh: %d\n'%energythreshold)
output.write('# t-thresh: %dns\n'%correlationthreshold)
output.write('# random-offset: %dns\n'%randomoffset)

for fname in sys.argv[1:]:
	print('analyzing %s'%fname)

	npz = np.load(fname)
	E = npz['power']
	T = npz['time_delta'] * 8
	npz.close()

	ev1 = 0	# events ch1
	ev2 = 0	# events ch2
	correl = 0	# correlations
	coinc = 0	# random coincidences

	for (e, t) in zip(E, T):
		evt = True	# both channels recorded events

		if e[0] > energythreshold:
			ev1 += 1
		else:
			evt = False

		if e[1] > energythreshold:
			ev2 += 1
		else:
			evt = False

		if evt:
			if np.abs(t) < correlationthreshold:
				correl += 1
			if np.abs(t - randomoffset) < correlationthreshold:
				coinc += 1

	outputline = '%s\t%d\t%d\t%d\t%d\n'%(fname, ev1, ev2, correl, coinc)
	print(outputline)
	output.write(outputline)

output.close()
