.PHONY: data

data: plots/dispersion_single.pdf plots/dispersion_alternating.pdf plots/amplitude-ratio.pdf

plots:
	mkdir plots

plots/dispersion_alternating.pdf: bzones.py plots
	./bzones.py

plots/dispersion_single.pdf: plots/dispersion_alternating.pdf
	#do nothing

plots/amplitude-ratio.pdf: source/a2-n*.lvm a2-plot.py
	./a2-plot.py $@

clean:
	git clean -Xf
