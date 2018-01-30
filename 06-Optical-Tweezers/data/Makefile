.PHONY: data

data: plots/distrib-mit.pdf plots/distrib-ohne.pdf plots/mostly-linear-fit.pdf

plots:
	mkdir plots

plots/distrib-%.pdf: source/%laser-blender.dat plots xy.py
	./xy.py $< distrib $@

plots/mostly-linear-fit.pdf: source/ohnelaser-blender.dat plots xy.py
	./xy.py $< msd $@

clean:
	git clean -Xf
