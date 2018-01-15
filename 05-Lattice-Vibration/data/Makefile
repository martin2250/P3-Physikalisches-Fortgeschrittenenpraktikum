.PHONY: data

data: plots/dispersion_single.pdf plots/dispersion_alternating.pdf plots/amplitude-ratio.pdf plots/dispersion_single_data.pdf plots/dispersion_alternating_data.pdf

plots:
	mkdir plots

plots/dispersion_alternating.pdf: bzones.py plots
	./bzones.py

plots/dispersion_single.pdf: plots/dispersion_alternating.pdf
	#do nothing

plots/amplitude-ratio.pdf: source/a2-n*.lvm a5-plot.py
	./a5-plot.py $@

plots/dispersion_alternating_data.pdf: source/a1-b-*.lvm dispersion_alternating.py
	./dispersion_alternating.py save

plots/dispersion_single_data.pdf: source/a1-a-*.lvm dispersion_single.py
	./dispersion_single.py save
	
clean:
	git clean -Xf
