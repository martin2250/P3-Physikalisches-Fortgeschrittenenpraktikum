.PHONY: data

data: plots/coilE.pdf plots/coilF.pdf plots/coilG.pdf

plots:
	mkdir plots

plots/coilE.pdf: source/ESR-Coil-E.dat esreval.py plots
	./esreval.py

plots/coilF.pdf: source/ESR-Coil-F.dat esreval.py plots
	./esreval.py

plots/coilG.pdf: source/ESR-Coil-G.dat esreval.py plots
	./esreval.py

clean:
	git clean -Xf
