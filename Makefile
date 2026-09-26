.PHONY: c clean check check-prebuild check-postbuild

c: clean

check-prebuild:
	python bin/check.py --group prebuild

check-postbuild:
	python bin/check.py --group postbuild

check: check-prebuild
	hugo --source tests/site --themesDir .. --destination tests/site/public --printPathWarnings --panicOnWarning
	$(MAKE) check-postbuild

clean:
	rm -rf -- public resources tests/site/public tests/site/resources tmp
	rm -f -- .hugo_build.lock tests/site/.hugo_build.lock
	find bin tests -type d -name __pycache__ -prune -exec rm -rf -- {} +
	find bin tests -type f -name '*.py[cod]' -delete
	find . -name .git -prune -o -type f -name .DS_Store -exec rm -f -- {} +
