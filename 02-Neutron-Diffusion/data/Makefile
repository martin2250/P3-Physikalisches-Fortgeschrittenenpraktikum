.PHONY: data

data: plots/diffusion.pdf plots/relax.pdf

plots:
	mkdir plots

plots/diffusion.pdf: values.dat diffuse.py plots
	./diffuse.py save

plots/relax.pdf: values.dat relax.py plots
	./relax.py save

clean:
	git clean -Xf
