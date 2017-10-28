.PHONY: data

data: plots/e-spectrum.pdf

plots:
	mkdir plots

plots/e-spectrum.pdf: e-spectrum.py source/energyspectrum.dat plots
	./$< $@

clean:
	git clean -Xf
