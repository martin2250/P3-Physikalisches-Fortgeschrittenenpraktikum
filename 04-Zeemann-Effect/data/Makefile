.PHONY: data refresh remove

data: external

remove:
	rm -rf external/

# pipe symbol makes prerequisites build in order, not simultaeously
refresh: | remove external

external:
	mkdir external
	wget -o external.zip 127.0.0.1
	unzip external.zip -d external

clean:
	git clean -Xf
