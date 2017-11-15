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
dE = 1*np.ones(d.shape)			# 1mm error for d

Y = np.log(d**2 * wo)
YE = np.sqrt(
	(1/(d**2 * wo) * woE)**2 +		# error on count
	(2*d/(d**2 * wo) * dE)**2)			# error on d

if len(sys.argv) <= 2:
	import kafe
	from kafe.function_library import linear_2par

	dataset = kafe.Dataset(data=(d, Y))
	dataset.add_error_source('y', 'simple', YE)		# poisson error for y
	dataset.add_error_source('x', 'simple', dE)		# poisson error for y

	fit = kafe.Fit(dataset, linear_2par)
	fit.do_fit(quiet=True)

	slope = fit.final_parameter_values[0]
	slopeE = fit.final_parameter_errors[0]
	yoffset = fit.final_parameter_values[1]

	os.execv(__file__, ['test', str(slope), str(slopeE), str(yoffset), 'save' if len(sys.argv) == 2 else 'show'])

else:
	slope = float(sys.argv[1])
	slopeE = float(sys.argv[2])
	yoffset = float(sys.argv[3])

	relaxlength = -1/slope
	relaxlengthE = slopeE/slope**2

	print('relaxation length:', relaxlength, '+-', relaxlengthE, 'mm')


	plt.errorbar(d, Y, fmt='o', yerr=YE, label='$\\log(d^2 \cdot N)$')

	linX = np.array([d[0], d[-1]])
	plt.plot(linX, slope * linX + yoffset, label='$-\\frac{d}{\\lambda} + c$, $\\lambda = %0.1f \pm %0.1f$mm'%(relaxlength, relaxlengthE))

	plt.xlabel('distance from  source $d$ (mm)')
	plt.ylabel('$\\log(d^2 \\cdot N)$')

	#plt.text(150, 13.4, 'test')

	plt.grid(True)
	plt.legend()

	if sys.argv[4] == 'save':
		plt.savefig('plots/relax.pdf')
	else:
		plt.show()
