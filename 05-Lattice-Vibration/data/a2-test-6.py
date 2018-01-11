#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

ratios = np.zeros(12)

def thing(path):
	a, b = np.loadtxt(path, unpack=True)
	ratio = a / b
	r = np.std(ratio)
	print(path, ':', r)


thing('source/a2-n06.lvm')
thing('source/a2-n06-2min-later.lvm')
