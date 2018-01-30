.PHONY: data

data: plots/distrib-mit.pdf plots/distrib-ohne.pdf plots/mostly-linear-fit.pdf plots/hist-mit.pdf plots/hist-ohne.pdf

plots:
	mkdir plots

plots/distrib-%.pdf: source/%laser-blender.dat plots xy.py
	./xy.py $< distrib $@

plots/hist-%.pdf: source/%laser-blender.dat plots xy.py
	./xy.py $< hist2d $@

plots/mostly-linear-fit.pdf: source/ohnelaser-blender.dat plots xy.py
	./xy.py $< msd $@

clean:
	git clean -Xf
