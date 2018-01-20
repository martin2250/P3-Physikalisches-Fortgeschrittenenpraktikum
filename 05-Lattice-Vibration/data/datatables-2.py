#!/usr/bin/python
import numpy as np

N = 12
stuff,freqs, morestuff = np.loadtxt('source/a1-b-01.lvm', unpack=True)

tablestart = """
\\begin{table}[h]
	\\caption{Amplitudes of Biatomic Chain, 5th and 6th thingmajig, Modes %d to %d}
"""
tabstart = """	\\begin{tabular}{SS}
		\\toprule
		{$A_{5,%d}$}&
		{$A_{6,%d}$}\\\\
		\midrule"""

tabend = """		\\bottomrule
	\end{tabular}"""


tableend = """\\end{table}"""

for i in range(0, N, 4):
	data = []
	for j in range(4):
		data.append(np.loadtxt('source/a2-n{:02d}.lvm'.format((i + 1 + j)))[1:,:])
	# A = np.loadtxt('source/a2-n{:02d}.lvm'.format((i + 1)))
	# B = np.loadtxt('source/a2-n{:02d}.lvm'.format((i + 2)))



	# A = A[1:,:] #discard first value
	# B = B[1:,:]
    #
	# C = np.append(A, B, axis=1)


	print(tablestart%(i+1, i+4))


	for j in range(4):
		print(tabstart%(i+1+j, i+1+j))
		for t in data[j]:
				print("\t\t%0.2f&%0.2f\\\\"%tuple(t))
		print(tabend)
		if j != 3:
			print("\t\\hfillx")

	print(tableend)
