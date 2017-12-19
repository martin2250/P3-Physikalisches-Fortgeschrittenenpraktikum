.PHONY: data refresh remove

data: external

remove:
	rm -rf external/

# pipe symbol makes prerequisites build in order, not simultaeously
refresh: | remove external

external:
	mkdir external
	wget https://github.com/martin2250/P3-Physikalisches-Fortgeschrittenenpraktikum/releases/download/04-external/external.zip
	unzip external.zip -d external
	(cd external && rename _ - * && rename _ - *)

clean:
	git clean -Xf
