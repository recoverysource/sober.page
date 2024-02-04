#!/usr/bin/make -f
##
# A simple wrapper for common developer commands.
# Most common commands: [run, clean]
##

site/index.html:
	hugo --minify -d site

browse: site/index.html
	sensible-browser site/index.html

run:
	hugo server --disableFastRender

clean:
	# hugo
	$(RM) -r .hugo_site resources

.PHONY: browse run clean
