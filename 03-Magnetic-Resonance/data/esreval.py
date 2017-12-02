#!/usr/bin/python
from __future__ import division, print_function
import sys
import numpy as np
import matplotlib.pyplot as plt
import kafe
from kafe.function_library import linear_2par

R = 1.07	#shunt
c = 3.96	#conversion factor for B-field

f1, U1_1, U2_1, U1 = np.loadtxt('./source/ESR-Coil-E.dat', unpack=True)
f2, U1_2, U2_2, U2 = np.loadtxt('./source/ESR-Coil-F.dat', unpack=True)
f3, U1_3, U2_3, U3 = np.loadtxt('./source/ESR-Coil-G.dat', unpack=True)

#conversion to magnetic field strength (in mT)
B1 = (U1*1e-3/R) * c
B2 = (U2*1e-3/R) * c
B3 = (U3*1e-3/R) * c

#errors
df = 0.1		#frequency error (in MHz)
dB = 52.3e-3	#calculated magnetic field error by hand, see paper

#datasets
dataset1 = kafe.Dataset(data=(B1, f1))
dataset2 = kafe.Dataset(data=(B2, f2))
dataset3 = kafe.Dataset(data=(B3, f3))

#error sources
dataset1.add_error_source('x', 'simple', dB)
dataset1.add_error_source('y', 'simple', df)

dataset2.add_error_source('x', 'simple', dB)
dataset2.add_error_source('y', 'simple', df)

dataset3.add_error_source('x', 'simple', dB)
dataset3.add_error_source('y', 'simple', df)

#fit
fit1 = kafe.Fit(dataset1, linear_2par)
fit2 = kafe.Fit(dataset2, linear_2par)
fit3 = kafe.Fit(dataset3, linear_2par)

fit1.do_fit(quiet=True)
fit2.do_fit(quiet=True)
fit3.do_fit(quiet=True)

slope1 = fit1.final_parameter_values[0]
slope2 = fit2.final_parameter_values[0]
slope3 = fit3.final_parameter_values[0]

slope_err1 = fit1.final_parameter_errors[0]
slope_err2 = fit2.final_parameter_errors[0]
slope_err3 = fit3.final_parameter_errors[0]

intercept1 = fit1.final_parameter_values[1]
intercept2 = fit2.final_parameter_values[1]
intercept3 = fit3.final_parameter_values[1]

intercepterr1 = fit1.final_parameter_errors[1]
intercepterr2 = fit2.final_parameter_errors[1]
intercepterr3 = fit3.final_parameter_errors[1]

#plots
linB1 = np.array([B1[0], B1[-1]])
linB2 = np.array([B2[0], B2[-1]])
linB3 = np.array([B3[0], B3[-1]])

plt.errorbar(B1, f1, fmt='o', markersize=2, xerr=dB, yerr=df, label='dataset')
plt.plot(linB1, slope1*linB1 + intercept1, label=('params:\n$a=(%.3f \\pm %.3f)\\ \\frac{MHz}{mT}$\n$b=(%.3f \\pm %.3f)$ MHz' %(slope1, slope_err1, intercept1, intercepterr1)))
plt.xlabel(r'$B$ in mT')
plt.ylabel(r'$f$ in MHz')
plt.legend()
plt.grid()
plt.savefig('./plots/coilE.pdf')
plt.gcf().clear()

plt.errorbar(B2, f2, fmt='o', markersize=2, xerr=dB, yerr=df, label='dataset')
plt.plot(linB2, slope2*linB2 + intercept2, label=('params:\n$a=(%.3f \\pm %.3f)\\ \\frac{MHz}{mT}$\n$b=(%.3f \\pm %.3f)$ MHz' %(slope2, slope_err2, intercept2, intercepterr2)))
plt.xlabel(r'$B$ in mT')
plt.ylabel(r'$f$ in MHz')
plt.legend()
plt.grid()
plt.savefig('./plots/coilF.pdf')
plt.gcf().clear()

plt.errorbar(B3, f3, fmt='o', markersize=2, xerr=dB, yerr=df, label='dataset')
plt.plot(linB3, slope3*linB3 + intercept3, label=('params:\n$a=(%.3f \\pm %.3f)\\ \\frac{MHz}{mT}$\n$b=(%.3f \\pm %.3f)$ MHz' %(slope3, slope_err3, intercept3, intercepterr3)))
plt.xlabel(r'$B$ in mT')
plt.ylabel(r'$f$ in MHz')
plt.legend()
plt.grid()
plt.savefig('./plots/coilG.pdf')
