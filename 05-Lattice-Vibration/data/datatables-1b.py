#!/usr/bin/python
import numpy as np
import os
N = 4

data_path = os.path.join(os.path.dirname(__file__), 'source')

tablestart = """
\\begin{tabular}{S|SS}
\\toprule
{excitation $n$}\t&\t{$\\omega_{n,\\text{1}}$}\t&\t{$\\omega_{n,\\text{2}}$} \\\\
\\midrule"""

tableend = """\\bottomrule
\\end{tabular}"""

for i in range(N):
	filename = 'a1-b-{:0>2d}.lvm'.format(i+1)
	path = os.path.join(data_path, filename)
	mode, w1, w2 = np.loadtxt(path, unpack=True)

	print(tablestart)

	for i in range(len(mode)):
			print("%i\t&\t%0.3f\t&\t%0.3f\t\\\\"%(mode[i]+1, 2*np.pi*w1[i], 2*np.pi*w2[i]))

	print(tableend)
