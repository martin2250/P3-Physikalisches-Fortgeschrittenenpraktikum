#!/usr/bin/python
from __future__ import division, print_function
import sys
import numpy as np
import matplotlib.pyplot as plt

#distance, count without Cd, count with Cd
d, wo, w = np.loadtxt('values.dat', unpack=True)
woE = np.sqrt(wo)
wE = np.sqrt(w)

if len(sys.argv) == 1:
	Y = np.log(d**2 * wo)
	YE = 1/wo * woE
	import kafe
	from kafe.function_library import linear_2par
	dataset = kafe.Dataset(data=(d, Y))
	dataset.add_error_source('y', 'simple', YE)
	fit = kafe.Fit(dataset, linear_2par)
	fit.do_fit(quiet=True)
	print(fit.final_parameter_values[0])
	print(fit.final_parameter_errors[0])
	print(fit.final_parameter_values[1])
	print(fit.final_parameter_errors[1])


plt.errorbar(d, Y, yerr=YE)
plt.show()
