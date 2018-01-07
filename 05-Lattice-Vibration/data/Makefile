.PHONY: data

data: plots/dispersion_single.pdf plots/dispersion_alternating.pdf

plots:
	mkdir plots

plots/dispersion_single.pdf: bzones.py plots
	./bzones.py

plots/dispersion_alternating.pdf: bzones.py plots plots/dispersion_single.pdf
	./bzones.py

clean:
	git clean -Xf
