.PHONY: data

data: plots/dispersion_single.pdf plots/dispersion_alternating.pdf

plots:
	mkdir plots

plots/dispersion_alternating.pdf: bzones.py plots
	./bzones.py

plots/dispersion_single.pdf: plots/dispersion_alternating.pdf
	#do nothing

clean:
	git clean -Xf
