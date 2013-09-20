LIBDIR=~/.local/lib

PYTHON_VERSION=3.3
SITEPACKAGES=${LIBDIR}/python${PYTHON_VERSION}/site-packages


.PHONY: style-check test

style-check:
	flake8 --max-complexity 6 ./pyversion/

test:
	python3 -m unittest --verbose --catch --failfast tests.py

clean:
	@rm -rv ./{pyversion/,}__pycache__/

install: test clean
	@cp -Rv ./pyversion ${SITEPACKAGES}
