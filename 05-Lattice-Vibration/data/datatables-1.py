#!/usr/bin/python
import numpy as np

N = 12
stuff,freqs, morestuff = np.loadtxt('source/a1-b-01.lvm', unpack=True)

tablestart = """
\\begin{table}
\\centering
\\caption{Mode: %d and %d}
\\begin{tabular}{TODO: your job}"""

tableend = """\\end{tabular}
\\end{table}"""

for i in range(0, N, 2):
	A = np.loadtxt('source/a2-n{:02d}.lvm'.format((i + 1)))
	B = np.loadtxt('source/a2-n{:02d}.lvm'.format((i + 2)))

	A = A[1:,:] #discard first value
	B = B[1:,:]

	C = np.append(A, B, axis=1)


	print(tablestart%(i+1, i+2))

	for c in C:
			print("%0.2f&%0.2f&%0.2f&%0.2f\\\\"%tuple(c))

	print(tableend)
