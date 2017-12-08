.PHONY: data

data: plots/coilE.pdf plots/coilF.pdf plots/coilG.pdf

plots:
	mkdir plots

plots/coilG.pdf: source/ESR-Coil-G.dat esreval.py plots
	./esreval.py

plots/coilE.pdf: source/ESR-Coil-G.dat esreval.py plots plots/coilG.pdf
	./esreval.py

plots/coilF.pdf: source/ESR-Coil-G.dat esreval.py plots plots/coilG.pdf plots/coilE.pdf
	./esreval.py

clean:
	git clean -Xf
