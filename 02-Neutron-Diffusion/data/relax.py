#!/usr/bin/python
from __future__ import division, print_function
import sys
import numpy as np
import matplotlib.pyplot as plt
import os

#distance, count without Cd, count with Cd
d, wo, w = np.loadtxt('values.dat', unpack=True)
woE = np.sqrt(wo)	# poisson error for series without Cd shield
wE = np.sqrt(w)


Y = np.log(d**2 * wo)
YE = 1/(d**2 * wo) * woE

if len(sys.argv) == 1:
	import kafe
	from kafe.function_library import linear_2par

	dataset = kafe.Dataset(data=(d, Y))
	dataset.add_error_source('y', 'simple', YE)		# poisson error for y

	fit = kafe.Fit(dataset, linear_2par)
	fit.do_fit(quiet=True)

	slope = fit.final_parameter_values[0]
	slopeE = fit.final_parameter_errors[0]
	yoffset = fit.final_parameter_values[1]

	print(slope, slopeE)

	os.execv(__file__, ['test', str(slope), str(slopeE), str(yoffset)])

else:
	print(sys.argv)
	slope = float(sys.argv[1])
	slopeE = float(sys.argv[2])
	yoffset = float(sys.argv[3])


	plt.errorbar(d, Y, yerr=YE)

	linX = np.array([d[0], d[-1]])
	plt.plot(linX, slope * linX + yoffset)
	plt.show()
