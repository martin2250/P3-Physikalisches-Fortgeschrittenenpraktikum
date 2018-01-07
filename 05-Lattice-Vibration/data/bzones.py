#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import os

plot_path = os.path.join(os.path.dirname(__file__), 'plots')

a = 1
m = 11	#Na
m2 = 17	#Cl, lel
D = 2

def omega1(k, D, m, a):
	return np.sqrt(4 * D / m) * np.abs(np.sin(k * a / 2))

def omega2_plus(k, D, m1, m2, a):
	m = m1 * m2 / (m1 + m2)
	return D / m + D*np.sqrt(1 / m**2 - 4 / m1 / m2 * np.sin(k*a / 2)**2 )

def omega2_minus(k, D, m1, m2, a):
	m = m1 * m2 / (m1 + m2)
	return D / m - D*np.sqrt(1 / m**2 - 4 / m1 / m2 * np.sin(k*a / 2)**2 )
k_lin = np.linspace(-np.pi/a, np.pi/a, 1000)

""" First dispersion relation """
fig, ax = plt.subplots()
ax.plot(k_lin, omega1(k_lin, D, m, a))

#x-axis
ax.set_xlim(-np.pi / a, np.pi / a)
ax.set_xticks([-np.pi / a, np.pi / a])
ax.set_xticklabels(['$-\\frac{\\pi}{a}$', '$\\frac{\\pi}{a}$'])
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.xaxis.tick_bottom()
ax.annotate('$k$', xy=(1.025, 0), ha='left', va='top', xycoords='axes fraction')

#y-axis
ax.set_ylim(0, np.sqrt(np.sqrt(4 * D / m)))
ax.set_yticks([np.sqrt(np.sqrt(4 * D / m))])
ax.set_yticklabels(['$\\sqrt{\\frac{4D}{m}}$'])
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.yaxis.tick_left()
ax.annotate('$\\omega$', xy=(0.5, 1.05), ha='left', va='top', xycoords='axes fraction')
ax.grid(axis='x')
#save and clear figure
plt.savefig(os.path.join(plot_path, 'dispersion_single.pdf'))
plt.gcf().clear()

""" Second dispersion relation """
fig, ax = plt.subplots()

k_lin = np.linspace(-2*np.pi/a, 2*np.pi/a, 1000)
ax.plot(k_lin, omega2_plus(k_lin, D, m, m2, a), label='$\\omega_{+}$')
ax.plot(k_lin, omega2_minus(k_lin, D, m, m2, a), label='$\\omega_{-}$')

#x-axis
ax.set_xlim(-2*np.pi / a, 2*np.pi / a)
ax.set_xticks([-2*np.pi / a, -np.pi / a, np.pi / a, 2*np.pi / a])
ax.set_xticklabels(['$-\\frac{2\\pi}{a}$', '$-\\frac{\\pi}{a}$', '$\\frac{\\pi}{a}$', '$\\frac{2\\pi}{a}$'])
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.xaxis.tick_bottom()
ax.annotate('$k$', xy=(1.025, 0), ha='left', va='top', xycoords='axes fraction')

#y-axis
ax.set_yticks([])
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.yaxis.tick_left()
ax.annotate('$\\omega$', xy=(0.5, 1.05), ha='left', va='top', xycoords='axes fraction')

plt.axhspan(omega2_minus(np.pi/a, D, m, m2, a), omega2_plus(np.pi/a, D, m, m2, a), color='r', alpha=0.2)
ax.legend()
ax.grid(axis='x')
#save figure
plt.savefig(os.path.join(plot_path, 'dispersion_alternating.pdf'))
