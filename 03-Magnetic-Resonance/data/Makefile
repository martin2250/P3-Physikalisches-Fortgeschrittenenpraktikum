.PHONY: data

data: plots/coilE.pdf plots/coilF.pdf plots/coilG.pdf

plots:
	mkdir plots

plots/coilE.pdf plots/coilF.pdf plots/coilG.pdf: source/ESR-Coil-E.dat esreval.py plots
	./esreval.py

clean:
	git clean -Xf
