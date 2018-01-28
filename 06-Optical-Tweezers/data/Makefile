.PHONY: data

data: plots/distrib-mit.pdf plots/distrib-ohne.pdf

plots:
	mkdir plots

plots/distrib-%.pdf: source/%laser-blender.dat plots xy.py
	./xy.py $< distrib $@

clean:
	git clean -Xf
